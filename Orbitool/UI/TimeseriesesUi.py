# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Orbitool\UI\Timeserieses.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(611, 416)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.layoutWidget_3 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.layoutWidget_3)
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.groupBox_2 = QtWidgets.QGroupBox(self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBox_2)
        self.formLayout_2.setContentsMargins(0, -1, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.mzRadioButton = QtWidgets.QRadioButton(self.groupBox_2)
        self.mzRadioButton.setChecked(True)
        self.mzRadioButton.setObjectName("mzRadioButton")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.mzRadioButton)
        self.formulaRadioButton = QtWidgets.QRadioButton(self.groupBox_2)
        self.formulaRadioButton.setObjectName("formulaRadioButton")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.formulaRadioButton)
        self.mzMaxDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mzMaxDoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.mzMaxDoubleSpinBox.setSizePolicy(sizePolicy)
        self.mzMaxDoubleSpinBox.setDecimals(5)
        self.mzMaxDoubleSpinBox.setMaximum(999.99)
        self.mzMaxDoubleSpinBox.setObjectName("mzMaxDoubleSpinBox")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.mzMaxDoubleSpinBox)
        self.mzMinDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mzMinDoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.mzMinDoubleSpinBox.setSizePolicy(sizePolicy)
        self.mzMinDoubleSpinBox.setDecimals(5)
        self.mzMinDoubleSpinBox.setMaximum(999.99)
        self.mzMinDoubleSpinBox.setObjectName("mzMinDoubleSpinBox")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.mzMinDoubleSpinBox)
        self.mzRangeRadioButton = QtWidgets.QRadioButton(self.groupBox_2)
        self.mzRangeRadioButton.setObjectName("mzRangeRadioButton")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.mzRangeRadioButton)
        self.mzDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mzDoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.mzDoubleSpinBox.setSizePolicy(sizePolicy)
        self.mzDoubleSpinBox.setDecimals(5)
        self.mzDoubleSpinBox.setMaximum(999.99)
        self.mzDoubleSpinBox.setObjectName("mzDoubleSpinBox")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.mzDoubleSpinBox)
        self.formulaLineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.formulaLineEdit.sizePolicy().hasHeightForWidth())
        self.formulaLineEdit.setSizePolicy(sizePolicy)
        self.formulaLineEdit.setObjectName("formulaLineEdit")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.formulaLineEdit)
        self.selectedMassListRadioButton = QtWidgets.QRadioButton(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectedMassListRadioButton.sizePolicy().hasHeightForWidth())
        self.selectedMassListRadioButton.setSizePolicy(sizePolicy)
        self.selectedMassListRadioButton.setChecked(False)
        self.selectedMassListRadioButton.setObjectName("selectedMassListRadioButton")
        self.formLayout_2.setWidget(9, QtWidgets.QFormLayout.SpanningRole, self.selectedMassListRadioButton)
        self.massListRadioButton = QtWidgets.QRadioButton(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.massListRadioButton.sizePolicy().hasHeightForWidth())
        self.massListRadioButton.setSizePolicy(sizePolicy)
        self.massListRadioButton.setObjectName("massListRadioButton")
        self.formLayout_2.setWidget(10, QtWidgets.QFormLayout.SpanningRole, self.massListRadioButton)
        self.selectedPeaksRadioButton = QtWidgets.QRadioButton(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectedPeaksRadioButton.sizePolicy().hasHeightForWidth())
        self.selectedPeaksRadioButton.setSizePolicy(sizePolicy)
        self.selectedPeaksRadioButton.setObjectName("selectedPeaksRadioButton")
        self.formLayout_2.setWidget(8, QtWidgets.QFormLayout.SpanningRole, self.selectedPeaksRadioButton)
        self.verticalLayout_17.addWidget(self.groupBox_2)
        self.formLayout_4 = QtWidgets.QFormLayout()
        self.formLayout_4.setObjectName("formLayout_4")
        self.label_22 = QtWidgets.QLabel(self.layoutWidget_3)
        self.label_22.setObjectName("label_22")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_22)
        self.rtolDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rtolDoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.rtolDoubleSpinBox.setSizePolicy(sizePolicy)
        self.rtolDoubleSpinBox.setMinimum(0.01)
        self.rtolDoubleSpinBox.setMaximum(9.99)
        self.rtolDoubleSpinBox.setProperty("value", 1.0)
        self.rtolDoubleSpinBox.setObjectName("rtolDoubleSpinBox")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.rtolDoubleSpinBox)
        self.verticalLayout_17.addLayout(self.formLayout_4)
        self.calcPushButton = QtWidgets.QPushButton(self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calcPushButton.sizePolicy().hasHeightForWidth())
        self.calcPushButton.setSizePolicy(sizePolicy)
        self.calcPushButton.setObjectName("calcPushButton")
        self.verticalLayout_17.addWidget(self.calcPushButton)
        self.tableWidget = QtWidgets.QTableWidget(self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_17.addWidget(self.tableWidget)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.label_23 = QtWidgets.QLabel(self.layoutWidget_3)
        self.label_23.setObjectName("label_23")
        self.horizontalLayout_16.addWidget(self.label_23)
        self.removeSelectedPushButton = QtWidgets.QPushButton(self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.removeSelectedPushButton.sizePolicy().hasHeightForWidth())
        self.removeSelectedPushButton.setSizePolicy(sizePolicy)
        self.removeSelectedPushButton.setObjectName("removeSelectedPushButton")
        self.horizontalLayout_16.addWidget(self.removeSelectedPushButton)
        self.removeAllPushButton = QtWidgets.QPushButton(self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.removeAllPushButton.sizePolicy().hasHeightForWidth())
        self.removeAllPushButton.setSizePolicy(sizePolicy)
        self.removeAllPushButton.setObjectName("removeAllPushButton")
        self.horizontalLayout_16.addWidget(self.removeAllPushButton)
        self.verticalLayout_17.addLayout(self.horizontalLayout_16)
        self.exportWithPpmCheckBox = QtWidgets.QCheckBox(self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exportWithPpmCheckBox.sizePolicy().hasHeightForWidth())
        self.exportWithPpmCheckBox.setSizePolicy(sizePolicy)
        self.exportWithPpmCheckBox.setObjectName("exportWithPpmCheckBox")
        self.verticalLayout_17.addWidget(self.exportWithPpmCheckBox)
        self.exportPushButton = QtWidgets.QPushButton(self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exportPushButton.sizePolicy().hasHeightForWidth())
        self.exportPushButton.setSizePolicy(sizePolicy)
        self.exportPushButton.setObjectName("exportPushButton")
        self.verticalLayout_17.addWidget(self.exportPushButton)
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.timeSeriesWidget = QtWidgets.QWidget(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timeSeriesWidget.sizePolicy().hasHeightForWidth())
        self.timeSeriesWidget.setSizePolicy(sizePolicy)
        self.timeSeriesWidget.setObjectName("timeSeriesWidget")
        self.verticalLayout_18.addWidget(self.timeSeriesWidget)
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.legendsCheckBox = QtWidgets.QCheckBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.legendsCheckBox.sizePolicy().hasHeightForWidth())
        self.legendsCheckBox.setSizePolicy(sizePolicy)
        self.legendsCheckBox.setObjectName("legendsCheckBox")
        self.horizontalLayout_24.addWidget(self.legendsCheckBox)
        self.logScaleCheckBox = QtWidgets.QCheckBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logScaleCheckBox.sizePolicy().hasHeightForWidth())
        self.logScaleCheckBox.setSizePolicy(sizePolicy)
        self.logScaleCheckBox.setObjectName("logScaleCheckBox")
        self.horizontalLayout_24.addWidget(self.logScaleCheckBox)
        self.rescalePushButton = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rescalePushButton.sizePolicy().hasHeightForWidth())
        self.rescalePushButton.setSizePolicy(sizePolicy)
        self.rescalePushButton.setObjectName("rescalePushButton")
        self.horizontalLayout_24.addWidget(self.rescalePushButton)
        self.verticalLayout_18.addLayout(self.horizontalLayout_24)
        self.verticalLayout.addWidget(self.splitter)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox_2.setTitle(_translate("Form", "Show time series at"))
        self.mzRadioButton.setText(_translate("Form", "mz"))
        self.formulaRadioButton.setText(_translate("Form", "formula"))
        self.mzRangeRadioButton.setText(_translate("Form", "mz range"))
        self.selectedMassListRadioButton.setText(_translate("Form", "mass list selected peak(s)"))
        self.massListRadioButton.setText(_translate("Form", "mass list all peaks"))
        self.selectedPeaksRadioButton.setText(_translate("Form", "selected peak(s) in peak list"))
        self.label_22.setText(_translate("Form", "<html><head/><body><p>rtol</p><p>when use mz,formula,peak</p></body></html>"))
        self.calcPushButton.setText(_translate("Form", "Calc time series"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "tag"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "mz"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "ppm"))
        self.label_23.setText(_translate("Form", "Remove"))
        self.removeSelectedPushButton.setText(_translate("Form", "selected"))
        self.removeAllPushButton.setText(_translate("Form", "all"))
        self.exportWithPpmCheckBox.setText(_translate("Form", "Export with text \"with ppm\""))
        self.exportPushButton.setText(_translate("Form", "Export time serieses"))
        self.legendsCheckBox.setText(_translate("Form", "legends"))
        self.logScaleCheckBox.setText(_translate("Form", "y-log scale"))
        self.rescalePushButton.setText(_translate("Form", "autoscale y axis"))

