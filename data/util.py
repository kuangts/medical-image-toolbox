
import os
import numpy as np
from .base import *
from scipy.ndimage import zoom
from vtkmodules.util.numpy_support import vtk_to_numpy, numpy_to_vtk


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
            b,m = -1024., 1. # this is a compramise for current situation
        
        img = (img-m) / m

    return img


def resample(arr:np.ndarray, *, old_spacing, new_spacing, **kw) -> np.ndarray:

    # kw is passed to zoom method, and often contains
    #   mode='grid-constant' # controls behavior outside bounds
    #   order=0 
    #   cval=0

    z = np.array(old_spacing)/np.array(new_spacing)
    arr = zoom(arr, zoom=z[::-1], grid_mode=True, **kw).astype(arr.dtype)

    return arr

    

