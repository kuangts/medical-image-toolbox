#!/usr/bin/env python3

''' this file is executed when image_util is invoked as a module, possibly from the command line using `python -m`.
a simple ui is launch to allow various commonly used functions (resampling, conversion between different medical formats, etc.).
'''

import os
import sys
import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt

from .image import ImageFrame, SkullEngineMask, SkullEngineScan


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




def test(argv):

    i_slice = 200
    frame = ImageFrame(size=(576,576,432), spacing=(0.4,0.4,0.4))
    os.chdir('C:\\data\\test')
    
    # decompress bin files from cass

    # read from bin and write to nifti

    img = SkullEngineScan.read_bin_aa('Patient_data.bin', frame=frame)
    msk0 = SkullEngineMask.read_bin_aa('0.bin', frame=frame)
    msk1 = SkullEngineMask.read_bin_aa('1.bin', frame=frame)
    msk = SkullEngineMask.combine_bin_aa('0.bin','1.bin', frame=frame)


    show(
        sitk.GetArrayFromImage(img)[i_slice,:,:],
        sitk.GetArrayFromImage(msk)[i_slice,:,:],
    )

    img.write_nifti('img_rewrite.nii.gz')
    msk0.write_nifti('msk_rewrite0.nii.gz')
    msk1.write_nifti('msk_rewrite1.nii.gz')

    # view in itksnap

    # read from nifti and write to bin

    img_rewrite = SkullEngineScan.read_nifti('img_rewrite.nii.gz')
    msk_rewrite0 = SkullEngineMask.read_nifti('msk_rewrite0.nii.gz')
    msk_rewrite1 = SkullEngineMask.read_nifti('msk_rewrite1.nii.gz')
    
    show(
        sitk.GetArrayFromImage(img)[i_slice,:,:],
        sitk.GetArrayFromImage(msk)[i_slice,:,:],
    )

    img_rewrite.write_bin_aa('Patient_data_rewrite.bin')
    msk_rewrite0.write_bin_aa('0_rewrite.bin')
    msk_rewrite1.write_bin_aa('1_rewrite.bin')

    assert np.all(np.fromfile('Patient_data.bin', dtype=np.int16)==np.fromfile('Patient_data_rewrite.bin', dtype=np.int16)) and \
        np.all(np.fromfile('0.bin', dtype=np.int16)==np.fromfile('0_rewrite.bin', dtype=np.int16)) and \
        np.all(np.fromfile('1.bin', dtype=np.int16)==np.fromfile('1_rewrite.bin', dtype=np.int16))

    # put bin files in cass file and view


def main(argv):
    pass




if __name__ == '__main__':
    test()    

# if __name__ == '__main__':
#     main(sys.argv[1:])