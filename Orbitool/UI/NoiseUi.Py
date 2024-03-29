# Form implementation generated from reading ui file 'Orbitool\UI\Noise.ui'
#
# Created by: PyQt6 UI code generator 6.5.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(784, 461)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.splitter = QtWidgets.QSplitter(parent=Form)
        self.splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(parent=self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.showAveragePushButton = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.showAveragePushButton.setObjectName("showAveragePushButton")
        self.verticalLayout.addWidget(self.showAveragePushButton)
        self.toolBox = QtWidgets.QToolBox(parent=self.layoutWidget)
        self.toolBox.setMinimumSize(QtCore.QSize(285, 0))
        self.toolBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.toolBox.setBaseSize(QtCore.QSize(285, 0))
        self.toolBox.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.toolBox.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.toolBox.setObjectName("toolBox")
        self.noiseTool = QtWidgets.QWidget()
        self.noiseTool.setGeometry(QtCore.QRect(0, 0, 318, 271))
        self.noiseTool.setObjectName("noiseTool")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.noiseTool)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(parent=self.noiseTool)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label)
        self.quantileDoubleSpinBox = QtWidgets.QDoubleSpinBox(parent=self.noiseTool)
        self.quantileDoubleSpinBox.setProperty("value", 0.9)
        self.quantileDoubleSpinBox.setObjectName("quantileDoubleSpinBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.quantileDoubleSpinBox)
        self.label_2 = QtWidgets.QLabel(parent=self.noiseTool)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_2)
        self.nSigmaDoubleSpinBox = QtWidgets.QDoubleSpinBox(parent=self.noiseTool)
        self.nSigmaDoubleSpinBox.setProperty("value", 3.0)
        self.nSigmaDoubleSpinBox.setObjectName("nSigmaDoubleSpinBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.nSigmaDoubleSpinBox)
        self.line = QtWidgets.QFrame(parent=self.noiseTool)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.line)
        self.sizeDependentLabel = QtWidgets.QLabel(parent=self.noiseTool)
        self.sizeDependentLabel.setObjectName("sizeDependentLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.sizeDependentLabel)
        self.sizeDependentCheckBox = QtWidgets.QCheckBox(parent=self.noiseTool)
        self.sizeDependentCheckBox.setObjectName("sizeDependentCheckBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.sizeDependentCheckBox)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.groupBox_2 = QtWidgets.QGroupBox(parent=self.noiseTool)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.tableWidget = QtWidgets.QTableWidget(parent=self.groupBox_2)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
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
        self.verticalLayout_6.addWidget(self.tableWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.addPushButton = QtWidgets.QPushButton(parent=self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addPushButton.sizePolicy().hasHeightForWidth())
        self.addPushButton.setSizePolicy(sizePolicy)
        self.addPushButton.setObjectName("addPushButton")
        self.horizontalLayout.addWidget(self.addPushButton)
        self.delPushButton = QtWidgets.QPushButton(parent=self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.delPushButton.sizePolicy().hasHeightForWidth())
        self.delPushButton.setSizePolicy(sizePolicy)
        self.delPushButton.setObjectName("delPushButton")
        self.horizontalLayout.addWidget(self.delPushButton)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.calculateNoisePushButton = QtWidgets.QPushButton(parent=self.noiseTool)
        self.calculateNoisePushButton.setObjectName("calculateNoisePushButton")
        self.verticalLayout_2.addWidget(self.calculateNoisePushButton)
        self.toolBox.addItem(self.noiseTool, "")
        self.paramTool = QtWidgets.QWidget()
        self.paramTool.setGeometry(QtCore.QRect(0, 0, 242, 190))
        self.paramTool.setObjectName("paramTool")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.paramTool)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.paramTableWidget = QtWidgets.QTableWidget(parent=self.paramTool)
        self.paramTableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.paramTableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.paramTableWidget.setObjectName("paramTableWidget")
        self.paramTableWidget.setColumnCount(4)
        self.paramTableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.paramTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.paramTableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.paramTableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.paramTableWidget.setHorizontalHeaderItem(3, item)
        self.paramTableWidget.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_3.addWidget(self.paramTableWidget)
        self.recalculateNoisePushButton = QtWidgets.QPushButton(parent=self.paramTool)
        self.recalculateNoisePushButton.setObjectName("recalculateNoisePushButton")
        self.verticalLayout_3.addWidget(self.recalculateNoisePushButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.groupBox = QtWidgets.QGroupBox(parent=self.paramTool)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.exportDenoisedSpectrumPushButton = QtWidgets.QPushButton(parent=self.groupBox)
        self.exportDenoisedSpectrumPushButton.setObjectName("exportDenoisedSpectrumPushButton")
        self.horizontalLayout_4.addWidget(self.exportDenoisedSpectrumPushButton)
        self.exportNoisePeaksPushButton = QtWidgets.QPushButton(parent=self.groupBox)
        self.exportNoisePeaksPushButton.setObjectName("exportNoisePeaksPushButton")
        self.horizontalLayout_4.addWidget(self.exportNoisePeaksPushButton)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.toolBox.addItem(self.paramTool, "")
        self.verticalLayout.addWidget(self.toolBox)
        self.substractCheckBox = QtWidgets.QCheckBox(parent=self.layoutWidget)
        self.substractCheckBox.setObjectName("substractCheckBox")
        self.verticalLayout.addWidget(self.substractCheckBox)
        self.dependentCheckBox = QtWidgets.QCheckBox(parent=self.layoutWidget)
        self.dependentCheckBox.setChecked(True)
        self.dependentCheckBox.setObjectName("dependentCheckBox")
        self.verticalLayout.addWidget(self.dependentCheckBox)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.denoisePushButton = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.denoisePushButton.setObjectName("denoisePushButton")
        self.horizontalLayout_3.addWidget(self.denoisePushButton)
        self.skipPushButton = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.skipPushButton.setObjectName("skipPushButton")
        self.horizontalLayout_3.addWidget(self.skipPushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.layoutWidget1 = QtWidgets.QWidget(parent=self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.widget = QtWidgets.QWidget(parent=self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.verticalLayout_5.addWidget(self.widget)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.spectrumPushButton = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.spectrumPushButton.setObjectName("spectrumPushButton")
        self.horizontalLayout_6.addWidget(self.spectrumPushButton)
        self.label_10 = QtWidgets.QLabel(parent=self.layoutWidget1)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_6.addWidget(self.label_10)
        self.yLogCheckBox = QtWidgets.QCheckBox(parent=self.layoutWidget1)
        self.yLogCheckBox.setObjectName("yLogCheckBox")
        self.horizontalLayout_6.addWidget(self.yLogCheckBox)
        self.yAxisPushButton = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.yAxisPushButton.setObjectName("yAxisPushButton")
        self.horizontalLayout_6.addWidget(self.yAxisPushButton)
        self.yLimDoubleToolButton = QtWidgets.QToolButton(parent=self.layoutWidget1)
        self.yLimDoubleToolButton.setObjectName("yLimDoubleToolButton")
        self.horizontalLayout_6.addWidget(self.yLimDoubleToolButton)
        self.yLimHalfToolButton = QtWidgets.QToolButton(parent=self.layoutWidget1)
        self.yLimHalfToolButton.setObjectName("yLimHalfToolButton")
        self.horizontalLayout_6.addWidget(self.yLimHalfToolButton)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.verticalLayout_4.addWidget(self.splitter)

        self.retranslateUi(Form)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.showAveragePushButton.setText(_translate("Form", "show selected r&aw spectrum in spectra list"))
        self.showAveragePushButton.setShortcut(_translate("Form", "Alt+A"))
        self.label.setText(_translate("Form", "quantile"))
        self.label_2.setText(_translate("Form", "N sigma"))
        self.sizeDependentLabel.setText(_translate("Form", "size-dependent"))
        self.groupBox_2.setTitle(_translate("Form", "Noise for high-intensity peaks"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "formula"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "delta(integer)"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "mass"))
        self.addPushButton.setText(_translate("Form", "add"))
        self.delPushButton.setText(_translate("Form", "del"))
        self.calculateNoisePushButton.setText(_translate("Form", "&Calc noise for the selected spectrum"))
        self.calculateNoisePushButton.setShortcut(_translate("Form", "Alt+C"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.noiseTool), _translate("Form", "Noise inputs"))
        item = self.paramTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "enabled"))
        item = self.paramTableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "type"))
        item = self.paramTableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "noise"))
        item = self.paramTableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "LOD"))
        self.recalculateNoisePushButton.setText(_translate("Form", "&Recalulate noise"))
        self.recalculateNoisePushButton.setShortcut(_translate("Form", "Alt+R"))
        self.groupBox.setTitle(_translate("Form", "Export"))
        self.exportDenoisedSpectrumPushButton.setText(_translate("Form", "Denoised spectrum"))
        self.exportDenoisedSpectrumPushButton.setShortcut(_translate("Form", "Ctrl+Alt+D"))
        self.exportNoisePeaksPushButton.setText(_translate("Form", "Noise peaks"))
        self.exportNoisePeaksPushButton.setShortcut(_translate("Form", "Ctrl+Alt+N"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.paramTool), _translate("Form", "Noise results"))
        self.substractCheckBox.setText(_translate("Form", "Subtract noise level from peaks"))
        self.dependentCheckBox.setText(_translate("Form", "Spectrum-dependent params"))
        self.denoisePushButton.setText(_translate("Form", "denoise"))
        self.denoisePushButton.setShortcut(_translate("Form", "Return"))
        self.skipPushButton.setText(_translate("Form", "ski&p"))
        self.skipPushButton.setShortcut(_translate("Form", "Alt+P"))
        self.spectrumPushButton.setText(_translate("Form", "Scale to spectrum"))
        self.label_10.setText(_translate("Form", "y-lim"))
        self.yLogCheckBox.setText(_translate("Form", "log scale"))
        self.yAxisPushButton.setText(_translate("Form", "rescale"))
        self.yLimDoubleToolButton.setText(_translate("Form", "×2 (↑)"))
        self.yLimDoubleToolButton.setShortcut(_translate("Form", "Up"))
        self.yLimHalfToolButton.setText(_translate("Form", "÷2 (↓)"))
        self.yLimHalfToolButton.setShortcut(_translate("Form", "Down"))
