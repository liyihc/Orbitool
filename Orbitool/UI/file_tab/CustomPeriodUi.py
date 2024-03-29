# Form implementation generated from reading ui file 'Orbitool\UI\file_tab\CustomPeriod.ui'
#
# Created by: PyQt6 UI code generator 6.5.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(628, 514)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtWidgets.QLabel(parent=Dialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(parent=Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.startDateTimeEdit = QtWidgets.QDateTimeEdit(parent=Dialog)
        self.startDateTimeEdit.setObjectName("startDateTimeEdit")
        self.gridLayout.addWidget(self.startDateTimeEdit, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(parent=Dialog)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 1, 2, 1, 1)
        self.endDateTimeEdit = QtWidgets.QDateTimeEdit(parent=Dialog)
        self.endDateTimeEdit.setObjectName("endDateTimeEdit")
        self.gridLayout.addWidget(self.endDateTimeEdit, 0, 3, 1, 1)
        self.numIntervalSpinBox = QtWidgets.QSpinBox(parent=Dialog)
        self.numIntervalSpinBox.setMaximum(9999)
        self.numIntervalSpinBox.setObjectName("numIntervalSpinBox")
        self.gridLayout.addWidget(self.numIntervalSpinBox, 1, 1, 1, 1)
        self.generateNumPeriodPushButton = QtWidgets.QPushButton(parent=Dialog)
        self.generateNumPeriodPushButton.setEnabled(True)
        self.generateNumPeriodPushButton.setObjectName("generateNumPeriodPushButton")
        self.gridLayout.addWidget(self.generateNumPeriodPushButton, 1, 3, 1, 1)
        self.label_7 = QtWidgets.QLabel(parent=Dialog)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 2, 0, 1, 1)
        self.timeIntervalLineEdit = QtWidgets.QLineEdit(parent=Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timeIntervalLineEdit.sizePolicy().hasHeightForWidth())
        self.timeIntervalLineEdit.setSizePolicy(sizePolicy)
        self.timeIntervalLineEdit.setObjectName("timeIntervalLineEdit")
        self.gridLayout.addWidget(self.timeIntervalLineEdit, 2, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(parent=Dialog)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 2, 2, 1, 1)
        self.generateTimePeriodPushButton = QtWidgets.QPushButton(parent=Dialog)
        self.generateTimePeriodPushButton.setObjectName("generateTimePeriodPushButton")
        self.gridLayout.addWidget(self.generateTimePeriodPushButton, 2, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.tableWidget = QtWidgets.QTableWidget(parent=Dialog)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.DoubleClicked|QtWidgets.QAbstractItemView.EditTrigger.EditKeyPressed)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.tableWidget)
        self.plotWidget = QtWidgets.QWidget(parent=Dialog)
        self.plotWidget.setMinimumSize(QtCore.QSize(0, 60))
        self.plotWidget.setMaximumSize(QtCore.QSize(16777215, 60))
        self.plotWidget.setObjectName("plotWidget")
        self.verticalLayout.addWidget(self.plotWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 16, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_10 = QtWidgets.QLabel(parent=Dialog)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout.addWidget(self.label_10)
        self.plotPositionHorizontalSlider = QtWidgets.QSlider(parent=Dialog)
        self.plotPositionHorizontalSlider.setMaximum(1)
        self.plotPositionHorizontalSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.plotPositionHorizontalSlider.setObjectName("plotPositionHorizontalSlider")
        self.horizontalLayout.addWidget(self.plotPositionHorizontalSlider)
        self.label_9 = QtWidgets.QLabel(parent=Dialog)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout.addWidget(self.label_9)
        self.plotFactorDoubleSpinBox = QtWidgets.QDoubleSpinBox(parent=Dialog)
        self.plotFactorDoubleSpinBox.setMinimum(0.01)
        self.plotFactorDoubleSpinBox.setStepType(QtWidgets.QAbstractSpinBox.StepType.AdaptiveDecimalStepType)
        self.plotFactorDoubleSpinBox.setProperty("value", 1.0)
        self.plotFactorDoubleSpinBox.setObjectName("plotFactorDoubleSpinBox")
        self.horizontalLayout.addWidget(self.plotFactorDoubleSpinBox)
        self.plotHideLabelCheckBox = QtWidgets.QCheckBox(parent=Dialog)
        self.plotHideLabelCheckBox.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.plotHideLabelCheckBox.setObjectName("plotHideLabelCheckBox")
        self.horizontalLayout.addWidget(self.plotHideLabelCheckBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(parent=Dialog)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.modifyLineEdit = QtWidgets.QLineEdit(parent=Dialog)
        self.modifyLineEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.modifyLineEdit.setObjectName("modifyLineEdit")
        self.horizontalLayout_2.addWidget(self.modifyLineEdit)
        self.label_3 = QtWidgets.QLabel(parent=Dialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.modifyStartPointsPushButton = QtWidgets.QPushButton(parent=Dialog)
        self.modifyStartPointsPushButton.setObjectName("modifyStartPointsPushButton")
        self.horizontalLayout_2.addWidget(self.modifyStartPointsPushButton)
        self.modifyEndPointsPushButton = QtWidgets.QPushButton(parent=Dialog)
        self.modifyEndPointsPushButton.setObjectName("modifyEndPointsPushButton")
        self.horizontalLayout_2.addWidget(self.modifyEndPointsPushButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.importPushButton = QtWidgets.QPushButton(parent=Dialog)
        self.importPushButton.setObjectName("importPushButton")
        self.horizontalLayout_2.addWidget(self.importPushButton)
        self.exportPushButton = QtWidgets.QPushButton(parent=Dialog)
        self.exportPushButton.setObjectName("exportPushButton")
        self.horizontalLayout_2.addWidget(self.exportPushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Orbitool - custom periods"))
        self.label_5.setText(_translate("Dialog", "every"))
        self.label.setText(_translate("Dialog", "from"))
        self.label_2.setText(_translate("Dialog", "to"))
        self.label_6.setText(_translate("Dialog", "spectra"))
        self.generateNumPeriodPushButton.setToolTip(_translate("Dialog", "coming soon"))
        self.generateNumPeriodPushButton.setText(_translate("Dialog", "generate by scan number"))
        self.label_7.setText(_translate("Dialog", "every"))
        self.timeIntervalLineEdit.setPlaceholderText(_translate("Dialog", "2h5m"))
        self.label_8.setText(_translate("Dialog", "minutes"))
        self.generateTimePeriodPushButton.setText(_translate("Dialog", "generate by time"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "start time/num"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "stop time/num"))
        self.label_10.setText(_translate("Dialog", "position"))
        self.label_9.setText(_translate("Dialog", "factor"))
        self.plotHideLabelCheckBox.setText(_translate("Dialog", "hide label"))
        self.label_4.setText(_translate("Dialog", "add"))
        self.modifyLineEdit.setToolTip(_translate("Dialog", "1000s ( 1000 seconds )\n"
"10m5s ( 10 minutes and 5 seconds )\n"
"1h ( 1 hour )"))
        self.modifyLineEdit.setPlaceholderText(_translate("Dialog", "-5m7s"))
        self.label_3.setText(_translate("Dialog", "to"))
        self.modifyStartPointsPushButton.setText(_translate("Dialog", "start points"))
        self.modifyEndPointsPushButton.setText(_translate("Dialog", "end points"))
        self.importPushButton.setText(_translate("Dialog", "Import"))
        self.exportPushButton.setText(_translate("Dialog", "Export"))
