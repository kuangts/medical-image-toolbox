# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'resample.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFormLayout, QGroupBox, QLabel, QLineEdit,
    QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(240, 320)
        Dialog.setModal(True)
        self.groupNewSpacing = QGroupBox(Dialog)
        self.groupNewSpacing.setObjectName(u"groupNewSpacing")
        self.groupNewSpacing.setGeometry(QRect(60, 30, 121, 101))
        self.groupNewSpacing.setFlat(False)
        self.layoutWidget = QWidget(self.groupNewSpacing)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(0, 20, 121, 76))
        self.formLayout = QFormLayout(self.layoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignBottom|Qt.AlignLeading|Qt.AlignLeft)
        self.formLayout.setFormAlignment(Qt.AlignBottom|Qt.AlignLeading|Qt.AlignLeft)
        self.formLayout.setContentsMargins(10, 0, 0, 0)
        self.x = QLabel(self.layoutWidget)
        self.x.setObjectName(u"x")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.x.sizePolicy().hasHeightForWidth())
        self.x.setSizePolicy(sizePolicy)
        self.x.setMinimumSize(QSize(20, 20))
        self.x.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.x)

        self.newx = QLineEdit(self.layoutWidget)
        self.newx.setObjectName(u"newx")
        sizePolicy.setHeightForWidth(self.newx.sizePolicy().hasHeightForWidth())
        self.newx.setSizePolicy(sizePolicy)
        self.newx.setMinimumSize(QSize(50, 0))

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.newx)

        self.y = QLabel(self.layoutWidget)
        self.y.setObjectName(u"y")
        sizePolicy.setHeightForWidth(self.y.sizePolicy().hasHeightForWidth())
        self.y.setSizePolicy(sizePolicy)
        self.y.setMinimumSize(QSize(20, 20))
        self.y.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.y)

        self.newy = QLineEdit(self.layoutWidget)
        self.newy.setObjectName(u"newy")
        sizePolicy.setHeightForWidth(self.newy.sizePolicy().hasHeightForWidth())
        self.newy.setSizePolicy(sizePolicy)
        self.newy.setMinimumSize(QSize(50, 0))

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.newy)

        self.z = QLabel(self.layoutWidget)
        self.z.setObjectName(u"z")
        sizePolicy.setHeightForWidth(self.z.sizePolicy().hasHeightForWidth())
        self.z.setSizePolicy(sizePolicy)
        self.z.setMinimumSize(QSize(20, 20))
        self.z.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.z)

        self.newz = QLineEdit(self.layoutWidget)
        self.newz.setObjectName(u"newz")
        sizePolicy.setHeightForWidth(self.newz.sizePolicy().hasHeightForWidth())
        self.newz.setSizePolicy(sizePolicy)
        self.newz.setMinimumSize(QSize(50, 0))

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.newz)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(40, 280, 164, 18))
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok|QDialogButtonBox.Reset)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.groupNewSpacing.setTitle(QCoreApplication.translate("Dialog", u"New spacing (pixel size)", None))
        self.x.setText(QCoreApplication.translate("Dialog", u"X", None))
        self.y.setText(QCoreApplication.translate("Dialog", u"Y", None))
        self.z.setText(QCoreApplication.translate("Dialog", u"Z", None))
    # retranslateUi

