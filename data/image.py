import os
from time import perf_counter
from typing import List, Dict
import dataclasses
from dataclasses import dataclass, fields, field
from collections import namedtuple
import SimpleITK as sitk
from SimpleITK.SimpleITK import _SetImageFromArray
import numpy as np
from scipy.ndimage import zoom
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.util.numpy_support import numpy_to_vtk, vtk_to_numpy
from vtkmodules.vtkCommonCore import vtkDataArray

from .base import *
from .util import *


ALLOW_PHI = True
CAN_ERASE_PHI_AT_INIT = True
MASK_PIXEL_TYPE = sitk.sitkUInt32
MASK_DTYPE = np.uint32


@dataclass(kw_only=True)
class Image(SkullEngineData):
    '''this is the base class of all image assets used in this program
    it contains at least the following five attributes:
        data: an vtk data array of the pixel value, of size Nx1
        frame: origin, spacing, and dimensions of the data
        identifier: 1) id for program to find a particular image, and 2) metadata which is info contained in original image and often contains phi
        actions: operations perform on this image, in sequential order, which is useful for implementing undo stack or generating filter scripts
        extra: extra key-value pairs for ad hoc use
    '''

    data: vtkDataArray
    frame: ImageFrame # override Frame to provide size and spacing

    # @property
    # def data(self):
    #     return self.Get

    def numpy_array(self) -> np.ndarray: # points to the same data in memory
        '''this method creates a numpy ndarray that points to the same data array, and it is very fast'''
        arr = vtk_to_numpy(self.data)
        arr.shape = self.frame.size[::-1] # use this syntax to make sure arr remains a view of self.data
        return arr
    


    @classmethod
    def empty(cls, *, frame:ImageFrame, dtype:np.dtype, **kw):
        '''this method create an empty image'''
        arr = np.empty(frame.size[::-1], dtype=dtype)
        obj = cls(
            data=numpy_to_vtk(arr.flat, deep=0),
            frame=frame,
            identifier=Identifier()
        )
        obj.actions.append(SkullEngineAction((cls.__name__, 'empty', [], dict(frame=frame, dtype=dtype, **kw))))
        return obj


    @classmethod
    def read(cls, filepath, **kw):
        '''this method reads an image from file with some of the most common codec
        it always tries to read input file as dicom, and if it fails, it will use sitk.ReadImage with provided or inferred imageIO
        filepath is always path to a regular file, e.g., a file in the dicom series, or NIFTI image file with .nii.gz extension
        '''
        img = None

        if 'imageIO' not in kw or kw['imageIO'] == "GDCMImageIO":
            try:
                img = read_dicom(filepath, **kw)
                if 'outputPixelType' in kw:
                    img = sitk.Cast(img, kw['outputPixelType'])
            except:
                pass

        if img is None:
            img = sitk.ReadImage(filepath, 
                              kw['outputPixelType'] if 'outputPixelType' in kw else sitk.sitkUnknown, 
                              kw['imageIO'] if 'imageIO' in kw else ''
                              )
        
        obj = cls.from_itk(img)
        obj.actions.append(
            SkullEngineAction((cls.__name__, 'read', [filepath], kw))
        )

        return obj
    

    def save(self, filepath):
        '''this method writes the image to file
        currently this program only writes image in NIFTI'''
        sitk.WriteImage(self.itk(), filepath, imageIO='NiftiImageIO')
        return None
    

    @classmethod
    def from_vtk(cls, img:vtkImageData):
        '''this method creates Image object from vtkImageData instance
        image identifier/actions can be further modified on the returned object but not within the method'''

        arr = img.GetPointData().GetScalars()
        frame = ImageFrame(
                        size=img.GetDimensions(),
                        spacing=img.GetSpacing(),
                        origin=img.GetOrigin(),
                        )

        identifier = Identifier()

        return cls(data=arr, frame=frame, identifier=identifier)


    @classmethod
    def from_itk(cls, img:sitk.Image):
        '''this method creates Image object from sitk Image instance
        image identifier/actions can be further modified on the returned object but not within the method
        sitk.Image can contain metadata, therefore PHI'''

        arr = sitk.GetArrayFromImage(img)
        arr = numpy_to_vtk(arr.flat, deep=0)
        frame = ImageFrame(
                        size=img.GetSize(),
                        spacing=img.GetSpacing(),
                        origin=img.GetOrigin(),
                        )

        metadata = {}
        for key in img.GetMetaDataKeys():
            metadata[key] = img.GetMetaData(key)

        identifier = Identifier(metadata=metadata)

        return cls(data=arr, frame=frame, identifier=identifier)


    def itk(self, *, with_metadata=False):
        '''this method creates sitk.Image instance, with metadata attached optionally
        the program mainly uses sitk for image io operations, and vtk for rendering
        partly due to that fact, the returned sitk image does not share memory'''

        img = sitk.GetImageFromArray(self.numpy_array())
        img.SetOrigin(self.frame.origin)
        img.SetSpacing(self.frame.spacing)
        if with_metadata:
            for k,v in self.identifier.metadata.items():
                img.SetMetaData(k, v)

        return img
    

    def vtk(self):
        '''this method creates vtkImageData instance, which shares memory with data'''

        img = vtkImageData()
        img.GetPointData().SetScalars(self.data)
        img.SetOrigin(self.frame.origin)
        img.SetDimensions(self.frame.size)
        img.SetSpacing(self.frame.spacing)
        # img.SetDirectionMatrix(sitk_img.GetDirection())
        return img



