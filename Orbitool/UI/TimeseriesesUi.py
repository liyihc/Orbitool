# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Timeserieses.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QAbstractSpinBox, QApplication,
    QCheckBox, QDoubleSpinBox, QFormLayout, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QRadioButton, QSizePolicy, QSplitter, QTableWidget,
    QTableWidgetItem, QToolBox, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(611, 417)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(Form)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.layoutWidget_3 = QWidget(self.splitter)
        self.layoutWidget_3.setObjectName(u"layoutWidget_3")
        self.verticalLayout_17 = QVBoxLayout(self.layoutWidget_3)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.toolBox = QToolBox(self.layoutWidget_3)
        self.toolBox.setObjectName(u"toolBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBox.sizePolicy().hasHeightForWidth())
        self.toolBox.setSizePolicy(sizePolicy)
        self.showPeakPage = QWidget()
        self.showPeakPage.setObjectName(u"showPeakPage")
        self.showPeakPage.setGeometry(QRect(0, 0, 314, 182))
        sizePolicy.setHeightForWidth(self.showPeakPage.sizePolicy().hasHeightForWidth())
        self.showPeakPage.setSizePolicy(sizePolicy)
        self.formLayout = QFormLayout(self.showPeakPage)
        self.formLayout.setObjectName(u"formLayout")
        self.mzRadioButton = QRadioButton(self.showPeakPage)
        self.mzRadioButton.setObjectName(u"mzRadioButton")
        self.mzRadioButton.setChecked(True)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.mzRadioButton)

        self.mzDoubleSpinBox = QDoubleSpinBox(self.showPeakPage)
        self.mzDoubleSpinBox.setObjectName(u"mzDoubleSpinBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.mzDoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.mzDoubleSpinBox.setSizePolicy(sizePolicy1)
        self.mzDoubleSpinBox.setDecimals(5)
        self.mzDoubleSpinBox.setMaximum(999.990000000000009)
        self.mzDoubleSpinBox.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.mzDoubleSpinBox)

        self.formulaRadioButton = QRadioButton(self.showPeakPage)
        self.formulaRadioButton.setObjectName(u"formulaRadioButton")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.formulaRadioButton)

        self.formulaLineEdit = QLineEdit(self.showPeakPage)
        self.formulaLineEdit.setObjectName(u"formulaLineEdit")
        sizePolicy1.setHeightForWidth(self.formulaLineEdit.sizePolicy().hasHeightForWidth())
        self.formulaLineEdit.setSizePolicy(sizePolicy1)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.formulaLineEdit)

        self.peakListRadioButton = QRadioButton(self.showPeakPage)
        self.peakListRadioButton.setObjectName(u"peakListRadioButton")
        sizePolicy1.setHeightForWidth(self.peakListRadioButton.sizePolicy().hasHeightForWidth())
        self.peakListRadioButton.setSizePolicy(sizePolicy1)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.peakListRadioButton)

        self.selectedMassListRadioButton = QRadioButton(self.showPeakPage)
        self.selectedMassListRadioButton.setObjectName(u"selectedMassListRadioButton")
        sizePolicy1.setHeightForWidth(self.selectedMassListRadioButton.sizePolicy().hasHeightForWidth())
        self.selectedMassListRadioButton.setSizePolicy(sizePolicy1)
        self.selectedMassListRadioButton.setChecked(False)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.SpanningRole, self.selectedMassListRadioButton)

        self.massListRadioButton = QRadioButton(self.showPeakPage)
        self.massListRadioButton.setObjectName(u"massListRadioButton")
        sizePolicy1.setHeightForWidth(self.massListRadioButton.sizePolicy().hasHeightForWidth())
        self.massListRadioButton.setSizePolicy(sizePolicy1)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.SpanningRole, self.massListRadioButton)

        self.label_22 = QLabel(self.showPeakPage)
        self.label_22.setObjectName(u"label_22")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.label_22)

        self.rtolDoubleSpinBox = QDoubleSpinBox(self.showPeakPage)
        self.rtolDoubleSpinBox.setObjectName(u"rtolDoubleSpinBox")
        sizePolicy1.setHeightForWidth(self.rtolDoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.rtolDoubleSpinBox.setSizePolicy(sizePolicy1)
        self.rtolDoubleSpinBox.setMinimum(0.010000000000000)
        self.rtolDoubleSpinBox.setMaximum(99.989999999999995)
        self.rtolDoubleSpinBox.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.rtolDoubleSpinBox.setValue(1.000000000000000)

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.rtolDoubleSpinBox)

        self.calcPeakPushButton = QPushButton(self.showPeakPage)
        self.calcPeakPushButton.setObjectName(u"calcPeakPushButton")
        sizePolicy1.setHeightForWidth(self.calcPeakPushButton.sizePolicy().hasHeightForWidth())
        self.calcPeakPushButton.setSizePolicy(sizePolicy1)

        self.formLayout.setWidget(6, QFormLayout.ItemRole.SpanningRole, self.calcPeakPushButton)

        self.toolBox.addItem(self.showPeakPage, u"Show peak time series")
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.page_4.setGeometry(QRect(0, 0, 314, 91))
        self.formLayout_2 = QFormLayout(self.page_4)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label = QLabel(self.page_4)
        self.label.setObjectName(u"label")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.rangeMinDoubleSpinBox = QDoubleSpinBox(self.page_4)
        self.rangeMinDoubleSpinBox.setObjectName(u"rangeMinDoubleSpinBox")
        self.rangeMinDoubleSpinBox.setDecimals(5)
        self.rangeMinDoubleSpinBox.setMaximum(999.990000000000009)
        self.rangeMinDoubleSpinBox.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.rangeMinDoubleSpinBox)

        self.label_2 = QLabel(self.page_4)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.rangeMaxDoubleSpinBox = QDoubleSpinBox(self.page_4)
        self.rangeMaxDoubleSpinBox.setObjectName(u"rangeMaxDoubleSpinBox")
        self.rangeMaxDoubleSpinBox.setDecimals(5)
        self.rangeMaxDoubleSpinBox.setMaximum(9999.989999999999782)
        self.rangeMaxDoubleSpinBox.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.rangeMaxDoubleSpinBox)

        self.calcRangePushButton = QPushButton(self.page_4)
        self.calcRangePushButton.setObjectName(u"calcRangePushButton")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.SpanningRole, self.calcRangePushButton)

        self.toolBox.addItem(self.page_4, u"Show intensity sum time series")

        self.verticalLayout_17.addWidget(self.toolBox)

        self.tableWidget = QTableWidget(self.layoutWidget_3)
        if (self.tableWidget.columnCount() < 4):
            self.tableWidget.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy2)
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_17.addWidget(self.tableWidget)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_23 = QLabel(self.layoutWidget_3)
        self.label_23.setObjectName(u"label_23")
        sizePolicy2.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy2)

        self.horizontalLayout_16.addWidget(self.label_23)

        self.removeSelectedPushButton = QPushButton(self.layoutWidget_3)
        self.removeSelectedPushButton.setObjectName(u"removeSelectedPushButton")
        sizePolicy1.setHeightForWidth(self.removeSelectedPushButton.sizePolicy().hasHeightForWidth())
        self.removeSelectedPushButton.setSizePolicy(sizePolicy1)

        self.horizontalLayout_16.addWidget(self.removeSelectedPushButton)

        self.removeAllPushButton = QPushButton(self.layoutWidget_3)
        self.removeAllPushButton.setObjectName(u"removeAllPushButton")
        sizePolicy1.setHeightForWidth(self.removeAllPushButton.sizePolicy().hasHeightForWidth())
        self.removeAllPushButton.setSizePolicy(sizePolicy1)

        self.horizontalLayout_16.addWidget(self.removeAllPushButton)


        self.verticalLayout_17.addLayout(self.horizontalLayout_16)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_3 = QLabel(self.layoutWidget_3)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.exportTimeseriesPushButton = QPushButton(self.layoutWidget_3)
        self.exportTimeseriesPushButton.setObjectName(u"exportTimeseriesPushButton")
        sizePolicy1.setHeightForWidth(self.exportTimeseriesPushButton.sizePolicy().hasHeightForWidth())
        self.exportTimeseriesPushButton.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.exportTimeseriesPushButton)

        self.exportSelectedPushButton = QPushButton(self.layoutWidget_3)
        self.exportSelectedPushButton.setObjectName(u"exportSelectedPushButton")

        self.horizontalLayout.addWidget(self.exportSelectedPushButton)

        self.exportDeviationPushButton = QPushButton(self.layoutWidget_3)
        self.exportDeviationPushButton.setObjectName(u"exportDeviationPushButton")

        self.horizontalLayout.addWidget(self.exportDeviationPushButton)


        self.verticalLayout_17.addLayout(self.horizontalLayout)

        self.splitter.addWidget(self.layoutWidget_3)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout_18 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.layoutWidget)
        self.widget.setObjectName(u"widget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy3)

        self.verticalLayout_18.addWidget(self.widget)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.logScaleCheckBox = QCheckBox(self.layoutWidget)
        self.logScaleCheckBox.setObjectName(u"logScaleCheckBox")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.logScaleCheckBox.sizePolicy().hasHeightForWidth())
        self.logScaleCheckBox.setSizePolicy(sizePolicy4)

        self.horizontalLayout_24.addWidget(self.logScaleCheckBox)

        self.rescalePushButton = QPushButton(self.layoutWidget)
        self.rescalePushButton.setObjectName(u"rescalePushButton")
        sizePolicy1.setHeightForWidth(self.rescalePushButton.sizePolicy().hasHeightForWidth())
        self.rescalePushButton.setSizePolicy(sizePolicy1)

        self.horizontalLayout_24.addWidget(self.rescalePushButton)


        self.verticalLayout_18.addLayout(self.horizontalLayout_24)

        self.splitter.addWidget(self.layoutWidget)

        self.verticalLayout.addWidget(self.splitter)


        self.retranslateUi(Form)

        self.toolBox.setCurrentIndex(0)
        self.toolBox.layout().setSpacing(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.mzRadioButton.setText(QCoreApplication.translate("Form", u"mz", None))
        self.formulaRadioButton.setText(QCoreApplication.translate("Form", u"formula", None))
        self.peakListRadioButton.setText(QCoreApplication.translate("Form", u"peak list", None))
        self.selectedMassListRadioButton.setText(QCoreApplication.translate("Form", u"mass list selected peak(s)", None))
        self.massListRadioButton.setText(QCoreApplication.translate("Form", u"mass list all peaks", None))
        self.label_22.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>tolerance(ppm)</p></body></html>", None))
        self.calcPeakPushButton.setText(QCoreApplication.translate("Form", u"Calc time series", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.showPeakPage), QCoreApplication.translate("Form", u"Show peak time series", None))
        self.label.setText(QCoreApplication.translate("Form", u"left", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"right", None))
        self.calcRangePushButton.setText(QCoreApplication.translate("Form", u"Calc time series", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_4), QCoreApplication.translate("Form", u"Show intensity sum time series", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"show", None))
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"tag", None))
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"mz-from", None))
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"mz-to", None))
        self.label_23.setText(QCoreApplication.translate("Form", u"Remove", None))
        self.removeSelectedPushButton.setText(QCoreApplication.translate("Form", u"selected", None))
        self.removeAllPushButton.setText(QCoreApplication.translate("Form", u"all", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Export", None))
        self.exportTimeseriesPushButton.setText(QCoreApplication.translate("Form", u"time serieses", None))
        self.exportSelectedPushButton.setText(QCoreApplication.translate("Form", u"selected", None))
        self.exportDeviationPushButton.setText(QCoreApplication.translate("Form", u"deviations", None))
        self.logScaleCheckBox.setText(QCoreApplication.translate("Form", u"y-log scale", None))
        self.rescalePushButton.setText(QCoreApplication.translate("Form", u"autoscale y axis", None))
    # retranslateUi

