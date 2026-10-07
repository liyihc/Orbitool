# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MassDefect.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDoubleSpinBox, QFormLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QRadioButton, QSizePolicy, QSlider,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(719, 590)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.verticalLayout_24 = QVBoxLayout()
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.formLayout_3 = QFormLayout(self.groupBox)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.elementRadioButton = QRadioButton(self.groupBox)
        self.elementRadioButton.setObjectName(u"elementRadioButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.elementRadioButton.sizePolicy().hasHeightForWidth())
        self.elementRadioButton.setSizePolicy(sizePolicy1)

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.LabelRole, self.elementRadioButton)

        self.elementLineEdit = QLineEdit(self.groupBox)
        self.elementLineEdit.setObjectName(u"elementLineEdit")
        sizePolicy1.setHeightForWidth(self.elementLineEdit.sizePolicy().hasHeightForWidth())
        self.elementLineEdit.setSizePolicy(sizePolicy1)

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.FieldRole, self.elementLineEdit)

        self.dbeRadioButton = QRadioButton(self.groupBox)
        self.dbeRadioButton.setObjectName(u"dbeRadioButton")
        sizePolicy1.setHeightForWidth(self.dbeRadioButton.sizePolicy().hasHeightForWidth())
        self.dbeRadioButton.setSizePolicy(sizePolicy1)
        self.dbeRadioButton.setChecked(True)

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.SpanningRole, self.dbeRadioButton)

        self.calcPushButton = QPushButton(self.groupBox)
        self.calcPushButton.setObjectName(u"calcPushButton")
        sizePolicy1.setHeightForWidth(self.calcPushButton.sizePolicy().hasHeightForWidth())
        self.calcPushButton.setSizePolicy(sizePolicy1)

        self.formLayout_3.setWidget(3, QFormLayout.ItemRole.SpanningRole, self.calcPushButton)

        self.atomsRadioButton = QRadioButton(self.groupBox)
        self.atomsRadioButton.setObjectName(u"atomsRadioButton")

        self.formLayout_3.setWidget(2, QFormLayout.ItemRole.SpanningRole, self.atomsRadioButton)


        self.verticalLayout_24.addWidget(self.groupBox)


        self.horizontalLayout_6.addLayout(self.verticalLayout_24)

        self.verticalLayout_22 = QVBoxLayout()
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.showGreyCheckBox = QCheckBox(Form)
        self.showGreyCheckBox.setObjectName(u"showGreyCheckBox")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.showGreyCheckBox)

        self.logCheckBox = QCheckBox(Form)
        self.logCheckBox.setObjectName(u"logCheckBox")
        sizePolicy1.setHeightForWidth(self.logCheckBox.sizePolicy().hasHeightForWidth())
        self.logCheckBox.setSizePolicy(sizePolicy1)
        self.logCheckBox.setChecked(True)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.logCheckBox)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label)

        self.transparencyDoubleSpinBox = QDoubleSpinBox(Form)
        self.transparencyDoubleSpinBox.setObjectName(u"transparencyDoubleSpinBox")
        self.transparencyDoubleSpinBox.setMaximum(1.000000000000000)
        self.transparencyDoubleSpinBox.setSingleStep(0.100000000000000)
        self.transparencyDoubleSpinBox.setValue(0.300000000000000)

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.transparencyDoubleSpinBox)


        self.verticalLayout_22.addLayout(self.formLayout_2)

        self.formLayout_8 = QFormLayout()
        self.formLayout_8.setObjectName(u"formLayout_8")
        self.label_14 = QLabel(Form)
        self.label_14.setObjectName(u"label_14")

        self.formLayout_8.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_14)

        self.minSizeHorizontalSlider = QSlider(Form)
        self.minSizeHorizontalSlider.setObjectName(u"minSizeHorizontalSlider")
        self.minSizeHorizontalSlider.setMinimum(-10)
        self.minSizeHorizontalSlider.setMaximum(70)
        self.minSizeHorizontalSlider.setValue(-10)
        self.minSizeHorizontalSlider.setOrientation(Qt.Horizontal)

        self.formLayout_8.setWidget(0, QFormLayout.ItemRole.FieldRole, self.minSizeHorizontalSlider)

        self.label_15 = QLabel(Form)
        self.label_15.setObjectName(u"label_15")

        self.formLayout_8.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_15)

        self.maxSizeHorizontalSlider = QSlider(Form)
        self.maxSizeHorizontalSlider.setObjectName(u"maxSizeHorizontalSlider")
        self.maxSizeHorizontalSlider.setMinimum(-10)
        self.maxSizeHorizontalSlider.setMaximum(70)
        self.maxSizeHorizontalSlider.setPageStep(5)
        self.maxSizeHorizontalSlider.setValue(25)
        self.maxSizeHorizontalSlider.setOrientation(Qt.Horizontal)

        self.formLayout_8.setWidget(1, QFormLayout.ItemRole.FieldRole, self.maxSizeHorizontalSlider)


        self.verticalLayout_22.addLayout(self.formLayout_8)


        self.horizontalLayout_6.addLayout(self.verticalLayout_22)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy2)

        self.verticalLayout.addWidget(self.widget)

        self.exportPushButton = QPushButton(Form)
        self.exportPushButton.setObjectName(u"exportPushButton")

        self.verticalLayout.addWidget(self.exportPushButton)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Color", None))
        self.elementRadioButton.setText(QCoreApplication.translate("Form", u"Element", None))
        self.dbeRadioButton.setText(QCoreApplication.translate("Form", u"DBE", None))
        self.calcPushButton.setText(QCoreApplication.translate("Form", u"calc mass defect", None))
        self.atomsRadioButton.setText(QCoreApplication.translate("Form", u"Atoms type", None))
        self.showGreyCheckBox.setText(QCoreApplication.translate("Form", u"show peak without formula", None))
        self.logCheckBox.setText(QCoreApplication.translate("Form", u"log intensity", None))
        self.label.setText(QCoreApplication.translate("Form", u"transparency", None))
        self.label_14.setText(QCoreApplication.translate("Form", u"min size", None))
        self.label_15.setText(QCoreApplication.translate("Form", u"max size", None))
        self.exportPushButton.setText(QCoreApplication.translate("Form", u"Export", None))
    # retranslateUi

