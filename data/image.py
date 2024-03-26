import os
import SimpleITK as sitk
import numpy as np


ALLOW_PHI = True
CAN_ERASE_PHI_AT_INIT = True


class ImageFrame:
    ''' this class encaps the size, spacing, and origin information of medical scans and segmentation masks.
    dimensions are ordered as +x, +y, +z
    on usage of this class:
        numpy arrays are ordered (+z, +y, +x) in this script, same as returned from sitk.GetArrayFromImage
        for legacy reasons, arrays decoded from AnatomicAligner bin file are ordered (-z, -y, +x), so a reversal is needed immediately on axial and coronal axes.
    '''

    def __init__(self, *, size, spacing=(1.,1.,1.), origin=(0.,0.,0.)) -> None:
        self.size = size
        self.spacing = spacing
        self.origin = origin
        return None



class Image(sitk.Image):

    def __init__(self, *args, 
                 identifier,        # this param helps program find image assets in memory and should not include phi
                 has_phi=True,      # whether the sitk image has PHI metadata attached
                 **kw,
                 ):
        
        super().__init__(*args)
        self.identifier = identifier
        self.has_phi = has_phi

        # more processing before image is ready to use

        if not self.has_phi:
            pass
            # self.erase_phi()

        else:
            if not ALLOW_PHI:
                if CAN_ERASE_PHI_AT_INIT:
                    self.erase_phi()

                else:
                    raise ValueError(
                        "This program allows only non-PHI data"
                    )
        
        return None


    def erase_phi(self):
        for key in self.GetMetaDataKeys():
            self.EraseMetaData(key)
        self.has_phi = False


    def phi(self):
        phi_dict = {}
        for key in self.GetMetaDataKeys():
            phi_dict[key] = self.GetMetaData(key)
        return phi_dict


    def read_dicom(cls, filepath, *, rescale=False, **kw):
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

        return cls(img, **kw)


    @classmethod
    def read(cls, filepath, **kw):

        if 'imageIO' in kw:
            if kw['imageIO'] == "GDCMImageIO":
                return cls.read_dicom(filepath, **kw)
            else:
                file_reader = sitk.ImageFileReader()
                file_reader.SetFileName(filepath)
                file_reader.SetImageIO(kw['imageIO'])
                file_reader.LoadPrivateTagsOn()
                file_reader.ReadImageInformation()
                img = file_reader.Execute()
        else:
            # try to read file as dicom
            try:
                return cls.read_dicom(filepath, **kw)

            except:
                pixel_id = kw['outputPixelType'] if 'outputPixelType' in kw else sitk.sitkUnknown
                image_io = kw['imageIO'] if 'imageIO' in kw else ''
                img = sitk.ReadImage(filepath, pixel_id, image_io)
                return cls(img, **kw)


class SkullEngineScan(Image):
    '''this class reads and writes medical scans in common formats'''

    @classmethod
    def read_bin_aa(cls, filepath, *, frame:ImageFrame, return_numpy=False, **kw):
        '''reads medical scans saved in AnatomicAligner bin file'''
        bytes = np.fromfile(filepath, dtype=np.int16)
        arr = bytes.reshape(frame.size[::-1])[::-1,::-1,:]
        if return_numpy:
            return arr
        img = sitk.GetImageFromArray(arr)
        img.SetSpacing(frame.spacing)
        img.SetOrigin(frame.origin)
        if 'has_phi' not in kw:
            kw['has_phi'] = False
        return cls(img, **kw)
    

    def write_bin_aa(self, filepath):
        '''writes medical scans to AnatomicAligner bin file'''
        arr = sitk.GetArrayFromImage(self)
        bytes = np.ravel(arr[::-1,::-1,:].astype(np.int16), order='C') # possible loss of precision since AA always uses int16
        return bytes.tofile(filepath)


    @classmethod
    def read(cls, filepath, *, return_numpy=False, **kw):
        img = super().read(filepath, rescale=True, **kw) # rescale is for dicom
        if return_numpy:
            return sitk.GetArrayFromImage(img)
        else:
            return img


    def save(self, filepath):
        sitk.WriteImage(self, filepath, imageIO='NiftiImageIO')
        return None
    


class SkullEngineMask(Image):
    '''this class encaps IO methods of segmentation masks of medical scans'''

    @classmethod
    def read_bin_aa(cls, filepath, *, frame:ImageFrame, return_numpy=False):
        # origin and spacing are optional for initializer but should be set later
        bytes = np.fromfile(filepath, dtype=np.int16)
        arr = np.zeros(frame.size[::-1])
        for i in range(0,bytes.size,4):
            arr[
                bytes[i+3],
                bytes[i],
                bytes[i+1]:bytes[i+1]+bytes[i+2]
                ] = 1
        arr = arr[::-1,::-1,:]
        if return_numpy:
            return arr
        img = sitk.GetImageFromArray(arr)
        img.SetSpacing(frame.spacing)
        img.SetOrigin(frame.origin)
        img.has_phi = False
        return cls(img)
        

    def write_bin_aa(self, filepath, split_if_multiple_found=True):
        arr = sitk.GetArrayFromImage(self)[::-1,::-1,:]
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
    def combine_bin_aa(cls, *filepath, frame:ImageFrame, return_numpy=False, **kw):
        # masks must be mutually disjoint
        arr = np.zeros(frame.size[::-1])
        for i, f in enumerate(filepath):
            m = cls.read_bin_aa(f, frame=frame, return_numpy=True)
            arr[m>0] = i

        if return_numpy:
            return arr
        
        img = sitk.GetImageFromArray(arr)
        img.SetSpacing(frame.spacing)
        img.SetOrigin(frame.origin)
        if 'has_phi' not in kw:
            kw['has_phi'] = False
        return cls(img, **kw)


    @classmethod
    def read(cls, filepath, *, return_numpy=False, **kw):
        img = super().read(filepath, rescale=False, **kw) # rescale is for dicom
        img = (img==100)
        if return_numpy:
            return sitk.GetArrayFromImage(img)
        else:
            return img


    def save(self, filepath):
        sitk.WriteImage(self, filepath, imageIO='NiftiImageIO')
        return None


