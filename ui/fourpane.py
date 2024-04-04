#!/usr/bin/env python

import sys, os, glob, json, math
from abc import abstractmethod, ABC
from collections.abc import Collection
## site packages
import numpy as np
from numbers import Number
# vtk
import vtk
from vtkmodules.vtkFiltersSources import vtkSphereSource 
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera, vtkInteractorStyleTrackballActor, vtkInteractorStyleImage
from vtkmodules.vtkIOImage import vtkNIFTIImageReader
from vtkmodules.vtkFiltersCore import vtkFlyingEdges3D
from vtkmodules.vtkCommonDataModel import vtkPointSet, vtkPolyData, vtkImageData
from vtkmodules.vtkCommonMath import vtkMatrix4x4
from vtkmodules.vtkCommonCore import vtkPoints, reference, vtkPoints, vtkIdList
from vtkmodules.vtkInteractionWidgets import vtkPointCloudRepresentation, vtkPointCloudWidget, vtkResliceCursorWidget, vtkResliceCursorLineRepresentation, vtkResliceCursor
from vtkmodules.vtkCommonTransforms import vtkMatrixToLinearTransform, vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter, vtkTransformFilter
from vtkmodules.vtkRenderingCore import vtkBillboardTextActor3D
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActorCollection,
    vtkTextActor,    
    vtkProperty,
    vtkCellPicker,
    vtkPointPicker,
    vtkPolyDataMapper,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkColorTransferFunction
)
from vtkmodules.vtkCommonExecutionModel import vtkAlgorithmOutput
from vtkmodules.util.numpy_support import vtk_to_numpy, numpy_to_vtk



from vtkmodules.vtkCommonColor import vtkNamedColors
colors = vtkNamedColors()
from vtkmodules.vtkFiltersCore import vtkFlyingEdges3D, vtkSmoothPolyDataFilter
from vtkmodules.vtkCommonTransforms import vtkMatrixToLinearTransform, vtkLinearTransform, vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter, vtkDiscreteFlyingEdges3D, vtkTransformFilter
from vtkmodules.vtkIOImage import vtkNIFTIImageReader
from vtkmodules.vtkCommonMath import vtkMatrix4x4
from vtkmodules.vtkIOGeometry import vtkSTLReader, vtkSTLWriter
from vtkmodules.vtkImagingCore import vtkImageThreshold, vtkImageMapToColors, vtkImageBlend
from vtkmodules.vtkCommonCore import vtkPoints

# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonCore import (
    VTK_VERSION_NUMBER,
    vtkVersion,
    vtkScalarsToColors,
    vtkLookupTable,
)
from vtkmodules.vtkCommonDataModel import (
    vtkDataObject,
    vtkDataSetAttributes
)
from vtkmodules.vtkFiltersCore import (
    vtkMaskFields,
    vtkThreshold,
    vtkWindowedSincPolyDataFilter
)
from vtkmodules.vtkFiltersGeneral import (
    vtkDiscreteFlyingEdges3D,
    vtkDiscreteMarchingCubes
)
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkIOXML import vtkXMLPolyDataWriter
from vtkmodules.vtkImagingStatistics import vtkImageAccumulate
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkImagingMorphological import vtkImageOpenClose3D


# PySide
from PySide6.QtGui import QWindow, QKeyEvent
from PySide6.QtCore import Qt
from PySide6.QtCore import Qt, Signal, Slot, QEvent, QObject
from PySide6.Qt3DInput import Qt3DInput 
from PySide6.QtWidgets import QApplication, QMainWindow, QGridLayout, QVBoxLayout, QWidget, QMdiSubWindow, QMdiArea, QDockWidget, QTreeWidgetItem, QTreeWidget, QLabel
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkInteractionImage import vtkImageViewer2, vtkResliceImageViewer, vtkResliceImageViewer 
from enum import Enum, IntFlag, auto
import numbers
import asyncio

from ..data.interface import DataManager, DataView 
from ..data.image import SkullEngineScan, SkullEngineMask


# class KeyFilter(QObject):
#     def eventFilter(self, obj, event):
#         if isinstance(event, QKeyEvent):
#             obj.parent().event(event)
#             return True
#         else:
#             # standard event processing
#             return super().eventFilter(obj, event)


# AXIAL = vtkResliceImageViewer.SLICE_ORIENTATION_XY
# CORONAL = vtkResliceImageViewer.SLICE_ORIENTATION_XZ
# SAGITTAL = vtkResliceImageViewer.SLICE_ORIENTATION_YZ



class QVTKRenderWindowInteractor(QVTKRenderWindowInteractor):
    
    def show(self):
        self.Initialize()
        self.GetRenderWindow().Render()
        self.Start()
        super().show()
        return None
    

    def closeEvent(self, QCloseEvent):
        self.Finalize()
        self.TerminateApp()
        super().closeEvent()
        return None