@dataclass(kw_only=True)
class SkullEngineScan(Image):
    '''this class reads and writes medical scans in common formats'''

    @classmethod
    def read_bin_aa(cls, filepath, *, frame:ImageFrame):
        '''reads medical scans saved in AnatomicAligner bin file'''
        arr = np.fromfile(filepath, dtype=np.int16)
        arr = arr.reshape(frame.size[::-1])[::-1,::-1,:]
        t = perf_counter()
        arr = numpy_to_vtk(arr.flat, deep=0)
        print(f'to vtk: {perf_counter()-t} seconds')
        img = cls(data=arr, frame=frame, identifier=Identifier())
        img.actions.append(
            SkullEngineAction((cls.__name__, 'read_bin_aa', filepath, dict(frame=frame)))
        )
        return img
    
    def write_bin_aa(self, filepath):
        '''writes medical scans to AnatomicAligner bin file'''
        arr = self.numpy_array()
        bytes = np.ravel(arr[::-1,::-1,:].astype(np.int16), order='C') # possible loss of precision since AA always uses int16
        return bytes.tofile(filepath)


    @classmethod
    def read(cls, filepath, **kw):
        img = super().read(filepath, rescale=True, **kw) # rescale is for dicom
        img.identifier.confirm_phi(has_phi=kw['has_phi'] if 'has_phi' in kw else True)
        
        return img
        

    # def resample(self, *, new_spacing):
    #     return super().resample(new_spacing=new_spacing, mode='nearest')




@dataclass(kw_only=True)
class SkullEngineMask(Image):
    '''this class encaps IO methods of segmentation masks of medical scans
    it is agnostic to what is stored in its data'''

    reference_scan: SkullEngineScan = None
    frame:ImageFrame = None

    @property
    def frame(self):
        return self.reference_scan.frame
    

    # following setter is a compromise
    # for overriding data field with a property
    # luckily, frame is a frozen dataset
    @frame.setter
    def frame(self, f):

        pass


    @classmethod
    def empty(cls, *, ref_scan:SkullEngineScan, **kw):
        '''this is a convenience method that creates an empty mask to possibly represent multiple overlapping roi's, '''
        img = super().empty(frame=ref_scan.frame, dtype=MASK_DTYPE)
        img.reference_scan = ref_scan
        return img


    @classmethod
    def read_bin_aa(cls, filepath, *, frame:ImageFrame):
        # origin and spacing are optional for initializer but should be set later
        bytes = np.fromfile(filepath, dtype=np.int16)
        arr = np.zeros(frame.size[::-1], dtype=bool)
        for i in range(0,bytes.size,4):
            arr[
                bytes[i+3],
                bytes[i],
                bytes[i+1]:bytes[i+1]+bytes[i+2]
                ] = True
        arr = arr[::-1,::-1,:].astype(np.int8) # this is a single roi mask, so we use a more efficient data type
        arr = numpy_to_vtk(arr.flat, deep=0)
        return cls(data=arr, frame=frame, identifier=Identifier())


    def write_bin_aa(self, filepath, split_if_multiple_found=True):
        arr = self.numpy_array()[::-1,::-1,:]
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


    # def resample(self, *, new_spacing):
    #     return super().resample(new_spacing=new_spacing, mode='grid-constant', order=0, cval=0)


        # img = self.itk()
        # img = sitk.Resample(
        #     img, img.GetSize(),
        #     sitk.Transform(),
        #     sitk.sitkLinear,
        #     img.GetOrigin(),
        #     new_spacing,
        #     img.GetDirection(),
        #     sitk.sitkUnknown,
        #     True)


@dataclass(kw_only=True)
class SkullEngineMultiRoiMask(SkullEngineMask):

    @classmethod
    def read(cls, filepath, **kw):
        return super().read(filepath, outputPixelType=MASK_PIXEL_TYPE, **kw) # rescale is for dicom


    def set_true(self, *, mask_id, voxel_index=None):

        data = self.numpy_array()
        bin_or = np.array(2**mask_id, dtype=MASK_DTYPE)
        if voxel_index is None:
            data[...] |= bin_or
        else:
            data[voxel_index] |= bin_or


    def set_false(self, *, mask_id, voxel_index=None):
        
        data = self.numpy_array()
        bin_and = np.bitwise_not(np.array(2**mask_id, dtype=MASK_DTYPE))
        if voxel_index is None:
            data[...] &= bin_and
        else:
            data[voxel_index] &= bin_and
