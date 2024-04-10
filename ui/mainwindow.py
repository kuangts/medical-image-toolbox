# This Python file uses the following encoding: utf-8
import sys
import os
from datetime import datetime

import numpy as np
from PySide6.QtGui import QDragEnterEvent
from PySide6.QtWidgets import QApplication, QMainWindow

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkIOImage import vtkNIFTIImageReader
from PySide6.QtCore import Qt, Signal, Slot, QEvent, QObject
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QPlainTextEdit,
    QPushButton,
    QMainWindow,
    QFileDialog
)

import SimpleITK as sitk
from vtkmodules.util.numpy_support import vtk_to_numpy, numpy_to_vtk

from .mainwindow_ui import Ui_MainWindow
from .fourpane import FourPaneWindow
from .dialogs import *
from ..data import DataManager, DataView, SkullEngineMask, SkullEngineScan

DEFAULT_RESAMPLING_REGULATION = (1,1,3)


class AppWindow(QMainWindow, DataView):

    def __init__(self, parent=None):
        super().__init__(parent)

        # set ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # set data manager
        dm = DataManager()
        self.set_data_manager(dm)

        # other
        self.setCentralWidget(self.ui.fourpane)
        self.setAcceptDrops(True)
        return None


    def show(self):
        self.centralWidget().show()
        super().show()
        return None


    def data_update(self, *args, **kw):
        for v in self.children():
            if isinstance(v, DataView):
                v.data_update(*args, **kw)

        return None


    def data_reload(self, *args, **kw):
        for v in self.children():
            if isinstance(v, DataView):
                v.data_reload(*args, **kw)

        return None


    @Slot(bool)
    def on_actionOpenImage_triggered(self, checked):

        dm = self.get_data_manager()
        if dm.scan_is_loaded():
            raise ValueError('image is already loaded and cannot be changed')
        
        file, _ = QFileDialog.getOpenFileName(self, 'Open Image ...', '', "Image Files (*.nii.gz)")
        print(f'Open Image: {file}')
        img = SkullEngineScan.read(file, has_phi=False)
        dm.set_scan(img)

        return None


    @Slot(bool)
    def on_actionOpenMask_triggered(self, checked):

        dm = self.get_data_manager()
        if not dm.scan_is_loaded():
            raise ValueError('load image first')
        
        file, _ = QFileDialog.getOpenFileName(self, 'Open Mask ...', '', "Image Files (*.nii.gz)")
        print(f'Open Mask: {file}')
        img = SkullEngineMask.read(file)
        mask_arr = img.numpy_array()
        dm.add_mask(arr=mask_arr)
        self.data_update()



    @Slot(bool)
    def on_actionSaveImage_triggered(self, checked):

        dm = self.get_data_manager()
        if not dm.scan_is_loaded():
            raise ValueError('no image to save')

        file, _ = QFileDialog.getSaveFileName(self, 'Save Image to ...', '', "Image Files (*.nii.gz)")
        print(f'Save Image: {file}')
        img = dm.get_scan()
        img.save(file)


    @Slot(bool)
    def on_actionSaveMask_triggered(self, checked):

        dm = self.get_data_manager()
        if not dm.scan_is_loaded():
            raise ValueError('no image to save')
        
        file, _ = QFileDialog.getSaveFileName(self, 'Save Mask to ...', '', "Image Files (*.nii.gz)")
        print(f'Save Mask: {file}')
        img = dm.get_scan()
        img.save(file)


    @Slot(bool)
    def on_actionSetOrigin_triggered(self, checked):
        print('Setting Origin ...')
        origin = self.get_data_manager().get_scan().frame.origin
        d = SetOriginDialog(self)
        d.show(origin=origin)


    @Slot(bool)
    def on_actionResample_triggered(self, checked):
        print('Resampling ...')
        spacing = self.get_data_manager().get_scan().frame.spacing
        d = ResampleDialog(self)
        d.show(spacing=spacing)


    @Slot(bool)
    def on_actionConfSeg_triggered(self, checked):
        print('Configure Segmentation')
    

    @Slot(bool)
    def on_actionStartSeg_triggered(self, checked):
        print('Start Segmentation')


    @Slot(bool)
    def on_actionEraseMeta_triggered(self, checked):
        print('Erase PHI')
    

    # Drag and Drop
    # https://doc.qt.io/qtforpython-6/overviews/dnd.html

    def dragEnterEvent(self, event):

        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if len(urls) > 1:
                event.dropAction()
            else:
                event.acceptProposedAction()



    def dropEvent(self, event):

        file = event.mimeData().urls()[0].path()
        file = file.strip('/')
        dm = self.get_data_manager()
        
        if not dm.scan_is_loaded():
            print(f'Open Image: {file}')
            img = SkullEngineScan.read(file, has_phi=False)
            dm.set_scan(img)
            
        else:
            print(f'Open Mask: {file}')
            img = SkullEngineScan.read(file, has_phi=False)
            mask_arr = img.numpy_array()
            dm.add_mask(arr=mask_arr)

        event.acceptProposedAction()

        return None



    #     file_path = QFileDialog.getOpenFileName(dir=r'C:\data\pre-post-paired-with-dicom\n0002\20100921-pre')[0]
    #     image_id = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S-%f')
    #     sitk_img = None

    #     if os.path.isfile(file_path):
            
    #         try:
    #             reader = sitk.ImageFileReader()
    #             reader.SetFileName(file_path)
    #             reader.SetImageIO("GDCMImageIO")
    #             reader.ReadImageInformation()
                
    #         except Exception as e:
    #             try:
    #                 sitk_img = sitk.ReadImage(file_path)
                    
    #             except:
    #                 raise

    #         else:
    #             tags = {
    #                 'Name':'0010|0010',
    #                 'DOB':'0010|0030',
    #                 'Sex':'0010|0040',
    #                 'Study':'0008|0020',
    #             }
    #             for k,v in tags.items():
    #                 if reader.HasMetaDataKey(v):
    #                     tags[k] = reader.GetMetaData(v).strip()
    #             if reader.HasMetaDataKey('0020|000e'):
    #                 series_id = reader.GetMetaData('0020|000e')
    #                 filenames = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(os.path.dirname(file_path), series_id)
    #                 reader = sitk.ImageSeriesReader()
    #                 reader.SetImageIO("GDCMImageIO")
    #                 reader.SetFileNames(filenames)
    #                 sitk_img = reader.Execute()

    #     if sitk_img is not None:

    #         voxels = sitk.GetArrayFromImage(sitk_img)
    #         voxels = numpy_to_vtk(voxels.flatten(), deep=True)
    #         vtk_img = vtkImageData()
    #         vtk_img.GetPointData().SetScalars(voxels)
    #         vtk_img.SetOrigin(sitk_img.GetOrigin())
    #         vtk_img.SetDimensions(sitk_img.GetSize())
    #         vtk_img.SetSpacing(sitk_img.GetSpacing())
    #         vtk_img.SetDirectionMatrix(sitk_img.GetDirection())
    #         self.update_image(vtk_img)
    #         self.image = vtk_img
    #         self.image_path = file_path
    #         self.image_id = image_id

        





    # # def closeEvent(self, QCloseEvent):
    # #     super().closeEvent(QCloseEvent)
    # #     self.central.close()
    # #     return None


    # @Slot(float, float, float)
    # def set_reslice_center(self, x, y, z):

    #     # three views must be resliced at the same time
    #     new_slice = [float('nan')]*3
    #     self.image.TransformPhysicalPointToContinuousIndex([x,y,z], new_slice)
    #     i,j,k = new_slice
    #     if i>=self.centralWidget().iren_sagittal.viewer.GetSliceMin() and i<=self.centralWidget().iren_sagittal.viewer.GetSliceMax():
    #         self.centralWidget().iren_sagittal.viewer.SetSlice(int(round(i)))
    #     if j>=self.centralWidget().iren_coronal.viewer.GetSliceMin() and j<=self.centralWidget().iren_coronal.viewer.GetSliceMax():
    #         self.centralWidget().iren_coronal.viewer.SetSlice(int(round(j)))
    #     if k>=self.centralWidget().iren_axial.viewer.GetSliceMin() and k<=self.centralWidget().iren_axial.viewer.GetSliceMax():
    #         self.centralWidget().iren_axial.viewer.SetSlice(int(round(k)))

    #     return None

