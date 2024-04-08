# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QStatusBar, QWidget)

from .fourpane import FourPaneWindow

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionOpenImage = QAction(MainWindow)
        self.actionOpenImage.setObjectName(u"actionOpenImage")
        self.actionOpenMask = QAction(MainWindow)
        self.actionOpenMask.setObjectName(u"actionOpenMask")
        self.actionSaveImage = QAction(MainWindow)
        self.actionSaveImage.setObjectName(u"actionSaveImage")
        self.actionSaveMask = QAction(MainWindow)
        self.actionSaveMask.setObjectName(u"actionSaveMask")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionConfSeg = QAction(MainWindow)
        self.actionConfSeg.setObjectName(u"actionConfSeg")
        self.actionStartSeg = QAction(MainWindow)
        self.actionStartSeg.setObjectName(u"actionStartSeg")
        self.actionSetOrigin = QAction(MainWindow)
        self.actionSetOrigin.setObjectName(u"actionSetOrigin")
        self.actionEraseMeta = QAction(MainWindow)
        self.actionEraseMeta.setObjectName(u"actionEraseMeta")
        self.actionResample = QAction(MainWindow)
        self.actionResample.setObjectName(u"actionResample")
        self.actionTransform = QAction(MainWindow)
        self.actionTransform.setObjectName(u"actionTransform")
        self.fourpane = FourPaneWindow(MainWindow)
        self.fourpane.setObjectName(u"fourpane")
        MainWindow.setCentralWidget(self.fourpane)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QRect(0, 0, 800, 17))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuSegmentation = QMenu(self.menubar)
        self.menuSegmentation.setObjectName(u"menuSegmentation")
        self.menuImage = QMenu(self.menubar)
        self.menuImage.setObjectName(u"menuImage")
        self.menu3D_Model = QMenu(self.menubar)
        self.menu3D_Model.setObjectName(u"menu3D_Model")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuImage.menuAction())
        self.menubar.addAction(self.menuSegmentation.menuAction())
        self.menubar.addAction(self.menu3D_Model.menuAction())
        self.menuFile.addAction(self.actionOpenImage)
        self.menuFile.addAction(self.actionOpenMask)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSaveImage)
        self.menuFile.addAction(self.actionSaveMask)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuSegmentation.addAction(self.actionConfSeg)
        self.menuSegmentation.addSeparator()
        self.menuSegmentation.addAction(self.actionStartSeg)
        self.menuImage.addAction(self.actionSetOrigin)
        self.menuImage.addAction(self.actionEraseMeta)
        self.menuImage.addAction(self.actionResample)
        self.menu3D_Model.addAction(self.actionTransform)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpenImage.setText(QCoreApplication.translate("MainWindow", u"Open Image", None))
#if QT_CONFIG(shortcut)
        self.actionOpenImage.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionOpenMask.setText(QCoreApplication.translate("MainWindow", u"Open Mask", None))
#if QT_CONFIG(shortcut)
        self.actionOpenMask.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionSaveImage.setText(QCoreApplication.translate("MainWindow", u"Save Image", None))
#if QT_CONFIG(shortcut)
        self.actionSaveImage.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionSaveMask.setText(QCoreApplication.translate("MainWindow", u"Save Mask", None))
#if QT_CONFIG(shortcut)
        self.actionSaveMask.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionConfSeg.setText(QCoreApplication.translate("MainWindow", u"Configure", None))
#if QT_CONFIG(tooltip)
        self.actionConfSeg.setToolTip(QCoreApplication.translate("MainWindow", u"Configure remote server for automatic segmentation", None))
#endif // QT_CONFIG(tooltip)
        self.actionStartSeg.setText(QCoreApplication.translate("MainWindow", u"Start", None))
#if QT_CONFIG(tooltip)
        self.actionStartSeg.setToolTip(QCoreApplication.translate("MainWindow", u"Start automatic segmentation", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionStartSeg.setShortcut(QCoreApplication.translate("MainWindow", u"S", None))
#endif // QT_CONFIG(shortcut)
        self.actionSetOrigin.setText(QCoreApplication.translate("MainWindow", u"Set Origin", None))
#if QT_CONFIG(tooltip)
        self.actionSetOrigin.setToolTip(QCoreApplication.translate("MainWindow", u"Translating the image by setting a new origin", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionSetOrigin.setShortcut(QCoreApplication.translate("MainWindow", u"O", None))
#endif // QT_CONFIG(shortcut)
        self.actionEraseMeta.setText(QCoreApplication.translate("MainWindow", u"Erase Metadata", None))
#if QT_CONFIG(tooltip)
        self.actionEraseMeta.setToolTip(QCoreApplication.translate("MainWindow", u"Remove all metadata associated with the image (including patient health information)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionEraseMeta.setShortcut(QCoreApplication.translate("MainWindow", u"D", None))
#endif // QT_CONFIG(shortcut)
        self.actionResample.setText(QCoreApplication.translate("MainWindow", u"Resample", None))
#if QT_CONFIG(shortcut)
        self.actionResample.setShortcut(QCoreApplication.translate("MainWindow", u"R", None))
#endif // QT_CONFIG(shortcut)
        self.actionTransform.setText(QCoreApplication.translate("MainWindow", u"Transform", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuSegmentation.setTitle(QCoreApplication.translate("MainWindow", u"Segmentation", None))
        self.menuImage.setTitle(QCoreApplication.translate("MainWindow", u"Image", None))
        self.menu3D_Model.setTitle(QCoreApplication.translate("MainWindow", u"3D Model", None))
    # retranslateUi

