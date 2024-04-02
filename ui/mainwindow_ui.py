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
        self.actionResampleParameters = QAction(MainWindow)
        self.actionResampleParameters.setObjectName(u"actionResampleParameters")
        self.actionResampleApply = QAction(MainWindow)
        self.actionResampleApply.setObjectName(u"actionResampleApply")
        self.actionConfigure = QAction(MainWindow)
        self.actionConfigure.setObjectName(u"actionConfigure")
        self.actionStart = QAction(MainWindow)
        self.actionStart.setObjectName(u"actionStart")
        self.fourpane = FourPaneWindow(MainWindow)
        self.fourpane.setObjectName(u"fourpane")
        MainWindow.setCentralWidget(self.fourpane)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QRect(0, 0, 800, 17))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuResample = QMenu(self.menubar)
        self.menuResample.setObjectName(u"menuResample")
        self.menuSegmentation = QMenu(self.menubar)
        self.menuSegmentation.setObjectName(u"menuSegmentation")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuResample.menuAction())
        self.menubar.addAction(self.menuSegmentation.menuAction())
        self.menuFile.addAction(self.actionOpenImage)
        self.menuFile.addAction(self.actionOpenMask)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSaveImage)
        self.menuFile.addAction(self.actionSaveMask)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuResample.addAction(self.actionResampleParameters)
        self.menuResample.addSeparator()
        self.menuResample.addAction(self.actionResampleApply)
        self.menuSegmentation.addAction(self.actionConfigure)
        self.menuSegmentation.addSeparator()
        self.menuSegmentation.addAction(self.actionStart)

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
        self.actionResampleParameters.setText(QCoreApplication.translate("MainWindow", u"Set Parameters", None))
        self.actionResampleApply.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
#if QT_CONFIG(shortcut)
        self.actionResampleApply.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+R", None))
#endif // QT_CONFIG(shortcut)
        self.actionConfigure.setText(QCoreApplication.translate("MainWindow", u"Configure", None))
        self.actionStart.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuResample.setTitle(QCoreApplication.translate("MainWindow", u"Resample", None))
        self.menuSegmentation.setTitle(QCoreApplication.translate("MainWindow", u"Segmentation", None))
    # retranslateUi

