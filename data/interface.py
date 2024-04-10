from abc import ABC, abstractmethod

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, Slot, QEvent, QObject

from .manager import DataManager

class DataView:

    ''' this is a protocol class to bridge data management and view hierarchy'''

    def get_root_widget(self):
        p = self
        while True:
            _p = p.parent()
            if _p is not None and isinstance(_p, DataView):
                p = _p
            else:
                return p


    def set_data_manager(self, _data_manager:DataManager) -> None:

        '''sets data manager for the current widget'''

        if self.get_data_manager():
            raise ValueError('data manager has already been set, and cannot be changed')
        
        else:
            self._data_manager = _data_manager
            _data_manager.dataUpdated.connect(self.data_update)
            _data_manager.dataReloaded.connect(self.data_reload)
            _data_manager.scanLoaded.connect(self.data_reload)
            return None


    def get_data_manager(self) -> DataManager:

        '''gets data manager from the cloest parent widget'''

        _p = self
        while True:
            if _p is None: 
                return None
            elif isinstance(_p, DataView) and hasattr(_p, '_data_manager'):
                return _p._data_manager
            else:
                _p = _p.parent()
                continue


    @Slot()
    @abstractmethod
    def data_reload(self, *args, **kw) -> None:
        '''rebuild pipeline'''
        for v in self.children():
            if isinstance(v, DataView):
                v.data_reload(*args, **kw)

        return None


    @Slot()
    @abstractmethod
    def data_update(self, *args, **kw) -> None:
        '''update pipeline'''
        for v in self.children():
            if isinstance(v, DataView):
                v.data_update(*args, **kw)

        return None


