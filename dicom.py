import os, time, csv
from collections.abc import Sequence
import SimpleITK as sitk
from numpy import log10


def get_info(file):
    file_reader = sitk.ImageFileReader()
    file_reader.SetFileName(file)
    file_reader.SetImageIO("GDCMImageIO")
    file_reader.LoadPrivateTagsOn()
    file_reader.ReadImageInformation()
    info = {k: file_reader.GetMetaData(k) for k in file_reader.GetMetaDataKeys()}
    return info


def sort_by_series_id(dicom_dir):
    series_ids = sitk.ImageSeriesReader.GetGDCMSeriesIDs(dicom_dir)
    filenames_per_id = { id:sitk.ImageSeriesReader.GetGDCMSeriesFileNames(dicom_dir, id) for id in series_ids}
    return filenames_per_id


def select_series(dicom_dir, user_choose=True):

    file_names_by_id = sort_by_series_id(dicom_dir)

    if not len(file_names_by_id):
        raise ValueError("directory \"" + dicom_dir + "\" does not contain a DICOM series.")
    
    elif len(file_names_by_id) == 1:
        return list(file_names_by_id.values())[0]

    else:
        if not user_choose:
            raise ValueError('more than one series found')

        for i, (id, names) in enumerate(file_names_by_id.items()):
            print(f'  {i:>2} - {id} - {len(names)} slices')
        id_selected = int(input('please select series to read...\n'))

        return list(file_names_by_id.values())[id_selected]
        

def read(file_or_dir, return_image=True, return_info=True, user_choose_if_multiple_series_found=False, rescale=True):

    file_or_dir = os.path.normpath(os.path.realpath(file_or_dir))

    if os.path.isfile(file_or_dir):

        info = get_info(file_or_dir)
        series_instance_uid = info['0020|000e']
        dicom_names = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(os.path.dirname(file_or_dir), series_instance_uid)
    
    elif os.path.isdir(file_or_dir):

        dicom_names = select_series(file_or_dir)
        info = get_info(dicom_names[0])

    else:
        raise ValueError(f'{file_or_dir} is not a valid path')
    
    return_tuple = ()

    if return_image:
        reader = sitk.ImageSeriesReader()
        reader.SetImageIO("GDCMImageIO")
        reader.SetFileNames(dicom_names)
        img = reader.Execute()

        if rescale:
            _rescale(img, info)

        return_tuple += (img,)
        
    if return_info:
        return_tuple += (info,)

    return return_tuple
    

def _rescale(img, info):
    '''The value b in relationship between stored values (SV) and the output units.
    Output units = m*SV+b # SV - stored values
    If Image Type (0008,0008) Value 1 is ORIGINAL and Value 3 is not LOCALIZER, 
    and Multi-energy CT Acquisition (0018,9361) is either absent or NO, 
    output units shall be Hounsfield Units (HU).'''

    # info is not modified
    # img is modified in-place
    if '0028|1052' in info and '0028|1053' in info:
        arr = sitk.GetArrayViewFromImage(img)
        try:
            b,m = float(info['0028|1052']), float(info['0028|1053']) # Rescale Intercept, Rescale Slope
            arr = (arr*m+b).astype(arr.dtype)
            sitk._SetImageFromArray(arr, img)
        except:
            print('dicom rescale failed')
    return None


def write(img, dcm_dir, info={}, prefix='', postfix='.dcm'):
    dcm_dir = os.path.normpath(os.path.realpath(os.path.expanduser(dcm_dir)))
    if os.path.exists(dcm_dir) and not os.path.isdir(dcm_dir):
        print(f'cannot write to {dcm_dir}, not a directory')
    else:
        os.makedirs(dcm_dir, exist_ok=True)
    if os.listdir(dcm_dir):
        print(f'cannot write to {dcm_dir}, directory not empty')
        return

    # downloaded from simpleitk example 'Dicom Series From Array'
    # at https://simpleitk.readthedocs.io/en/master/link_DicomSeriesFromArray_docs.html
    # modified to always write int16, original huntsfield value

    # Write the 3D image as a series
    # IMPORTANT: There are many DICOM tags that need to be updated when you modify
    #            an original image. This is a delicate operation and requires
    #            knowledge of the DICOM standard. This example only modifies some.
    #            For a more complete list of tags that need to be modified see:
    #                  http://gdcm.sourceforge.net/wiki/index.php/Writing_DICOM
    #            If it is critical for your work to generate valid DICOM files,
    #            It is recommended to use David Clunie's Dicom3tools to validate
    #            the files:
    #                  http://www.dclunie.com/dicom3tools.html

    writer = sitk.ImageFileWriter()
    writer.SetImageIO("GDCMImageIO")
    # Use the study/series/frame of reference information given in the meta-data
    # dictionary and not the automatically generated information from the file IO
    writer.KeepOriginalImageUIDOn()

    modification_time = time.strftime("%H%M%S")
    modification_date = time.strftime("%Y%m%d")

    # Copy some of the tags and add the relevant tags indicating the change.
    # For the series instance UID (0020|000e), each of the components is a number,
    # cannot start with zero, and separated by a '.' We create a unique series ID
    # using the date and time. Tags of interest:
    direction = img.GetDirection()
    # Tags shared by the series.
    series_tag_values = {
        "0008|0012":modification_date,
        "0008|0013":modification_time,
        "0008|0060": "CT",
        # Setting the type to CT so that the slice location is preserved and the thickness is carried over.
        "0008|0008": "DERIVED\\SECONDARY",  # Image Type
        "0020|000e": "1.2.826.0.1.3680043.2.1125." + modification_date + ".1" + modification_time, # Series Instance UID
        "0020|0037": '\\'.join(map(str, (direction[0], direction[3], direction[6],
                                         direction[1], direction[4], direction[7]))),  # Image Orientation # (Patient)
    }

    series_tag_values.update(info)

    # Write slices to output directory
    for i in range(img.GetDepth()):
        image_slice = img[:, :, i]
        #   Image Position (Patient) --  also determines the spacing between slices
        series_tag_values["0020|0032"] = '\\'.join(map(str, img.TransformIndexToPhysicalPoint((0, 0, i))))
        #   Instance Number
        series_tag_values["0020|0013"] = str(i)
        #   set
        for k, v in series_tag_values.items():
            image_slice.SetMetaData(k, v)
        # Write to the output directory and add the extension dcm, to force
        # writing in DICOM format.
        n_digits = int(log10(img.GetDepth()-1)) + 1
        writer.SetFileName(os.path.join(dcm_dir, f'{prefix}{i+1:0{n_digits}}{postfix}.dcm'))
        writer.Execute(image_slice)