class QVTK3DWindow(QVTKRenderWindowInteractor):
    pass



class QVTKAxisAlignedWindow(QVTKRenderWindowInteractor):

    def __init__(self, parent=None, orientation=None, cursor=None, **kw):
        super().__init__(parent, **kw)
        if orientation is None:
            raise ValueError("must specify orientation")
        self.viewer = vtkResliceImageViewer()
        style = vtkInteractorStyleImage()
        self.SetInteractorStyle(style)
        self.GetRenderWindow().AddRenderer(self.viewer.GetRenderer())
        self.viewer.SetRenderWindow(self.GetRenderWindow())
        self.viewer.SetupInteractor(self)
        self.viewer.GetInteractorStyle().AutoAdjustCameraClippingRangeOn()
        self.viewer.GetInteractorStyle().SetDefaultRenderer(self.viewer.GetRenderer())
        self.viewer.SetResliceModeToAxisAligned()
        self.viewer.SetSliceOrientation(orientation)
        rep = vtk.vtkResliceCursorLineRepresentation.SafeDownCast( self.viewer.GetResliceCursorWidget().GetRepresentation())
        rep.GetResliceCursorActor().GetCursorAlgorithm().SetReslicePlaneNormal(orientation)
        return None
    

    def update_image(self, img):
        self.viewer.SetInputData(img)
        return None
    




