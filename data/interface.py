from abc import ABC, abstractmethod
from .image import SKNScan, SKNMask


class DataManager:

    def __init__(self) -> None:
        return None
    

    def load_scan(self, filepath, *, has_phi):

        if self.scan_is_loaded():
            raise ValueError('image is already loaded and cannot be changed')
        
        img = SKNScan.read(filepath, has_phi=has_phi)
        self.set_scan(img)

        return None


    def set_scan(self, _img:SKNScan) -> None:

        '''loading the scan triggers a few actions, such as setting up the masks, etc.'''

        if self.scan_is_loaded():
            raise ValueError('image is already loaded and cannot be changed')
        else:
            self.scan = _img

        return None


    def add_mask(self, _m:SKNMask) -> None:
        if not hasattr(self, 'mask_list'):
            self.mask_list = []
        self.mask_list.append(_m)


    def scan_is_loaded(self) -> bool:

        if hasattr(self, 'scan') and self.scan:
            return True
        else:
            return False 


    def get_number_of_masks(self) -> int:
        if not hasattr(self, 'mask_list'):
            return 0
        return len(self.mask_list)


    def get_scan(self) -> SKNScan:

        if self.scan_is_loaded():
            return self.scan
        else:
            return None


    def get_mask(self, i:int) -> SKNMask:

        if i >= 0 and i < self.get_number_of_masks():
            return self.mask_list[i]
        else:
            return None


    def get_mask_list(self):

        if not hasattr(self, 'mask_list'):
            self.mask_list = []

        return self.mask_list


    def get_blended_image(self):

        if self.scan_is_loaded():
            img = self.get_scan()
            if self.get_number_of_masks():
                pass
                


    def get_blended_image_port(self):
        pass



class DataView:

    def set_data_manager(self, _data_manager) -> None:

        if self.get_data_manager():
            raise ValueError('data manager has already been set, and cannot be changed')
        
        else:
            _p = self
            try:
                while True:
                    assert _p.parent() is not None # has parent and parent is not None
                    _p = _p.parent()
            except:
                _p._data_manager = _data_manager
                return None



    def get_data_manager(self) -> DataManager:

        _p = self
        try:
            while True:
                assert _p.parent() is not None # has parent and parent is not None
                _p = _p.parent()
        except:
            if hasattr(_p, '_data_manager'):
                return _p._data_manager
            else:
                return None


    @abstractmethod
    def data_changed(self, *args, **kw) -> None:
        pass

