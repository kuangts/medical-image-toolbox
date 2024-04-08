import os
import subprocess
from tempfile import TemporaryDirectory
import numpy as np
import SimpleITK as sitk
from PySide6.QtCore import Qt, Signal, Slot, QEvent, QObject
from .image import ImageFrame, ImageIdentifier, SkullEngineAsset, SkullEngineScan, SkullEngineMultiRoiMask, MASK_DTYPE, MASK_PIXEL_TYPE
RAR_PROG = 'C:\\Program Files\\WinRAR\\Rar.exe'


class DataManager(QObject):
    '''this class handles the internal logic of data assets, including scan, masks, 3d models, etc.
    specifically, it can load exactly one scan'''

    dataReloaded = Signal(SkullEngineAsset)
    dataUpdated = Signal(SkullEngineAsset)

    # def __init__(self) -> None:
    #     # self.image = None
    #     # self.object_list = []
    #     return None


    def reset(self) -> None:
        self.get_object_list().clear()

        return None
    

    @classmethod
    def from_aa(cls, filepath, **kw):
        filepath = os.path.realpath(os.path.expanduser(filepath))
        man = cls()
        cwd = os.getcwd()
        with TemporaryDirectory() as d:
            os.chdir(d)
            subprocess.run([RAR_PROG, 'x', '-idq', filepath, 'Patient_info.bin', 'Patient_data.bin', 'Mask_Info.bin'],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            with open('Patient_info.bin') as f:
                info = f.read().split(',')
            name, studydate, sex, _, _, sz, sy, sx, rx, ry, rz, _, cx, cy, cz, *_ = info
            frame = ImageFrame(size=[int(sx),int(sy),int(sz)], spacing=[float(rx),float(ry),float(rz)], origin=[0.,0.,0.])
            scan = SkullEngineScan.read_bin_aa('Patient_data.bin', frame=frame)
            scan.identifier.metadata["Patient's Name"] = name
            scan.identifier.metadata["Study Date"] = studydate
            scan.identifier.metadata["Patient's Sex"] = sex
            man.set_scan(scan)

            with open('Patient_info.bin') as f:
                info = f.read().strip(';').split(';')
            num_masks = int(info[0])
            subprocess.run([RAR_PROG, 'x', '-idq', filepath, *[f'{i}.bin' for i in range(num_masks)]],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            for i in range(num_masks):
                msk = SkullEngineMultiRoiMask.read_bin_aa(f'{i}.bin', frame=frame)
                man.add_mask(mask_id=i, arr=msk.numpy_array()>0)

            os.chdir(cwd)

        return man



    def set_scan(self, _img:SkullEngineScan, *, action_if_exists='reset') -> None:
        '''this method loads scan. this is usually the first step.
        action_if_exists can choose from reset|confirm|error '''

        if self.scan_is_loaded():
            if action_if_exists == 'reset':
                pass
            elif action_if_exists == 'confirm':
                pass
            elif action_if_exists == 'error':
                raise ValueError('image is already loaded and cannot be changed')
        else:
            self.scan = _img
            self.mask = SkullEngineMultiRoiMask.empty(frame=self.scan.frame)

        self.dataReloaded(_img)
        return None


    def get_next_available_mask_id(self) -> int:
        ids = self.get_mask_ids()
        if not len(ids):
            return 0
        max_id = np.max(ids)
        for i in range(max_id+1):
            if i not in ids:
                return i
        return max_id+1


    def add_mask(self, *, mask_id:int=None, arr:np.ndarray=None) -> None:
        if not self.scan_is_loaded():
            raise ValueError('load scan first')
        
        if mask_id in self.get_mask_ids():
            print(f'mask {mask_id} already exists and will be erased')
            self.mask.set_false(mask_id=mask_id)

        if arr is None:

            new_id = mask_id or self.get_next_available_mask_id()
            if new_id not in self.get_mask_ids():
                self.get_mask_ids().append(new_id)

        else:
            assert np.all(arr.shape[::-1] == self.get_scan().frame.size)
                
            if arr.dtype == bool:

                new_id = mask_id or self.get_next_available_mask_id()
                if new_id not in self.get_mask_ids():
                    self.get_mask_ids().append(new_id)
                self.mask.set_true(mask_id=new_id, voxel_index=arr)

            else:
                for v in np.unique(arr):
                    if v != 0:
                        new_id = mask_id or self.get_next_available_mask_id()
                        if new_id not in self.get_mask_ids():
                            self.get_mask_ids().append(new_id)
                        self.mask.set_true(mask_id=new_id, voxel_index=arr==v)

        self.dataUpdated.emit(self.get_mask())
        
        return None
        
    

    def scan_is_loaded(self) -> bool:

        if hasattr(self, 'scan') and self.scan:
            return True
        else:
            return False 


    def get_mask_ids(self) -> list:
        if not hasattr(self, '_mask_ids'):
            self._mask_ids = []
        return self._mask_ids


    def get_scan(self) -> SkullEngineScan:

        if self.scan_is_loaded():
            return self.scan
        else:
            return None


    def get_mask(self) -> SkullEngineMultiRoiMask:

        if self.scan_is_loaded():
            return self.mask
        else:
            return None



    def get_object_list(self) -> list:
        '''object list is composed of
        1) object pipelined from masks, and
        2) objects imported or otherwise created (by cutting, duplicating, etc.)'''

        if not hasattr(self, 'object_list'):
            self.object_list = []

        return self.object_list


    def resample(self, *, new_spacing):
        img = self.get_scan()
        if img:
            img.resample(new_spacing=new_spacing)
            self.get_mask().resample(new_spacing=new_spacing)



    # def get_blended_image(self):

    #     if self.scan_is_loaded():
    #         img = self.get_scan()
    #         if self.get_number_of_masks():
    #             pass
                


    # def get_blended_image_port(self):
    #     pass