class FourPaneWindow(QWidget, DataView):
    # this class is where all vtk events are handled
    # mode is controled by its parent on view hierarchy thru delegation
    # 
    reslice_signal = Signal(float, float, float)

    def __init__(self, *initargs):

        super().__init__(*initargs)

        self.reslice_signal.connect(self.reslice)


        self.image_picker = vtkCellPicker()
        self.image_picker.SetTolerance(.01)
        # three orthogonal views
        
        # sagittal
        self.iren_sagittal = QVTKAxisAlignedWindow(parent=self, orientation=vtkResliceImageViewer.SLICE_ORIENTATION_YZ)
        self.iren_sagittal.viewer.GetInteractorStyle().AddObserver('LeftButtonPressEvent', self.left_button_press_event_image)
        # self.iren_sagittal.viewer.GetInteractorStyle().AddObserver('MouseMoveEvent', self.left_button_move_event_image)

        # axial
        self.iren_axial = QVTKAxisAlignedWindow(parent=self, orientation=vtkResliceImageViewer.SLICE_ORIENTATION_XY)
        self.iren_axial.viewer.GetInteractorStyle().AddObserver('LeftButtonPressEvent', self.left_button_press_event_image)
        # self.iren_axial.viewer.GetInteractorStyle().AddObserver('MouseMoveEvent', self.left_button_move_event_image)

        # coronal
        self.iren_coronal = QVTKAxisAlignedWindow(parent=self, orientation=vtkResliceImageViewer.SLICE_ORIENTATION_XZ)
        self.iren_coronal.viewer.GetInteractorStyle().AddObserver('LeftButtonPressEvent', self.left_button_press_event_image)
        # self.iren_coronal.viewer.GetInteractorStyle().AddObserver('MouseMoveEvent', self.left_button_move_event_image)
        
        # 3d view
        self.iren_3d = QVTK3DWindow(parent=self)
        self.renderer_3d = vtkRenderer()
        self.renderer_3d.SetBackground(0.6863, 0.9333, 0.9333)
        self.iren_3d.GetRenderWindow().AddRenderer(self.renderer_3d)
        style = vtkInteractorStyleTrackballCamera()
        style.AutoAdjustCameraClippingRangeOn()
        style.SetDefaultRenderer(self.renderer_3d)
        self.iren_3d.SetInteractorStyle(style)

        cursor = self.iren_axial.viewer.GetResliceCursor()
        self.iren_coronal.viewer.SetResliceCursor(cursor)
        self.iren_sagittal.viewer.SetResliceCursor(cursor)

        # self.iren_axial.viewer.AddObserver(self.iren_axial.viewer.SliceChangedEvent, self.reslice)
        # self.iren_coronal.viewer.AddObserver(self.iren_coronal.viewer.SliceChangedEvent, self.reslice)
        # self.iren_sagittal.viewer.AddObserver(self.iren_sagittal.viewer.SliceChangedEvent, self.reslice)

        # self.iren_axial.viewer.GetResliceCursorWidget().AddObserver(vtkResliceCursorWidget.ResliceAxesChangedEvent, self.axis_changed)
        # self.iren_coronal.viewer.GetResliceCursorWidget().AddObserver(vtkResliceCursorWidget.ResliceAxesChangedEvent, self.axis_changed)
        # self.iren_sagittal.viewer.GetResliceCursorWidget().AddObserver(vtkResliceCursorWidget.ResliceAxesChangedEvent, self.axis_changed)


        self.data_reload() # this is to silent error from vtk before image is loaded

        # put 4 subviews on a 2x2 grid
        self.gridlayout = QGridLayout(parent=self)
        self.gridlayout.setContentsMargins(0,0,0,0)
        self.gridlayout.addWidget(self.iren_axial, 0, 0, 1, 1)
        self.gridlayout.addWidget(self.iren_sagittal, 0, 1, 1, 1)
        self.gridlayout.addWidget(self.iren_coronal, 1, 0, 1, 1)
        self.gridlayout.addWidget(self.iren_3d, 1, 1, 1, 1)
        return None
    

    def show(self):
        for v in self.children():
            if hasattr(v, 'show'):
                v.show()
        super().show()
        return None
    


    def get_image(self) -> vtkImageData:
        # blend scan with masks

        dm = self.get_data_manager()
        if dm is None or not dm.scan_is_loaded():
            return vtkImageData()
        
        img = dm.get_scan().vtk()

        # img_lut = vtkScalarsToColors()
        # img_lut.SetRange(img.GetScalarRange())

        img_lut = vtkLookupTable()
        img_lut.SetRange(img.GetScalarRange()) # image intensity range
        img_lut.SetValueRange(0.0, 1.0) # from bkg to white
        img_lut.SetSaturationRange(0.0, 0.0) # no color saturation
        img_lut.SetRampToLinear()
        img_lut.Build()

        img_rgb = vtkImageMapToColors()
        img_rgb.SetInputData(img)
        img_rgb.SetLookupTable(img_lut)
        img_rgb.SetOutputFormatToRGB()
        img_rgb.Update()

        msk = dm.get_mask().vtk()
        msk_lut = vtkColorTransferFunction()
        msk_lut.AddRGBPoint(0.,0.,0.,0.)
        msk_lut.AddRGBPoint(1.,1.,0.,0.)
        msk_lut.AddRGBPoint(2.,0.,1.,0.)
        msk_lut.AddRGBPoint(4.,0.,0.,1.)
        msk_lut.Build()

        msk_rgb = vtkImageMapToColors()
        msk_rgb.SetInputData(msk)
        msk_rgb.SetLookupTable(msk_lut)
        msk_rgb.SetOutputFormatToRGB()
        msk_rgb.PassAlphaToOutputOn()
        msk_rgb.Update()

        blender = vtkImageBlend()
        blender.AddInputConnection(img_rgb.GetOutputPort())
        blender.AddInputConnection(msk_rgb.GetOutputPort())
        blender.SetOpacity(0, 0.5)
        blender.SetOpacity(1, 0.5)
        blender.Update()
        self._img_blend = blender

        img = img_rgb.GetOutput()

        return blender.GetOutput()


    def data_update(self) -> None:
        if hasattr(self, '_img_blend'):
            self._img_blend.Update() # must have, updates imagedata for viewers
            self.iren_sagittal.viewer.Render()
            self.iren_axial.viewer.Render()
            self.iren_coronal.viewer.Render()
        


    def data_reload(self, *args, **kw) -> None:

        vtk_img = self.get_image()

        self.iren_sagittal.viewer.SetInputData(vtk_img)
        self.iren_axial.viewer.SetInputData(vtk_img)
        self.iren_coronal.viewer.SetInputData(vtk_img)
        self.reslice_signal.emit(*vtk_img.GetCenter())
        
        return None
    
    

    def left_button_press_event_image(self, obj:vtkInteractorStyleImage, event):

        if not self.get_data_manager().scan_is_loaded():
            print('scan not loaded')
            return None
        
        pos = obj.GetInteractor().GetEventPosition()
        self.image_picker.Pick(pos[0], pos[1], 0, obj.GetDefaultRenderer())
        if self.image_picker.GetCellId() >= 0:
            self.reslice_signal.emit(*self.image_picker.GetPickPosition())



    @Slot(float, float, float)
    def reslice(self, x, y, z):

        vtk_img = self.iren_sagittal.viewer.GetInput()
        if vtk_img:

            # three views must be resliced at the same time
            new_slice = [float('nan')]*3
            vtk_img.TransformPhysicalPointToContinuousIndex([x,y,z], new_slice)
            i,j,k = new_slice

            if i>=self.iren_sagittal.viewer.GetSliceMin() and i<=self.iren_sagittal.viewer.GetSliceMax():
                self.iren_sagittal.viewer.SetSlice(int(round(i)))
            if j>=self.iren_coronal.viewer.GetSliceMin() and j<=self.iren_coronal.viewer.GetSliceMax():
                self.iren_coronal.viewer.SetSlice(int(round(j)))
            if k>=self.iren_axial.viewer.GetSliceMin() and k<=self.iren_axial.viewer.GetSliceMax():
                self.iren_axial.viewer.SetSlice(int(round(k)))

        return None

