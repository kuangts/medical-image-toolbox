# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'origin.ui'
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
        self.groupOrigin = QGroupBox(Dialog)
        self.groupOrigin.setObjectName(u"groupOrigin")
        self.groupOrigin.setGeometry(QRect(60, 30, 121, 101))
        self.groupOrigin.setFlat(False)
        self.layoutWidget = QWidget(self.groupOrigin)
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

        self.groupTranslation = QGroupBox(Dialog)
        self.groupTranslation.setObjectName(u"groupTranslation")
        self.groupTranslation.setGeometry(QRect(60, 150, 121, 101))
        self.groupTranslation.setLayoutDirection(Qt.LeftToRight)
        self.layoutWidget1 = QWidget(self.groupTranslation)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(0, 20, 121, 76))
        self.formLayout_3 = QFormLayout(self.layoutWidget1)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.formLayout_3.setLabelAlignment(Qt.AlignBottom|Qt.AlignLeading|Qt.AlignLeft)
        self.formLayout_3.setFormAlignment(Qt.AlignBottom|Qt.AlignLeading|Qt.AlignLeft)
        self.formLayout_3.setContentsMargins(10, 0, 0, 0)
        self.dx = QLabel(self.layoutWidget1)
        self.dx.setObjectName(u"dx")
        sizePolicy.setHeightForWidth(self.dx.sizePolicy().hasHeightForWidth())
        self.dx.setSizePolicy(sizePolicy)
        self.dx.setMinimumSize(QSize(20, 20))
        self.dx.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.dx)

        self.newdx = QLineEdit(self.layoutWidget1)
        self.newdx.setObjectName(u"newdx")
        sizePolicy.setHeightForWidth(self.newdx.sizePolicy().hasHeightForWidth())
        self.newdx.setSizePolicy(sizePolicy)
        self.newdx.setMinimumSize(QSize(50, 0))

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.newdx)

        self.dy = QLabel(self.layoutWidget1)
        self.dy.setObjectName(u"dy")
        sizePolicy.setHeightForWidth(self.dy.sizePolicy().hasHeightForWidth())
        self.dy.setSizePolicy(sizePolicy)
        self.dy.setMinimumSize(QSize(20, 20))
        self.dy.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.dy)

        self.newdy = QLineEdit(self.layoutWidget1)
        self.newdy.setObjectName(u"newdy")
        sizePolicy.setHeightForWidth(self.newdy.sizePolicy().hasHeightForWidth())
        self.newdy.setSizePolicy(sizePolicy)
        self.newdy.setMinimumSize(QSize(50, 0))

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.newdy)

        self.dz = QLabel(self.layoutWidget1)
        self.dz.setObjectName(u"dz")
        sizePolicy.setHeightForWidth(self.dz.sizePolicy().hasHeightForWidth())
        self.dz.setSizePolicy(sizePolicy)
        self.dz.setMinimumSize(QSize(20, 20))
        self.dz.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.dz)

        self.newdz = QLineEdit(self.layoutWidget1)
        self.newdz.setObjectName(u"newdz")
        sizePolicy.setHeightForWidth(self.newdz.sizePolicy().hasHeightForWidth())
        self.newdz.setSizePolicy(sizePolicy)
        self.newdz.setMinimumSize(QSize(50, 0))

        self.formLayout_3.setWidget(2, QFormLayout.FieldRole, self.newdz)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(40, 280, 164, 18))
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok|QDialogButtonBox.Reset)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.groupOrigin.setTitle(QCoreApplication.translate("Dialog", u"New Origin", None))
        self.x.setText(QCoreApplication.translate("Dialog", u"X", None))
        self.y.setText(QCoreApplication.translate("Dialog", u"Y", None))
        self.z.setText(QCoreApplication.translate("Dialog", u"Z", None))
        self.groupTranslation.setTitle(QCoreApplication.translate("Dialog", u"Translation", None))
        self.dx.setText(QCoreApplication.translate("Dialog", u"DX", None))
        self.newdx.setText("")
        self.dy.setText(QCoreApplication.translate("Dialog", u"DY", None))
        self.newdy.setText("")
        self.dz.setText(QCoreApplication.translate("Dialog", u"DZ", None))
        self.newdz.setText("")
    # retranslateUi

