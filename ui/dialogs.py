from functools import partial

from PySide6.QtCore import Qt, Signal, Slot, QEvent, QObject
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import QDialog, QLineEdit, QAbstractButton

from ..data import DataView, DataManager
from .origin_ui import Ui_Dialog as ui_origin
from .resample_ui import Ui_Dialog as ui_resample


class SetOriginDialog(QDialog, DataView):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.ui = ui_origin()
        self.ui.setupUi(self)
        self.origin = [float('nan'),]*3
        self.new_origin = [float('nan'),]*3
        self.translation = [0.,0.,0.]

        validator = QDoubleValidator()

        self.ui.newx.setValidator(validator)
        self.ui.newy.setValidator(validator)
        self.ui.newz.setValidator(validator)
        self.ui.newdx.setValidator(validator)
        self.ui.newdy.setValidator(validator)
        self.ui.newdz.setValidator(validator)

        self.ui.newx.editingFinished.connect(partial(self.edited, self.ui.newx))
        self.ui.newy.editingFinished.connect(partial(self.edited, self.ui.newy))
        self.ui.newz.editingFinished.connect(partial(self.edited, self.ui.newz))
        self.ui.newdx.editingFinished.connect(partial(self.edited, self.ui.newdx))
        self.ui.newdy.editingFinished.connect(partial(self.edited, self.ui.newdy))
        self.ui.newdz.editingFinished.connect(partial(self.edited, self.ui.newdz))

        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.clicked.connect(self.button_clicked)

        return None


    def show(self, *, origin):
        self.origin = list(map(float,origin))
        self.new_origin = list(map(float,origin))
        self.set_new_origin(self.origin)
        self.set_translation(self.translation)
        print(f'current origin is {self.origin}')
        super().show()

        return None


    def set_new_origin(self, o):
        self.ui.newx.setText(f'{o[0]:.6f}')
        self.ui.newy.setText(f'{o[1]:.6f}')
        self.ui.newz.setText(f'{o[2]:.6f}')


    def set_translation(self, t):
        self.ui.newdx.setText(f'{t[0]:.6f}')
        self.ui.newdy.setText(f'{t[1]:.6f}')
        self.ui.newdz.setText(f'{t[2]:.6f}')


    def edited(self, line_edit:QLineEdit):

        if line_edit in (self.ui.newx, self.ui.newy, self.ui.newz):

            if line_edit == self.ui.newx:
                self.new_origin[0] = float(self.ui.newx.text())
                self.translation[0] = self.new_origin[0] - self.origin[0]
            if line_edit == self.ui.newy:
                self.new_origin[1] = float(self.ui.newy.text())
                self.translation[1] = self.new_origin[1] - self.origin[1]
            if line_edit == self.ui.newz:
                self.new_origin[2] = float(self.ui.newz.text())
                self.translation[2] = self.new_origin[2] - self.origin[2]
            print(f'new origin is now {self.new_origin}')

        elif line_edit in (self.ui.newdx, self.ui.newdy, self.ui.newdz):
            if line_edit == self.ui.newdx:
                self.translation[0] = float(self.ui.newdx.text())
                self.new_origin[0] = self.origin[0] + self.translation[0]
            if line_edit == self.ui.newdy:
                self.translation[1] = float(self.ui.newdy.text())
                self.new_origin[1] = self.origin[1] + self.translation[1]
            if line_edit == self.ui.newdz:
                self.translation[2] = float(self.ui.newdz.text())
                self.new_origin[2] = self.origin[2] + self.translation[2]
            print(f'translation is now {self.translation}')

        self.set_new_origin(self.new_origin)
        self.set_translation(self.translation)

        return None


    def button_clicked(self, b:QAbstractButton) -> None:

        if b.text() == 'Reset':
            self.new_origin = self.origin.copy()
            self.translation = [0.,0.,0.]
            self.set_new_origin(self.new_origin)
            self.set_translation(self.translation)
            
        elif b.text() == 'OK':
            scan = self.get_data_manager().get_scan()
            scan.frame.origin = tuple(self.new_origin)
            self.get_data_manager().dataReloaded.emit(scan)
            print(f'New origin is set {scan.frame.origin}')


class ResampleDialog(QDialog, DataView):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.ui = ui_resample()
        self.ui.setupUi(self)
        self.spacing = [float('nan'),]*3
        self.new_spacing = [float('nan'),]*3

        validator = QDoubleValidator()

        self.ui.newx.setValidator(validator)
        self.ui.newy.setValidator(validator)
        self.ui.newz.setValidator(validator)

        self.ui.newx.editingFinished.connect(partial(self.edited, self.ui.newx))
        self.ui.newy.editingFinished.connect(partial(self.edited, self.ui.newy))
        self.ui.newz.editingFinished.connect(partial(self.edited, self.ui.newz))

        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.clicked.connect(self.button_clicked)

        return None


    def show(self, *, spacing):
        self.spacing = list(map(float,spacing))
        self.new_spacing = list(map(float,spacing))
        self.set_new_spacing(self.spacing)
        print(f'current spacing is {self.spacing}')
        super().show()

        return None


    def set_new_spacing(self, o):
        self.ui.newx.setText(f'{o[0]:.6f}')
        self.ui.newy.setText(f'{o[1]:.6f}')
        self.ui.newz.setText(f'{o[2]:.6f}')


    def edited(self, line_edit:QLineEdit):

        if line_edit == self.ui.newx:
            self.new_spacing[0] = float(self.ui.newx.text())
        if line_edit == self.ui.newy:
            self.new_spacing[1] = float(self.ui.newy.text())
        if line_edit == self.ui.newz:
            self.new_spacing[2] = float(self.ui.newz.text())

        print(f'new spacing is now {self.new_spacing}')

        return None


    def button_clicked(self, b:QAbstractButton) -> None:

        if b.text() == 'Reset':
            self.new_spacing = self.spacing.copy()
            self.set_new_spacing(self.new_spacing)
            
        elif b.text() == 'OK':
            dm = self.get_data_manager()
            if dm:
                dm.resample(new_spacing=self.new_spacing)
                scan = dm.get_scan()
                self.get_data_manager().dataReloaded.emit(scan)
                print(f'New spacing is set {scan.frame.spacing}')


