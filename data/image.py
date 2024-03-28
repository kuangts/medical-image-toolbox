import os
import SimpleITK as sitk
import numpy as np
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.util.numpy_support import numpy_to_vtk


ALLOW_PHI = True
CAN_ERASE_PHI_AT_INIT = True


def read_dicom(filepath, *, rescale=False, **kw):
    # get series id from the file
    file_reader = sitk.ImageFileReader()
    file_reader.SetFileName(filepath)
    file_reader.SetImageIO("GDCMImageIO")
    file_reader.LoadPrivateTagsOn()
    file_reader.ReadImageInformation()
    series_instance_uid = ''
    if file_reader.HasMetaDataKey('0020|000e'):
        series_instance_uid = file_reader.GetMetaData('0020|000e')

    # find all the files in the same series and same directory
    dicom_names = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(os.path.dirname(filepath), series_instance_uid)

    # read the series
    reader = sitk.ImageSeriesReader()
    reader.SetImageIO("GDCMImageIO")
    reader.SetFileNames(dicom_names)
    reader.SetOutputPixelType()
    reader.LoadPrivateTagsOn()
    img = reader.Execute()

    if rescale:
        if img.HasMetaDataKey('0028|1052') and img.HasMetaDataKey('0028|1053'):
            b,m = float(img.GetMetaData('0028|1052')), float(img.GetMetaData('0028|1053')) # Rescale Intercept, Rescale Slope
        else:
            b,m = -1024., 1.
        
        img = (img-m) / m

    return img


class ImageFrame:
    ''' this class encaps the size, spacing, and origin information of medical scans and segmentation masks.
    dimensions are ordered as +x, +y, +z
    on usage of this class:
        numpy arrays are ordered (+z, +y, +x) in this script, same as returned from sitk.GetArrayFromImage
        for legacy reasons, arrays decoded from AnatomicAligner bin file are ordered (-z, -y, +x), so a reversal is needed immediately on axial and coronal axes.
    '''

    def __init__(self, *, size:tuple, spacing:tuple, origin:tuple) -> None:
        self.size = size
        self.spacing = spacing
        self.origin = origin
        return None



class Image:

    def __init__(self, *, data, frame, has_phi, identifier='', metadata={}, **kw):

        self.data = data
        self.frame = frame
        self.has_phi = has_phi
        self.identifier = identifier
        self.metadata = metadata
        for k,v in kw.items():
            setattr(self, k, v)
        return None


    @classmethod
    def read(cls,
                 filepath,
                 has_phi=True,      # whether the sitk image has PHI metadata attached
                 **kw,
                 ):
        

        if 'imageIO' not in kw or kw['imageIO'] == "GDCMImageIO":
            try:
                img = read_dicom(filepath, **kw)
            except:
                pass

        img = sitk.ReadImage(filepath, 
                              kw['outputPixelType'] if 'outputPixelType' in kw else sitk.sitkUnknown, 
                              kw['imageIO'] if 'imageIO' in kw else ''
                              )
            
        data = sitk.GetArrayFromImage(img)
        frame = ImageFrame(
                        size=img.GetSize(),
                        spacing=img.GetSpacing(),
                        origin=img.GetOrigin(),
                        )

        # more processing before image is ready to use
        metadata = {}

        if ALLOW_PHI:
            for key in img.GetMetaDataKeys():
                metadata[key] = img.GetMetaData(key)

        elif has_phi:

            if CAN_ERASE_PHI_AT_INIT:
                metadata = {}
                has_phi = False

            else:
                raise ValueError(
                    "This program allows only non-PHI data"
                )
        
        return cls(data=data, frame=frame, has_phi=has_phi, identifier=filepath, metadata=metadata)
    

    def save(self, filepath):
        sitk.WriteImage(self.itk(), filepath, imageIO='NiftiImageIO')
        return None
    


    def itk(self, *, with_metadata=False):
        arr = self.data
        if arr.dtype == bool:
            arr = arr.astype(np.int8)
        img = sitk.GetImageFromArray(arr)
        img.SetOrigin(self.frame.origin)
        img.SetSpacing(self.frame.spacing)
        if with_metadata:
            for k,v in self.metadata.items():
                img.SetMetaData(k,self.metadata(v))

        return img
    

    def vtk(self):
        arr = self.data
        if arr.dtype == bool:
            arr = arr.astype(np.int8)
        arr = numpy_to_vtk(arr.flatten(), deep=True)
        vtk_img = vtkImageData()
        vtk_img.GetPointData().SetScalars(arr)
        vtk_img.SetOrigin(self.frame.origin)
        vtk_img.SetDimensions(self.data.shape[::-1])
        vtk_img.SetSpacing(self.frame.spacing)
        # vtk_img.SetDirectionMatrix(sitk_img.GetDirection())
        return vtk_img



