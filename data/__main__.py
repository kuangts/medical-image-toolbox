#!/usr/bin/env python3

''' this file is executed when image_util is invoked as a module, possibly from the command line using `python -m`.
a simple ui is launch to allow various commonly used functions (resampling, conversion between different medical formats, etc.).
'''

import os
import sys
import shutil
import subprocess
import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt

from .image import ImageFrame, SkullEngineMask, SkullEngineScan
from .interface import DataManager

RAR_PROG = 'C:\\Program Files\\WinRAR\\Rar.exe'

def show(image_slice:np.array, mask_slice:np.array):

    fig = plt.figure(frameon=False)
    ax = fig.add_subplot()
    ax.imshow(image_slice, cmap=plt.cm.gray)
    masks_color = np.zeros(image_slice.shape)
    masks_color[...] = np.nan
    masks_color[mask_slice!=0] = 1
    ax.imshow(masks_color, alpha=.5)
    plt.show()

    return None



def test():
    
    os.chdir('C:\\data\\test')
    man = DataManager.from_aa('pre.CASS')
    i_slice = man.get_scan().frame.size[-1]//2
    img = man.get_scan()
    msk0 = man.get_mask(0)
    msk1 = man.get_mask(1)
    
    show(
        img.numpy_array()[i_slice,:,:],
        msk0.numpy_array()[i_slice,:,:],
    )

    img.save('img_rewrite.nii.gz')
    msk0.save('msk_rewrite0.nii.gz')
    msk1.save('msk_rewrite1.nii.gz')

    # view in itksnap

    # read from nifti and write to bin

    img_rewrite = SkullEngineScan.read('img_rewrite.nii.gz', has_phi=False)
    msk_rewrite0 = SkullEngineMask.read('msk_rewrite0.nii.gz')
    msk_rewrite1 = SkullEngineMask.read('msk_rewrite1.nii.gz')
    
    show(
        img_rewrite.numpy_array()[i_slice,:,:],
        msk_rewrite0.numpy_array()[i_slice,:,:],
    )

    img_rewrite.write_bin_aa('Patient_data_rewrite.bin')
    msk_rewrite0.write_bin_aa('0_rewrite.bin')
    msk_rewrite1.write_bin_aa('1_rewrite.bin')

    assert np.all(np.fromfile('Patient_data.bin', dtype=np.int16)==np.fromfile('Patient_data_rewrite.bin', dtype=np.int16)) and \
        np.all(np.fromfile('0.bin', dtype=np.int16)==np.fromfile('0_rewrite.bin', dtype=np.int16)) and \
        np.all(np.fromfile('1.bin', dtype=np.int16)==np.fromfile('1_rewrite.bin', dtype=np.int16))




if __name__ == '__main__':
    test()    

