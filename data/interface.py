from abc import ABC, abstractmethod
from .manager import DataManager

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