class SkullEngineScan(Image):
    '''this class reads and writes medical scans in common formats'''


    @classmethod
    def read_bin_aa(cls, filepath, frame:ImageFrame):
        '''reads medical scans saved in AnatomicAligner bin file'''
        bytes = np.fromfile(filepath, dtype=np.int16)
        arr = bytes.reshape(frame.size[::-1])[::-1,::-1,:]
        return cls(data=arr, frame=frame, has_phi=False, identifier=filepath)
    

    def write_bin_aa(self, filepath):
        '''writes medical scans to AnatomicAligner bin file'''
        bytes = np.ravel(self.data[::-1,::-1,:].astype(np.int16), order='C') # possible loss of precision since AA always uses int16
        return bytes.tofile(filepath)


    @classmethod
    def read(cls, filepath, **kw):
        return super().read(filepath, rescale=True, **kw) # rescale is for dicom


class SkullEngineMask(Image):
    pass


class SkullEngineSingleRoiMask(Image):
    '''this class encaps IO methods of segmentation masks of medical scans'''


    def __init__(self, *, data, frame, has_phi, identifier='', metadata={}, **kw):
        if data.dtype != bool:
            print(f'creating single ROI mask from {data.dtype} data; might result in loss of ROIs')
            data = data>0
        super().__init__(data=data, frame=frame, has_phi=has_phi, identifier=identifier, metadata=metadata, **kw)



    @classmethod
    def read_bin_aa(cls, filepath, frame:ImageFrame):
        # origin and spacing are optional for initializer but should be set later
        bytes = np.fromfile(filepath, dtype=np.int16)
        arr = np.zeros(frame.size[::-1], dtype=bool)
        for i in range(0,bytes.size,4):
            arr[
                bytes[i+3],
                bytes[i],
                bytes[i+1]:bytes[i+1]+bytes[i+2]
                ] = True
        arr = arr[::-1,::-1,:]
        return cls(data=arr, frame=frame, has_phi=False, identifier=filepath)
        

    def write_bin_aa(self, filepath, split_if_multiple_found=True):
        arr = self.data[::-1,::-1,:]
        vals = np.unique(arr)
        vals = vals[vals!=0]
        multiple_found = len(vals) > 1

        if not split_if_multiple_found and multiple_found:
            raise ValueError('multiple masks found.')

        for v in vals:
            seg_list = []
            arrv = arr==v
            for i in range(arrv.shape[0]):
                for j in range(arrv.shape[1]):
                    segs = np.diff(np.hstack((0, arrv[i,j], 0)))
                    for start, end in zip(np.nonzero(segs==1)[0], np.nonzero(segs==-1)[0]):
                        seg_list += [ j,start,end-start,i ]
            bytes = np.array(seg_list, dtype=np.int16)
            if multiple_found:
                _d, _f = os.path.splitext(filepath)
                bytes.tofile(_d + f"_{v}"+ _f)
            else:
                bytes.tofile(filepath)
            
        return None
    
    
    @classmethod
    def read(cls, filepath, **kw):
        return super().read(filepath, rescale=False, **kw) # rescale is for dicom


class SkullEngineMultipleRoiMask(Image):
    '''this class encaps IO methods of segmentation masks of medical scans with multiple ROIs'''


    

    @classmethod
    def combine(cls, *args:list[Image]):
        # masks must be mutually disjoint
        arr = args[0].data.copy()
        frame = 
        arr = np.zeros(frame.size[::-1])
        for i, f in enumerate(filepath):
            m = cls.read_bin_aa(f, frame=frame)
            arr[m.data>0] = i
        
        return SkullEngineMultipleROIMask(data=arr, frame=frame, has_phi=False, identifier=';'.join(filepath))


