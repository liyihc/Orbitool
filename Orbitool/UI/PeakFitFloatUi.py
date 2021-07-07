# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Orbitool\UI\PeakFitFloat.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(474, 362)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_18 = QtWidgets.QLabel(Form)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_10.addWidget(self.label_18)
        self.originCheckBox = QtWidgets.QCheckBox(Form)
        self.originCheckBox.setChecked(True)
        self.originCheckBox.setObjectName("originCheckBox")
        self.horizontalLayout_10.addWidget(self.originCheckBox)
        self.sumCheckBox = QtWidgets.QCheckBox(Form)
        self.sumCheckBox.setChecked(True)
        self.sumCheckBox.setObjectName("sumCheckBox")
        self.horizontalLayout_10.addWidget(self.sumCheckBox)
        self.residualCheckBox = QtWidgets.QCheckBox(Form)
        self.residualCheckBox.setChecked(True)
        self.residualCheckBox.setObjectName("residualCheckBox")
        self.horizontalLayout_10.addWidget(self.residualCheckBox)
        self.legendCheckBox = QtWidgets.QCheckBox(Form)
        self.legendCheckBox.setChecked(True)
        self.legendCheckBox.setObjectName("legendCheckBox")
        self.horizontalLayout_10.addWidget(self.legendCheckBox)
        self.verticalLayout.addLayout(self.horizontalLayout_10)
        self.widget = QtWidgets.QWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(0, 0))
        self.widget.setObjectName("widget")
        self.verticalLayout.addWidget(self.widget)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.intensityTableWidget = QtWidgets.QTableWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.intensityTableWidget.sizePolicy().hasHeightForWidth())
        self.intensityTableWidget.setSizePolicy(sizePolicy)
        self.intensityTableWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.intensityTableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.intensityTableWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.intensityTableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.intensityTableWidget.setObjectName("intensityTableWidget")
        self.intensityTableWidget.setColumnCount(2)
        self.intensityTableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.intensityTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.intensityTableWidget.setHorizontalHeaderItem(1, item)
        self.intensityTableWidget.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_4.addWidget(self.intensityTableWidget)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_13 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_15.addWidget(self.label_13)
        self.spinBox = QtWidgets.QSpinBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox.sizePolicy().hasHeightForWidth())
        self.spinBox.setSizePolicy(sizePolicy)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(20)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout_15.addWidget(self.spinBox)
        self.verticalLayout_4.addLayout(self.horizontalLayout_15)
        self.refitPushButton = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refitPushButton.sizePolicy().hasHeightForWidth())
        self.refitPushButton.setSizePolicy(sizePolicy)
        self.refitPushButton.setObjectName("refitPushButton")
        self.verticalLayout_4.addWidget(self.refitPushButton)
        self.horizontalLayout_12.addLayout(self.verticalLayout_4)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.peaksTableWidget = QtWidgets.QTableWidget(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.peaksTableWidget.sizePolicy().hasHeightForWidth())
        self.peaksTableWidget.setSizePolicy(sizePolicy)
        self.peaksTableWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.peaksTableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.peaksTableWidget.setObjectName("peaksTableWidget")
        self.peaksTableWidget.setColumnCount(6)
        self.peaksTableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.peaksTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.peaksTableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.peaksTableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.peaksTableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.peaksTableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.peaksTableWidget.setHorizontalHeaderItem(5, item)
        self.peaksTableWidget.horizontalHeader().setDefaultSectionSize(70)
        self.peaksTableWidget.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_5.addWidget(self.peaksTableWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.closePushButton = QtWidgets.QPushButton(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.closePushButton.sizePolicy().hasHeightForWidth())
        self.closePushButton.setSizePolicy(sizePolicy)
        self.closePushButton.setObjectName("closePushButton")
        self.horizontalLayout.addWidget(self.closePushButton)
        self.savePushButton = QtWidgets.QPushButton(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.savePushButton.sizePolicy().hasHeightForWidth())
        self.savePushButton.setSizePolicy(sizePolicy)
        self.savePushButton.setObjectName("savePushButton")
        self.horizontalLayout.addWidget(self.savePushButton)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.horizontalLayout_12.addWidget(self.groupBox_2)
        self.verticalLayout.addLayout(self.horizontalLayout_12)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_18.setText(_translate("Form", "show"))
        self.originCheckBox.setText(_translate("Form", "origin"))
        self.sumCheckBox.setText(_translate("Form", "sum"))
        self.residualCheckBox.setText(_translate("Form", "residual"))
        self.legendCheckBox.setText(_translate("Form", "legend"))
        item = self.intensityTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "mz"))
        item = self.intensityTableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "intensity"))
        self.label_13.setText(_translate("Form", "peak num"))
        self.refitPushButton.setText(_translate("Form", "Re-fit"))
        self.groupBox_2.setTitle(_translate("Form", "Peaks"))
        item = self.peaksTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "formula"))
        item = self.peaksTableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "position"))
        item = self.peaksTableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "intensity"))
        item = self.peaksTableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "ppm"))
        item = self.peaksTableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "isotope ratio"))
        item = self.peaksTableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Form", "ref ratio"))
        self.closePushButton.setText(_translate("Form", "Close"))
        self.savePushButton.setText(_translate("Form", "Save"))

