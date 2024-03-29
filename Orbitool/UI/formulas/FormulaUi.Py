# Form implementation generated from reading ui file 'Orbitool\UI\Formula.ui'
#
# Created by: PyQt6 UI code generator 6.5.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(300, 650)
        Form.setMinimumSize(QtCore.QSize(300, 0))
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(parent=Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 265, 732))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.mzMinDoubleSpinBox = QtWidgets.QDoubleSpinBox(parent=self.scrollAreaWidgetContents)
        self.mzMinDoubleSpinBox.setMaximum(9999.99)
        self.mzMinDoubleSpinBox.setObjectName("mzMinDoubleSpinBox")
        self.horizontalLayout_3.addWidget(self.mzMinDoubleSpinBox)
        self.label_2 = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.mzMaxDoubleSpinBox = QtWidgets.QDoubleSpinBox(parent=self.scrollAreaWidgetContents)
        self.mzMaxDoubleSpinBox.setMaximum(9999.99)
        self.mzMaxDoubleSpinBox.setObjectName("mzMaxDoubleSpinBox")
        self.horizontalLayout_3.addWidget(self.mzMaxDoubleSpinBox)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setObjectName("formLayout_3")
        self.chargeLabel = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        self.chargeLabel.setObjectName("chargeLabel")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.chargeLabel)
        self.chargeSpinBox = QtWidgets.QSpinBox(parent=self.scrollAreaWidgetContents)
        self.chargeSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.chargeSpinBox.setMinimum(-99)
        self.chargeSpinBox.setObjectName("chargeSpinBox")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.chargeSpinBox)
        self.tolerancePpmLabel = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        self.tolerancePpmLabel.setObjectName("tolerancePpmLabel")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.tolerancePpmLabel)
        self.rtolDoubleSpinBox = QtWidgets.QDoubleSpinBox(parent=self.scrollAreaWidgetContents)
        self.rtolDoubleSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.rtolDoubleSpinBox.setObjectName("rtolDoubleSpinBox")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.rtolDoubleSpinBox)
        self.globalLimitLabel = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        self.globalLimitLabel.setObjectName("globalLimitLabel")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.globalLimitLabel)
        self.globalLimitSpinBox = QtWidgets.QSpinBox(parent=self.scrollAreaWidgetContents)
        self.globalLimitSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.globalLimitSpinBox.setObjectName("globalLimitSpinBox")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.globalLimitSpinBox)
        self.verticalLayout_4.addLayout(self.formLayout_3)
        self.groupBox_2 = QtWidgets.QGroupBox(parent=self.scrollAreaWidgetContents)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.nitrogenRuleCheckBox = QtWidgets.QCheckBox(parent=self.groupBox_2)
        self.nitrogenRuleCheckBox.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.nitrogenRuleCheckBox.setObjectName("nitrogenRuleCheckBox")
        self.verticalLayout_5.addWidget(self.nitrogenRuleCheckBox)
        self.dbeLimitCheckBox = QtWidgets.QCheckBox(parent=self.groupBox_2)
        self.dbeLimitCheckBox.setObjectName("dbeLimitCheckBox")
        self.verticalLayout_5.addWidget(self.dbeLimitCheckBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_5 = QtWidgets.QLabel(parent=self.groupBox_2)
        self.label_5.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_5.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.dbeMinDoubleSpinBox = QtWidgets.QDoubleSpinBox(parent=self.groupBox_2)
        self.dbeMinDoubleSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.dbeMinDoubleSpinBox.setMinimum(-99.0)
        self.dbeMinDoubleSpinBox.setObjectName("dbeMinDoubleSpinBox")
        self.horizontalLayout.addWidget(self.dbeMinDoubleSpinBox)
        self.label_4 = QtWidgets.QLabel(parent=self.groupBox_2)
        self.label_4.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.dbeMaxDoubleSpinBox = QtWidgets.QDoubleSpinBox(parent=self.groupBox_2)
        self.dbeMaxDoubleSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.dbeMaxDoubleSpinBox.setMinimum(-99.0)
        self.dbeMaxDoubleSpinBox.setObjectName("dbeMaxDoubleSpinBox")
        self.horizontalLayout.addWidget(self.dbeMaxDoubleSpinBox)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.verticalLayout_4.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(parent=self.scrollAreaWidgetContents)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.isotopeTreeWidget = QtWidgets.QTreeWidget(parent=self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.isotopeTreeWidget.sizePolicy().hasHeightForWidth())
        self.isotopeTreeWidget.setSizePolicy(sizePolicy)
        self.isotopeTreeWidget.setMinimumSize(QtCore.QSize(0, 200))
        self.isotopeTreeWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.isotopeTreeWidget.setExpandsOnDoubleClick(False)
        self.isotopeTreeWidget.setObjectName("isotopeTreeWidget")
        self.isotopeTreeWidget.header().setVisible(True)
        self.isotopeTreeWidget.header().setCascadingSectionResizes(False)
        self.isotopeTreeWidget.header().setDefaultSectionSize(55)
        self.isotopeTreeWidget.header().setMinimumSectionSize(40)
        self.isotopeTreeWidget.header().setSortIndicatorShown(False)
        self.verticalLayout_2.addWidget(self.isotopeTreeWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.isotopeLineEdit = QtWidgets.QLineEdit(parent=self.groupBox_3)
        self.isotopeLineEdit.setObjectName("isotopeLineEdit")
        self.horizontalLayout_2.addWidget(self.isotopeLineEdit)
        self.isotopeAddToolButton = QtWidgets.QToolButton(parent=self.groupBox_3)
        self.isotopeAddToolButton.setMaximumSize(QtCore.QSize(20, 20))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.ButtonText, brush)
        self.isotopeAddToolButton.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.isotopeAddToolButton.setFont(font)
        self.isotopeAddToolButton.setObjectName("isotopeAddToolButton")
        self.horizontalLayout_2.addWidget(self.isotopeAddToolButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_4.addWidget(self.groupBox_3)
        self.groupBox_4 = QtWidgets.QGroupBox(parent=self.scrollAreaWidgetContents)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.elementShowPushButton = QtWidgets.QPushButton(parent=self.groupBox_4)
        self.elementShowPushButton.setObjectName("elementShowPushButton")
        self.horizontalLayout_5.addWidget(self.elementShowPushButton)
        self.elementHidePushButton = QtWidgets.QPushButton(parent=self.groupBox_4)
        self.elementHidePushButton.setObjectName("elementHidePushButton")
        self.horizontalLayout_5.addWidget(self.elementHidePushButton)
        self.verticalLayout_8.addLayout(self.horizontalLayout_5)
        self.elementTableWidget = QtWidgets.QTableWidget(parent=self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.elementTableWidget.sizePolicy().hasHeightForWidth())
        self.elementTableWidget.setSizePolicy(sizePolicy)
        self.elementTableWidget.setMinimumSize(QtCore.QSize(0, 150))
        self.elementTableWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.elementTableWidget.setBaseSize(QtCore.QSize(0, 0))
        self.elementTableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.elementTableWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.elementTableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.elementTableWidget.setObjectName("elementTableWidget")
        self.elementTableWidget.setColumnCount(8)
        self.elementTableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.elementTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.elementTableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.elementTableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.elementTableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.elementTableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.elementTableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.elementTableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.elementTableWidget.setHorizontalHeaderItem(7, item)
        self.elementTableWidget.horizontalHeader().setDefaultSectionSize(60)
        self.elementTableWidget.horizontalHeader().setMinimumSectionSize(40)
        self.elementTableWidget.horizontalHeader().setStretchLastSection(True)
        self.elementTableWidget.verticalHeader().setVisible(False)
        self.verticalLayout_8.addWidget(self.elementTableWidget)
        self.horizontalLayout_30 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_30.setObjectName("horizontalLayout_30")
        self.elementLineEdit = QtWidgets.QLineEdit(parent=self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.elementLineEdit.sizePolicy().hasHeightForWidth())
        self.elementLineEdit.setSizePolicy(sizePolicy)
        self.elementLineEdit.setObjectName("elementLineEdit")
        self.horizontalLayout_30.addWidget(self.elementLineEdit)
        self.elementAddToolButton = QtWidgets.QToolButton(parent=self.groupBox_4)
        self.elementAddToolButton.setMaximumSize(QtCore.QSize(20, 20))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.ButtonText, brush)
        self.elementAddToolButton.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.elementAddToolButton.setFont(font)
        self.elementAddToolButton.setObjectName("elementAddToolButton")
        self.horizontalLayout_30.addWidget(self.elementAddToolButton)
        self.verticalLayout_8.addLayout(self.horizontalLayout_30)
        self.verticalLayout_4.addWidget(self.groupBox_4)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.groupBox = QtWidgets.QGroupBox(parent=Form)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.inputLineEdit = QtWidgets.QLineEdit(parent=self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inputLineEdit.sizePolicy().hasHeightForWidth())
        self.inputLineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.inputLineEdit.setFont(font)
        self.inputLineEdit.setObjectName("inputLineEdit")
        self.horizontalLayout_4.addWidget(self.inputLineEdit)
        self.calcPushButton = QtWidgets.QPushButton(parent=self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calcPushButton.sizePolicy().hasHeightForWidth())
        self.calcPushButton.setSizePolicy(sizePolicy)
        self.calcPushButton.setMaximumSize(QtCore.QSize(40, 16777215))
        self.calcPushButton.setObjectName("calcPushButton")
        self.horizontalLayout_4.addWidget(self.calcPushButton)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "mz min"))
        self.label_2.setText(_translate("Form", "mz max"))
        self.chargeLabel.setText(_translate("Form", "charge"))
        self.tolerancePpmLabel.setText(_translate("Form", "tolerance(ppm)"))
        self.globalLimitLabel.setToolTip(_translate("Form", "<html><head/><body><p>In the calculation, the sum of isotopes marked with &quot;global limit&quot; will not exceed this value</p></body></html>"))
        self.globalLimitLabel.setText(_translate("Form", "global limit"))
        self.groupBox_2.setTitle(_translate("Form", "DBE limit"))
        self.nitrogenRuleCheckBox.setToolTip(_translate("Form", "the restriction that DBE must be an integer"))
        self.nitrogenRuleCheckBox.setText(_translate("Form", "enable Nitrogen Rule"))
        self.dbeLimitCheckBox.setToolTip(_translate("Form", "DBE range limit and O and H quantity limit. Please check the instruction manual for the specific calculation method.\n"
"You can update the DBE of the element and the attributes that affect the number of O and H in the \"element infos\"."))
        self.dbeLimitCheckBox.setText(_translate("Form", "enable DBE limit and O H limit"))
        self.label_5.setText(_translate("Form", "min"))
        self.label_4.setText(_translate("Form", "max"))
        self.groupBox_3.setTitle(_translate("Form", "isotopes"))
        self.isotopeTreeWidget.headerItem().setText(0, _translate("Form", "Isotope"))
        self.isotopeTreeWidget.headerItem().setText(1, _translate("Form", "del"))
        self.isotopeTreeWidget.headerItem().setText(2, _translate("Form", "min"))
        self.isotopeTreeWidget.headerItem().setText(3, _translate("Form", "max"))
        self.isotopeTreeWidget.headerItem().setText(4, _translate("Form", "attrs"))
        self.isotopeAddToolButton.setText(_translate("Form", "+"))
        self.groupBox_4.setTitle(_translate("Form", "element infos"))
        self.elementShowPushButton.setText(_translate("Form", "show infos"))
        self.elementHidePushButton.setText(_translate("Form", "hide infos"))
        item = self.elementTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "e"))
        item = self.elementTableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "mass"))
        item = self.elementTableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "del"))
        item = self.elementTableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "2DBE"))
        item = self.elementTableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Hmin"))
        item = self.elementTableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Hmax"))
        item = self.elementTableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Form", "Omin"))
        item = self.elementTableWidget.horizontalHeaderItem(7)
        item.setText(_translate("Form", "Omax"))
        self.elementAddToolButton.setText(_translate("Form", "+"))
        self.groupBox.setTitle(_translate("Form", "Mass calculator"))
        self.calcPushButton.setText(_translate("Form", "Calc"))
