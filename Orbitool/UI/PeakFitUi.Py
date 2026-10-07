# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PeakFit.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QToolBox, QToolButton,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(826, 677)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.showSelectedPushButton = QPushButton(Form)
        self.showSelectedPushButton.setObjectName(u"showSelectedPushButton")

        self.verticalLayout.addWidget(self.showSelectedPushButton)

        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.toolBox = QToolBox(self.groupBox)
        self.toolBox.setObjectName(u"toolBox")
        self.singlePage = QWidget()
        self.singlePage.setObjectName(u"singlePage")
        self.singlePage.setGeometry(QRect(0, 0, 303, 236))
        self.gridLayout = QGridLayout(self.singlePage)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(3)
        self.filterSelectYToolButton = QToolButton(self.singlePage)
        self.filterSelectYToolButton.setObjectName(u"filterSelectYToolButton")

        self.gridLayout.addWidget(self.filterSelectYToolButton, 0, 2, 1, 1)

        self.filterSelectNToolButton = QToolButton(self.singlePage)
        self.filterSelectNToolButton.setObjectName(u"filterSelectNToolButton")

        self.gridLayout.addWidget(self.filterSelectNToolButton, 0, 3, 1, 1)

        self.filterFormulaYToolButton = QToolButton(self.singlePage)
        self.filterFormulaYToolButton.setObjectName(u"filterFormulaYToolButton")

        self.gridLayout.addWidget(self.filterFormulaYToolButton, 1, 2, 1, 1)

        self.filterFormulaNToolButton = QToolButton(self.singlePage)
        self.filterFormulaNToolButton.setObjectName(u"filterFormulaNToolButton")

        self.gridLayout.addWidget(self.filterFormulaNToolButton, 1, 3, 1, 1)

        self.label_8 = QLabel(self.singlePage)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 2, 0, 1, 2)

        self.filterStableIsotopeYToolButton = QToolButton(self.singlePage)
        self.filterStableIsotopeYToolButton.setObjectName(u"filterStableIsotopeYToolButton")

        self.gridLayout.addWidget(self.filterStableIsotopeYToolButton, 2, 2, 1, 1)

        self.filterStableIsotopeNToolButton = QToolButton(self.singlePage)
        self.filterStableIsotopeNToolButton.setObjectName(u"filterStableIsotopeNToolButton")

        self.gridLayout.addWidget(self.filterStableIsotopeNToolButton, 2, 3, 1, 1)

        self.label_5 = QLabel(self.singlePage)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)

        self.filterTagComboBox = QComboBox(self.singlePage)
        self.filterTagComboBox.setObjectName(u"filterTagComboBox")
        self.filterTagComboBox.setFocusPolicy(Qt.StrongFocus)

        self.gridLayout.addWidget(self.filterTagComboBox, 3, 1, 1, 1)

        self.filterTagYToolButton = QToolButton(self.singlePage)
        self.filterTagYToolButton.setObjectName(u"filterTagYToolButton")

        self.gridLayout.addWidget(self.filterTagYToolButton, 3, 2, 1, 1)

        self.filterTagNToolButton = QToolButton(self.singlePage)
        self.filterTagNToolButton.setObjectName(u"filterTagNToolButton")

        self.gridLayout.addWidget(self.filterTagNToolButton, 3, 3, 1, 1)

        self.label_6 = QLabel(self.singlePage)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)

        self.filterIntensityMaxToolButton = QToolButton(self.singlePage)
        self.filterIntensityMaxToolButton.setObjectName(u"filterIntensityMaxToolButton")

        self.gridLayout.addWidget(self.filterIntensityMaxToolButton, 4, 3, 1, 1)

        self.label_7 = QLabel(self.singlePage)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 5, 0, 1, 1)

        self.filterIntensityMinToolButton = QToolButton(self.singlePage)
        self.filterIntensityMinToolButton.setObjectName(u"filterIntensityMinToolButton")

        self.gridLayout.addWidget(self.filterIntensityMinToolButton, 5, 3, 1, 1)

        self.label_9 = QLabel(self.singlePage)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 6, 0, 1, 1)

        self.filterMassDefectMinDoubleSpinBox = QDoubleSpinBox(self.singlePage)
        self.filterMassDefectMinDoubleSpinBox.setObjectName(u"filterMassDefectMinDoubleSpinBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filterMassDefectMinDoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.filterMassDefectMinDoubleSpinBox.setSizePolicy(sizePolicy)
        self.filterMassDefectMinDoubleSpinBox.setFocusPolicy(Qt.StrongFocus)
        self.filterMassDefectMinDoubleSpinBox.setDecimals(3)
        self.filterMassDefectMinDoubleSpinBox.setMinimum(-0.500000000000000)
        self.filterMassDefectMinDoubleSpinBox.setMaximum(0.500000000000000)
        self.filterMassDefectMinDoubleSpinBox.setSingleStep(0.100000000000000)
        self.filterMassDefectMinDoubleSpinBox.setValue(-0.500000000000000)

        self.gridLayout.addWidget(self.filterMassDefectMinDoubleSpinBox, 6, 1, 1, 1)

        self.filterMassDefectMaxDoubleSpinBox = QDoubleSpinBox(self.singlePage)
        self.filterMassDefectMaxDoubleSpinBox.setObjectName(u"filterMassDefectMaxDoubleSpinBox")
        self.filterMassDefectMaxDoubleSpinBox.setFocusPolicy(Qt.StrongFocus)
        self.filterMassDefectMaxDoubleSpinBox.setDecimals(3)
        self.filterMassDefectMaxDoubleSpinBox.setMinimum(-0.500000000000000)
        self.filterMassDefectMaxDoubleSpinBox.setMaximum(0.500000000000000)
        self.filterMassDefectMaxDoubleSpinBox.setSingleStep(0.100000000000000)
        self.filterMassDefectMaxDoubleSpinBox.setValue(0.500000000000000)

        self.gridLayout.addWidget(self.filterMassDefectMaxDoubleSpinBox, 6, 2, 1, 1)

        self.filterMassDefectToolButton = QToolButton(self.singlePage)
        self.filterMassDefectToolButton.setObjectName(u"filterMassDefectToolButton")

        self.gridLayout.addWidget(self.filterMassDefectToolButton, 6, 3, 1, 1)

        self.label_10 = QLabel(self.singlePage)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 7, 0, 1, 1)

        self.filterGroupLineEdit = QLineEdit(self.singlePage)
        self.filterGroupLineEdit.setObjectName(u"filterGroupLineEdit")

        self.gridLayout.addWidget(self.filterGroupLineEdit, 7, 1, 1, 1)

        self.filterGroupYToolButton = QToolButton(self.singlePage)
        self.filterGroupYToolButton.setObjectName(u"filterGroupYToolButton")

        self.gridLayout.addWidget(self.filterGroupYToolButton, 7, 2, 1, 1)

        self.filterGroupNToolButton = QToolButton(self.singlePage)
        self.filterGroupNToolButton.setObjectName(u"filterGroupNToolButton")

        self.gridLayout.addWidget(self.filterGroupNToolButton, 7, 3, 1, 1)

        self.filterIntensityMinDoubleSpinBox = QDoubleSpinBox(self.singlePage)
        self.filterIntensityMinDoubleSpinBox.setObjectName(u"filterIntensityMinDoubleSpinBox")
        sizePolicy.setHeightForWidth(self.filterIntensityMinDoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.filterIntensityMinDoubleSpinBox.setSizePolicy(sizePolicy)
        self.filterIntensityMinDoubleSpinBox.setFocusPolicy(Qt.StrongFocus)
        self.filterIntensityMinDoubleSpinBox.setDecimals(1)
        self.filterIntensityMinDoubleSpinBox.setMaximum(1000000000000.000000000000000)
        self.filterIntensityMinDoubleSpinBox.setValue(10000.000000000000000)

        self.gridLayout.addWidget(self.filterIntensityMinDoubleSpinBox, 5, 1, 1, 2)

        self.filterIntensityMaxDoubleSpinBox = QDoubleSpinBox(self.singlePage)
        self.filterIntensityMaxDoubleSpinBox.setObjectName(u"filterIntensityMaxDoubleSpinBox")
        sizePolicy.setHeightForWidth(self.filterIntensityMaxDoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.filterIntensityMaxDoubleSpinBox.setSizePolicy(sizePolicy)
        self.filterIntensityMaxDoubleSpinBox.setFocusPolicy(Qt.StrongFocus)
        self.filterIntensityMaxDoubleSpinBox.setDecimals(1)
        self.filterIntensityMaxDoubleSpinBox.setMaximum(1000000000000.000000000000000)
        self.filterIntensityMaxDoubleSpinBox.setValue(100.000000000000000)

        self.gridLayout.addWidget(self.filterIntensityMaxDoubleSpinBox, 4, 1, 1, 2)

        self.label_3 = QLabel(self.singlePage)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 2)

        self.label_4 = QLabel(self.singlePage)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 2)

        self.toolBox.addItem(self.singlePage, u"single")
        self.stepPage = QWidget()
        self.stepPage.setObjectName(u"stepPage")
        self.stepPage.setGeometry(QRect(0, -88, 286, 200))
        self.formLayout = QFormLayout(self.stepPage)
        self.formLayout.setObjectName(u"formLayout")
        self.label_11 = QLabel(self.stepPage)
        self.label_11.setObjectName(u"label_11")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_11)

        self.stepPlusLineEdit = QLineEdit(self.stepPage)
        self.stepPlusLineEdit.setObjectName(u"stepPlusLineEdit")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.stepPlusLineEdit)

        self.label_13 = QLabel(self.stepPage)
        self.label_13.setObjectName(u"label_13")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_13)

        self.stepMinSpinBox = QSpinBox(self.stepPage)
        self.stepMinSpinBox.setObjectName(u"stepMinSpinBox")
        sizePolicy.setHeightForWidth(self.stepMinSpinBox.sizePolicy().hasHeightForWidth())
        self.stepMinSpinBox.setSizePolicy(sizePolicy)
        self.stepMinSpinBox.setFocusPolicy(Qt.StrongFocus)
        self.stepMinSpinBox.setMinimum(-99)
        self.stepMinSpinBox.setMaximum(99)
        self.stepMinSpinBox.setValue(-2)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.stepMinSpinBox)

        self.stepMaxSpinBox = QSpinBox(self.stepPage)
        self.stepMaxSpinBox.setObjectName(u"stepMaxSpinBox")
        sizePolicy.setHeightForWidth(self.stepMaxSpinBox.sizePolicy().hasHeightForWidth())
        self.stepMaxSpinBox.setSizePolicy(sizePolicy)
        self.stepMaxSpinBox.setFocusPolicy(Qt.StrongFocus)
        self.stepMaxSpinBox.setMinimum(-99)
        self.stepMaxSpinBox.setMaximum(99)
        self.stepMaxSpinBox.setValue(2)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.stepMaxSpinBox)

        self.stepRtolDoubleSpinBox = QDoubleSpinBox(self.stepPage)
        self.stepRtolDoubleSpinBox.setObjectName(u"stepRtolDoubleSpinBox")
        self.stepRtolDoubleSpinBox.setEnabled(False)
        self.stepRtolDoubleSpinBox.setValue(2.000000000000000)

        self.formLayout.setWidget(6, QFormLayout.ItemRole.FieldRole, self.stepRtolDoubleSpinBox)

        self.label_12 = QLabel(self.stepPage)
        self.label_12.setObjectName(u"label_12")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_12)

        self.stepMinusLineEdit = QLineEdit(self.stepPage)
        self.stepMinusLineEdit.setObjectName(u"stepMinusLineEdit")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.stepMinusLineEdit)

        self.label_14 = QLabel(self.stepPage)
        self.label_14.setObjectName(u"label_14")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.LabelRole, self.label_14)

        self.stepAccordToMassCheckBox = QCheckBox(self.stepPage)
        self.stepAccordToMassCheckBox.setObjectName(u"stepAccordToMassCheckBox")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.stepAccordToMassCheckBox)

        self.label_15 = QLabel(self.stepPage)
        self.label_15.setObjectName(u"label_15")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.label_15)

        self.stepPushButton = QPushButton(self.stepPage)
        self.stepPushButton.setObjectName(u"stepPushButton")

        self.formLayout.setWidget(7, QFormLayout.ItemRole.SpanningRole, self.stepPushButton)

        self.toolBox.addItem(self.stepPage, u"step")

        self.verticalLayout_3.addWidget(self.toolBox)

        self.filterClearPushButton = QPushButton(self.groupBox)
        self.filterClearPushButton.setObjectName(u"filterClearPushButton")

        self.verticalLayout_3.addWidget(self.filterClearPushButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(Form)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.onlySelectedCheckBox = QCheckBox(self.groupBox_2)
        self.onlySelectedCheckBox.setObjectName(u"onlySelectedCheckBox")
        self.onlySelectedCheckBox.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_5.addWidget(self.onlySelectedCheckBox)

        self.checkBox = QCheckBox(self.groupBox_2)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout_5.addWidget(self.checkBox)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.replotPushButton = QPushButton(self.groupBox_2)
        self.replotPushButton.setObjectName(u"replotPushButton")

        self.verticalLayout_4.addWidget(self.replotPushButton)

        self.calcDistributionCheckBox = QCheckBox(self.groupBox_2)
        self.calcDistributionCheckBox.setObjectName(u"calcDistributionCheckBox")
        self.calcDistributionCheckBox.setLayoutDirection(Qt.RightToLeft)
        self.calcDistributionCheckBox.setChecked(True)

        self.verticalLayout_4.addWidget(self.calcDistributionCheckBox)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.label)

        self.fitComboBox = QComboBox(self.groupBox_2)
        self.fitComboBox.setObjectName(u"fitComboBox")

        self.horizontalLayout_3.addWidget(self.fitComboBox)

        self.fitPushButton = QPushButton(self.groupBox_2)
        self.fitPushButton.setObjectName(u"fitPushButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.fitPushButton.sizePolicy().hasHeightForWidth())
        self.fitPushButton.setSizePolicy(sizePolicy2)

        self.horizontalLayout_3.addWidget(self.fitPushButton)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.actionRmTagPushButton = QPushButton(self.groupBox_2)
        self.actionRmTagPushButton.setObjectName(u"actionRmTagPushButton")

        self.horizontalLayout_4.addWidget(self.actionRmTagPushButton)

        self.addTagComboBox = QComboBox(self.groupBox_2)
        self.addTagComboBox.setObjectName(u"addTagComboBox")

        self.horizontalLayout_4.addWidget(self.addTagComboBox)

        self.addTagPushButton = QPushButton(self.groupBox_2)
        self.addTagPushButton.setObjectName(u"addTagPushButton")
        sizePolicy2.setHeightForWidth(self.addTagPushButton.sizePolicy().hasHeightForWidth())
        self.addTagPushButton.setSizePolicy(sizePolicy2)

        self.horizontalLayout_4.addWidget(self.addTagPushButton)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.actionAddToMassListPushButton = QPushButton(self.groupBox_2)
        self.actionAddToMassListPushButton.setObjectName(u"actionAddToMassListPushButton")

        self.horizontalLayout_6.addWidget(self.actionAddToMassListPushButton)

        self.actionMassDefectPushButton = QPushButton(self.groupBox_2)
        self.actionMassDefectPushButton.setObjectName(u"actionMassDefectPushButton")

        self.horizontalLayout_6.addWidget(self.actionMassDefectPushButton)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)


        self.verticalLayout.addWidget(self.groupBox_2)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy3)

        self.verticalLayout_2.addWidget(self.widget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.scaleToSpectrumPushButton = QPushButton(Form)
        self.scaleToSpectrumPushButton.setObjectName(u"scaleToSpectrumPushButton")

        self.horizontalLayout_2.addWidget(self.scaleToSpectrumPushButton)

        self.leftToolButton = QToolButton(Form)
        self.leftToolButton.setObjectName(u"leftToolButton")

        self.horizontalLayout_2.addWidget(self.leftToolButton)

        self.rightToolButton = QToolButton(Form)
        self.rightToolButton.setObjectName(u"rightToolButton")

        self.horizontalLayout_2.addWidget(self.rightToolButton)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.yLogcheckBox = QCheckBox(Form)
        self.yLogcheckBox.setObjectName(u"yLogcheckBox")

        self.horizontalLayout_2.addWidget(self.yLogcheckBox)

        self.rescaleToolButton = QToolButton(Form)
        self.rescaleToolButton.setObjectName(u"rescaleToolButton")

        self.horizontalLayout_2.addWidget(self.rescaleToolButton)

        self.yLimDoubleToolButton = QToolButton(Form)
        self.yLimDoubleToolButton.setObjectName(u"yLimDoubleToolButton")

        self.horizontalLayout_2.addWidget(self.yLimDoubleToolButton)

        self.yLimHalfToolButton = QToolButton(Form)
        self.yLimHalfToolButton.setObjectName(u"yLimHalfToolButton")

        self.horizontalLayout_2.addWidget(self.yLimHalfToolButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.retranslateUi(Form)

        self.toolBox.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
#if QT_CONFIG(tooltip)
        self.showSelectedPushButton.setToolTip(QCoreApplication.translate("Form", u"Alt+O", None))
#endif // QT_CONFIG(tooltip)
        self.showSelectedPushButton.setText(QCoreApplication.translate("Form", u"sh&ow selected spectrum", None))
#if QT_CONFIG(shortcut)
        self.showSelectedPushButton.setShortcut(QCoreApplication.translate("Form", u"Alt+O", None))
#endif // QT_CONFIG(shortcut)
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Peaks Filter", None))
        self.filterSelectYToolButton.setText(QCoreApplication.translate("Form", u"Y", None))
        self.filterSelectNToolButton.setText(QCoreApplication.translate("Form", u"N", None))
        self.filterFormulaYToolButton.setText(QCoreApplication.translate("Form", u"Y", None))
        self.filterFormulaNToolButton.setText(QCoreApplication.translate("Form", u"N", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"Stable isotope", None))
        self.filterStableIsotopeYToolButton.setText(QCoreApplication.translate("Form", u"Y", None))
        self.filterStableIsotopeNToolButton.setText(QCoreApplication.translate("Form", u"N", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Tag", None))
        self.filterTagYToolButton.setText(QCoreApplication.translate("Form", u"Y", None))
        self.filterTagNToolButton.setText(QCoreApplication.translate("Form", u"N", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"less than", None))
        self.filterIntensityMaxToolButton.setText(QCoreApplication.translate("Form", u"Y", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"larger than", None))
        self.filterIntensityMinToolButton.setText(QCoreApplication.translate("Form", u"Y", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"Mass defect", None))
        self.filterMassDefectToolButton.setText(QCoreApplication.translate("Form", u"Y", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"Has group", None))
        self.filterGroupLineEdit.setText(QCoreApplication.translate("Form", u"NO3-", None))
        self.filterGroupYToolButton.setText(QCoreApplication.translate("Form", u"Y", None))
        self.filterGroupNToolButton.setText(QCoreApplication.translate("Form", u"N", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Selected", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Formula", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.singlePage), QCoreApplication.translate("Form", u"single", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"Group+", None))
        self.stepPlusLineEdit.setText(QCoreApplication.translate("Form", u"HO2", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"Step range", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"Group-", None))
        self.label_14.setText(QCoreApplication.translate("Form", u"tolerance(ppm)", None))
#if QT_CONFIG(tooltip)
        self.stepAccordToMassCheckBox.setToolTip(QCoreApplication.translate("Form", u"step according to mass instead of formula", None))
#endif // QT_CONFIG(tooltip)
        self.stepAccordToMassCheckBox.setText("")
#if QT_CONFIG(tooltip)
        self.label_15.setToolTip(QCoreApplication.translate("Form", u"according to mass instead of only formula", None))
#endif // QT_CONFIG(tooltip)
        self.label_15.setText(QCoreApplication.translate("Form", u"according to mass", None))
        self.stepPushButton.setText(QCoreApplication.translate("Form", u"step", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.stepPage), QCoreApplication.translate("Form", u"step", None))
#if QT_CONFIG(tooltip)
        self.filterClearPushButton.setToolTip(QCoreApplication.translate("Form", u"Alt+C", None))
#endif // QT_CONFIG(tooltip)
        self.filterClearPushButton.setText(QCoreApplication.translate("Form", u"&clear filter", None))
#if QT_CONFIG(shortcut)
        self.filterClearPushButton.setShortcut(QCoreApplication.translate("Form", u"Alt+C", None))
#endif // QT_CONFIG(shortcut)
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"Actions", None))
#if QT_CONFIG(tooltip)
        self.onlySelectedCheckBox.setToolTip(QCoreApplication.translate("Form", u"Apply the following actions to the selected peaks only.", None))
#endif // QT_CONFIG(tooltip)
        self.onlySelectedCheckBox.setText(QCoreApplication.translate("Form", u"Only selected peaks", None))
#if QT_CONFIG(tooltip)
        self.checkBox.setToolTip(QCoreApplication.translate("Form", u"If no peak is selected, the action is applied to all displayed peaks.", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox.setText(QCoreApplication.translate("Form", u"All if no peak selected", None))
        self.replotPushButton.setText(QCoreApplication.translate("Form", u"replot within list", None))
#if QT_CONFIG(tooltip)
        self.calcDistributionCheckBox.setToolTip(QCoreApplication.translate("Form", u"If checked, isotope peaks that do not match the natural distribution will be removed after fitting.", None))
#endif // QT_CONFIG(tooltip)
        self.calcDistributionCheckBox.setText(QCoreApplication.translate("Form", u"Filter formulas with natural abundance", None))
        self.label.setText(QCoreApplication.translate("Form", u"Use", None))
        self.fitPushButton.setText(QCoreApplication.translate("Form", u"Fit", None))
#if QT_CONFIG(tooltip)
        self.actionRmTagPushButton.setToolTip(QCoreApplication.translate("Form", u"Alt+R", None))
#endif // QT_CONFIG(tooltip)
        self.actionRmTagPushButton.setText(QCoreApplication.translate("Form", u"Remove tag", None))
#if QT_CONFIG(shortcut)
        self.actionRmTagPushButton.setShortcut(QCoreApplication.translate("Form", u"Alt+R", None))
#endif // QT_CONFIG(shortcut)
        self.addTagPushButton.setText(QCoreApplication.translate("Form", u"Add tag", None))
#if QT_CONFIG(tooltip)
        self.actionAddToMassListPushButton.setToolTip(QCoreApplication.translate("Form", u"Alt+A", None))
#endif // QT_CONFIG(tooltip)
        self.actionAddToMassListPushButton.setText(QCoreApplication.translate("Form", u"&add to mass list", None))
#if QT_CONFIG(shortcut)
        self.actionAddToMassListPushButton.setShortcut(QCoreApplication.translate("Form", u"Alt+A", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.actionMassDefectPushButton.setToolTip(QCoreApplication.translate("Form", u"Plot the mass defect of the peaks currently shown.", None))
#endif // QT_CONFIG(tooltip)
        self.actionMassDefectPushButton.setText(QCoreApplication.translate("Form", u"mass defect", None))
        self.scaleToSpectrumPushButton.setText(QCoreApplication.translate("Form", u"Scale to spectrum", None))
        self.leftToolButton.setText(QCoreApplication.translate("Form", u"\u2190", None))
#if QT_CONFIG(shortcut)
        self.leftToolButton.setShortcut(QCoreApplication.translate("Form", u"Left", None))
#endif // QT_CONFIG(shortcut)
        self.rightToolButton.setText(QCoreApplication.translate("Form", u"\u2192", None))
#if QT_CONFIG(shortcut)
        self.rightToolButton.setShortcut(QCoreApplication.translate("Form", u"Right", None))
#endif // QT_CONFIG(shortcut)
        self.label_2.setText(QCoreApplication.translate("Form", u"y-lim", None))
        self.yLogcheckBox.setText(QCoreApplication.translate("Form", u"y-log scale", None))
        self.rescaleToolButton.setText(QCoreApplication.translate("Form", u"rescale", None))
        self.yLimDoubleToolButton.setText(QCoreApplication.translate("Form", u"\u00d72 (\u2191)", None))
#if QT_CONFIG(shortcut)
        self.yLimDoubleToolButton.setShortcut(QCoreApplication.translate("Form", u"Up", None))
#endif // QT_CONFIG(shortcut)
        self.yLimHalfToolButton.setText(QCoreApplication.translate("Form", u"\u00f72 (\u2193)", None))
#if QT_CONFIG(shortcut)
        self.yLimHalfToolButton.setShortcut(QCoreApplication.translate("Form", u"Down", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

