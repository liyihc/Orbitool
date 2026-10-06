# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CatTimeseries.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QDoubleSpinBox,
    QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QRadioButton, QScrollArea, QSizePolicy, QSpinBox,
    QSplitter, QTabWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(753, 494)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.timeSeriesCatSplitter = QSplitter(Form)
        self.timeSeriesCatSplitter.setObjectName(u"timeSeriesCatSplitter")
        self.timeSeriesCatSplitter.setOrientation(Qt.Horizontal)
        self.verticalLayoutWidget = QWidget(self.timeSeriesCatSplitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayout_23 = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.verticalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.csvAddPushButton = QPushButton(self.verticalLayoutWidget)
        self.csvAddPushButton.setObjectName(u"csvAddPushButton")

        self.verticalLayout_23.addWidget(self.csvAddPushButton)

        self.horizontalLayout_33 = QHBoxLayout()
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.label_31 = QLabel(self.verticalLayoutWidget)
        self.label_31.setObjectName(u"label_31")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_31.sizePolicy().hasHeightForWidth())
        self.label_31.setSizePolicy(sizePolicy)

        self.horizontalLayout_33.addWidget(self.label_31)

        self.timeSeriesCatFileLabel = QLabel(self.verticalLayoutWidget)
        self.timeSeriesCatFileLabel.setObjectName(u"timeSeriesCatFileLabel")

        self.horizontalLayout_33.addWidget(self.timeSeriesCatFileLabel)


        self.verticalLayout_23.addLayout(self.horizontalLayout_33)

        self.timeSeriesCatCsvTabWidget = QTabWidget(self.verticalLayoutWidget)
        self.timeSeriesCatCsvTabWidget.setObjectName(u"timeSeriesCatCsvTabWidget")
        self.timeSeriesCatRawTab = QWidget()
        self.timeSeriesCatRawTab.setObjectName(u"timeSeriesCatRawTab")
        self.verticalLayout_29 = QVBoxLayout(self.timeSeriesCatRawTab)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.verticalLayout_29.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.timeSeriesCatRawTab)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 228, 356))
        self.verticalLayout_30 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.rawTableWidget = QTableWidget(self.scrollAreaWidgetContents)
        self.rawTableWidget.setObjectName(u"rawTableWidget")
        self.rawTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.rawTableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.rawTableWidget.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_30.addWidget(self.rawTableWidget)

        self.groupBox_10 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.gridLayout = QGridLayout(self.groupBox_10)
        self.gridLayout.setObjectName(u"gridLayout")
        self.rawMatlabRadioButton = QRadioButton(self.groupBox_10)
        self.rawMatlabRadioButton.setObjectName(u"rawMatlabRadioButton")

        self.gridLayout.addWidget(self.rawMatlabRadioButton, 1, 0, 1, 1)

        self.rawIgorRadioButton = QRadioButton(self.groupBox_10)
        self.rawIgorRadioButton.setObjectName(u"rawIgorRadioButton")

        self.gridLayout.addWidget(self.rawIgorRadioButton, 0, 1, 1, 1)

        self.rawExcelRadioButton = QRadioButton(self.groupBox_10)
        self.rawExcelRadioButton.setObjectName(u"rawExcelRadioButton")

        self.gridLayout.addWidget(self.rawExcelRadioButton, 1, 1, 1, 1)

        self.rawIsoRadioButton = QRadioButton(self.groupBox_10)
        self.rawIsoRadioButton.setObjectName(u"rawIsoRadioButton")
        self.rawIsoRadioButton.setChecked(True)

        self.gridLayout.addWidget(self.rawIsoRadioButton, 0, 0, 1, 1)

        self.rawCustomRadioButton = QRadioButton(self.groupBox_10)
        self.rawCustomRadioButton.setObjectName(u"rawCustomRadioButton")

        self.gridLayout.addWidget(self.rawCustomRadioButton, 2, 0, 1, 1)

        self.rawCustomLineEdit = QLineEdit(self.groupBox_10)
        self.rawCustomLineEdit.setObjectName(u"rawCustomLineEdit")

        self.gridLayout.addWidget(self.rawCustomLineEdit, 2, 1, 1, 1)


        self.verticalLayout_30.addWidget(self.groupBox_10)

        self.formLayout_11 = QFormLayout()
        self.formLayout_11.setObjectName(u"formLayout_11")
        self.label_30 = QLabel(self.scrollAreaWidgetContents)
        self.label_30.setObjectName(u"label_30")

        self.formLayout_11.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_30)

        self.rawTimeColumnLabel = QLabel(self.scrollAreaWidgetContents)
        self.rawTimeColumnLabel.setObjectName(u"rawTimeColumnLabel")

        self.formLayout_11.setWidget(1, QFormLayout.ItemRole.LabelRole, self.rawTimeColumnLabel)

        self.rawTimeColumnSpinBox = QSpinBox(self.scrollAreaWidgetContents)
        self.rawTimeColumnSpinBox.setObjectName(u"rawTimeColumnSpinBox")
        self.rawTimeColumnSpinBox.setMinimum(1)

        self.formLayout_11.setWidget(1, QFormLayout.ItemRole.FieldRole, self.rawTimeColumnSpinBox)

        self.rawFirstIonColumnLabel = QLabel(self.scrollAreaWidgetContents)
        self.rawFirstIonColumnLabel.setObjectName(u"rawFirstIonColumnLabel")

        self.formLayout_11.setWidget(2, QFormLayout.ItemRole.LabelRole, self.rawFirstIonColumnLabel)

        self.rawFirstIonColumnLineEdit = QSpinBox(self.scrollAreaWidgetContents)
        self.rawFirstIonColumnLineEdit.setObjectName(u"rawFirstIonColumnLineEdit")
        self.rawFirstIonColumnLineEdit.setMinimum(2)
        self.rawFirstIonColumnLineEdit.setMaximum(99999)

        self.formLayout_11.setWidget(2, QFormLayout.ItemRole.FieldRole, self.rawFirstIonColumnLineEdit)

        self.rawIonRowLabel = QLabel(self.scrollAreaWidgetContents)
        self.rawIonRowLabel.setObjectName(u"rawIonRowLabel")

        self.formLayout_11.setWidget(3, QFormLayout.ItemRole.LabelRole, self.rawIonRowLabel)

        self.rawIonRowLineEdit = QSpinBox(self.scrollAreaWidgetContents)
        self.rawIonRowLineEdit.setObjectName(u"rawIonRowLineEdit")
        self.rawIonRowLineEdit.setMinimum(1)
        self.rawIonRowLineEdit.setMaximum(99999)

        self.formLayout_11.setWidget(3, QFormLayout.ItemRole.FieldRole, self.rawIonRowLineEdit)


        self.verticalLayout_30.addLayout(self.formLayout_11)

        self.rawFinishPushButton = QPushButton(self.scrollAreaWidgetContents)
        self.rawFinishPushButton.setObjectName(u"rawFinishPushButton")

        self.verticalLayout_30.addWidget(self.rawFinishPushButton)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_29.addWidget(self.scrollArea)

        self.timeSeriesCatCsvTabWidget.addTab(self.timeSeriesCatRawTab, "")
        self.timeSeriesCatProcessedTab = QWidget()
        self.timeSeriesCatProcessedTab.setObjectName(u"timeSeriesCatProcessedTab")
        self.verticalLayout_28 = QVBoxLayout(self.timeSeriesCatProcessedTab)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.processedTableWidget = QTableWidget(self.timeSeriesCatProcessedTab)
        if (self.processedTableWidget.columnCount() < 1):
            self.processedTableWidget.setColumnCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        self.processedTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        self.processedTableWidget.setObjectName(u"processedTableWidget")
        self.processedTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.processedTableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.processedTableWidget.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_28.addWidget(self.processedTableWidget)

        self.timeSeriesCatCsvTabWidget.addTab(self.timeSeriesCatProcessedTab, "")

        self.verticalLayout_23.addWidget(self.timeSeriesCatCsvTabWidget)

        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.label_16 = QLabel(self.verticalLayoutWidget)
        self.label_16.setObjectName(u"label_16")

        self.horizontalLayout_28.addWidget(self.label_16)

        self.rtolDoubleSpinBox = QDoubleSpinBox(self.verticalLayoutWidget)
        self.rtolDoubleSpinBox.setObjectName(u"rtolDoubleSpinBox")
        self.rtolDoubleSpinBox.setMinimum(0.010000000000000)
        self.rtolDoubleSpinBox.setMaximum(99.989999999999995)
        self.rtolDoubleSpinBox.setValue(1.000000000000000)

        self.horizontalLayout_28.addWidget(self.rtolDoubleSpinBox)


        self.verticalLayout_23.addLayout(self.horizontalLayout_28)

        self.catPushButton = QPushButton(self.verticalLayoutWidget)
        self.catPushButton.setObjectName(u"catPushButton")

        self.verticalLayout_23.addWidget(self.catPushButton)

        self.timeSeriesCatSplitter.addWidget(self.verticalLayoutWidget)
        self.verticalLayoutWidget_2 = QWidget(self.timeSeriesCatSplitter)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayout_25 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.verticalLayout_25.setContentsMargins(0, 0, 0, 0)
        self.timeSeriesesTableWidget = QTableWidget(self.verticalLayoutWidget_2)
        if (self.timeSeriesesTableWidget.columnCount() < 2):
            self.timeSeriesesTableWidget.setColumnCount(2)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.timeSeriesesTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.timeSeriesesTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem2)
        self.timeSeriesesTableWidget.setObjectName(u"timeSeriesesTableWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.timeSeriesesTableWidget.sizePolicy().hasHeightForWidth())
        self.timeSeriesesTableWidget.setSizePolicy(sizePolicy1)
        self.timeSeriesesTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.timeSeriesesTableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.timeSeriesesTableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.timeSeriesesTableWidget.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_25.addWidget(self.timeSeriesesTableWidget)

        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.label_17 = QLabel(self.verticalLayoutWidget_2)
        self.label_17.setObjectName(u"label_17")
        sizePolicy.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)

        self.horizontalLayout_29.addWidget(self.label_17)

        self.rmSelectedPushButton = QPushButton(self.verticalLayoutWidget_2)
        self.rmSelectedPushButton.setObjectName(u"rmSelectedPushButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.rmSelectedPushButton.sizePolicy().hasHeightForWidth())
        self.rmSelectedPushButton.setSizePolicy(sizePolicy2)

        self.horizontalLayout_29.addWidget(self.rmSelectedPushButton)

        self.rmAllPushButton = QPushButton(self.verticalLayoutWidget_2)
        self.rmAllPushButton.setObjectName(u"rmAllPushButton")
        sizePolicy2.setHeightForWidth(self.rmAllPushButton.sizePolicy().hasHeightForWidth())
        self.rmAllPushButton.setSizePolicy(sizePolicy2)

        self.horizontalLayout_29.addWidget(self.rmAllPushButton)


        self.verticalLayout_25.addLayout(self.horizontalLayout_29)

        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.label_26 = QLabel(self.verticalLayoutWidget_2)
        self.label_26.setObjectName(u"label_26")
        sizePolicy.setHeightForWidth(self.label_26.sizePolicy().hasHeightForWidth())
        self.label_26.setSizePolicy(sizePolicy)

        self.horizontalLayout_31.addWidget(self.label_26)

        self.intSelectedPushButton = QPushButton(self.verticalLayoutWidget_2)
        self.intSelectedPushButton.setObjectName(u"intSelectedPushButton")
        sizePolicy2.setHeightForWidth(self.intSelectedPushButton.sizePolicy().hasHeightForWidth())
        self.intSelectedPushButton.setSizePolicy(sizePolicy2)

        self.horizontalLayout_31.addWidget(self.intSelectedPushButton)

        self.intAllPushButton = QPushButton(self.verticalLayoutWidget_2)
        self.intAllPushButton.setObjectName(u"intAllPushButton")
        sizePolicy2.setHeightForWidth(self.intAllPushButton.sizePolicy().hasHeightForWidth())
        self.intAllPushButton.setSizePolicy(sizePolicy2)

        self.horizontalLayout_31.addWidget(self.intAllPushButton)


        self.verticalLayout_25.addLayout(self.horizontalLayout_31)

        self.timeSeriesTableWidget = QTableWidget(self.verticalLayoutWidget_2)
        if (self.timeSeriesTableWidget.columnCount() < 2):
            self.timeSeriesTableWidget.setColumnCount(2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.timeSeriesTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.timeSeriesTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem4)
        self.timeSeriesTableWidget.setObjectName(u"timeSeriesTableWidget")
        sizePolicy1.setHeightForWidth(self.timeSeriesTableWidget.sizePolicy().hasHeightForWidth())
        self.timeSeriesTableWidget.setSizePolicy(sizePolicy1)
        self.timeSeriesTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.timeSeriesTableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.timeSeriesTableWidget.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_25.addWidget(self.timeSeriesTableWidget)

        self.exportPushButton = QPushButton(self.verticalLayoutWidget_2)
        self.exportPushButton.setObjectName(u"exportPushButton")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.exportPushButton.sizePolicy().hasHeightForWidth())
        self.exportPushButton.setSizePolicy(sizePolicy3)

        self.verticalLayout_25.addWidget(self.exportPushButton)

        self.timeSeriesCatSplitter.addWidget(self.verticalLayoutWidget_2)
        self.verticalLayoutWidget_3 = QWidget(self.timeSeriesCatSplitter)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayout_26 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.verticalLayout_26.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.verticalLayoutWidget_3)
        self.widget.setObjectName(u"widget")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy4)

        self.verticalLayout_26.addWidget(self.widget)

        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.showLegendsCheckBox = QCheckBox(self.verticalLayoutWidget_3)
        self.showLegendsCheckBox.setObjectName(u"showLegendsCheckBox")
        sizePolicy2.setHeightForWidth(self.showLegendsCheckBox.sizePolicy().hasHeightForWidth())
        self.showLegendsCheckBox.setSizePolicy(sizePolicy2)

        self.horizontalLayout_32.addWidget(self.showLegendsCheckBox)

        self.logScaleCheckBox = QCheckBox(self.verticalLayoutWidget_3)
        self.logScaleCheckBox.setObjectName(u"logScaleCheckBox")
        sizePolicy2.setHeightForWidth(self.logScaleCheckBox.sizePolicy().hasHeightForWidth())
        self.logScaleCheckBox.setSizePolicy(sizePolicy2)

        self.horizontalLayout_32.addWidget(self.logScaleCheckBox)

        self.rescalePushButton = QPushButton(self.verticalLayoutWidget_3)
        self.rescalePushButton.setObjectName(u"rescalePushButton")
        sizePolicy2.setHeightForWidth(self.rescalePushButton.sizePolicy().hasHeightForWidth())
        self.rescalePushButton.setSizePolicy(sizePolicy2)

        self.horizontalLayout_32.addWidget(self.rescalePushButton)


        self.verticalLayout_26.addLayout(self.horizontalLayout_32)

        self.timeSeriesCatSplitter.addWidget(self.verticalLayoutWidget_3)

        self.verticalLayout.addWidget(self.timeSeriesCatSplitter)


        self.retranslateUi(Form)

        self.timeSeriesCatCsvTabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.csvAddPushButton.setText(QCoreApplication.translate("Form", u"Add csv files", None))
        self.label_31.setText(QCoreApplication.translate("Form", u"File:", None))
        self.timeSeriesCatFileLabel.setText("")
        self.groupBox_10.setTitle(QCoreApplication.translate("Form", u"time format", None))
        self.rawMatlabRadioButton.setText(QCoreApplication.translate("Form", u"matlab", None))
        self.rawIgorRadioButton.setText(QCoreApplication.translate("Form", u"igor time", None))
        self.rawExcelRadioButton.setText(QCoreApplication.translate("Form", u"excel time", None))
        self.rawIsoRadioButton.setText(QCoreApplication.translate("Form", u"iso time", None))
        self.rawCustomRadioButton.setText(QCoreApplication.translate("Form", u"custom", None))
        self.rawCustomLineEdit.setText(QCoreApplication.translate("Form", u"%Y%m%d %H:%M:%S", None))
        self.label_30.setText(QCoreApplication.translate("Form", u"Key row/col", None))
        self.rawTimeColumnLabel.setText(QCoreApplication.translate("Form", u"Time column", None))
        self.rawFirstIonColumnLabel.setText(QCoreApplication.translate("Form", u"First ion column", None))
        self.rawIonRowLabel.setText(QCoreApplication.translate("Form", u"Ion row", None))
        self.rawFinishPushButton.setText(QCoreApplication.translate("Form", u"Finish", None))
        self.timeSeriesCatCsvTabWidget.setTabText(self.timeSeriesCatCsvTabWidget.indexOf(self.timeSeriesCatRawTab), QCoreApplication.translate("Form", u"raw data", None))
        ___qtablewidgetitem = self.processedTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"time", None))
        self.timeSeriesCatCsvTabWidget.setTabText(self.timeSeriesCatCsvTabWidget.indexOf(self.timeSeriesCatProcessedTab), QCoreApplication.translate("Form", u"processed", None))
        self.label_16.setText(QCoreApplication.translate("Form", u"rtol", None))
        self.catPushButton.setText(QCoreApplication.translate("Form", u"Concatenate/Next file", None))
        ___qtablewidgetitem1 = self.timeSeriesesTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"tag", None))
        ___qtablewidgetitem2 = self.timeSeriesesTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"mz", None))
        self.label_17.setText(QCoreApplication.translate("Form", u"Remove", None))
        self.rmSelectedPushButton.setText(QCoreApplication.translate("Form", u"selected", None))
        self.rmAllPushButton.setText(QCoreApplication.translate("Form", u"all", None))
        self.label_26.setText(QCoreApplication.translate("Form", u"interpolate", None))
        self.intSelectedPushButton.setText(QCoreApplication.translate("Form", u"selected", None))
        self.intAllPushButton.setText(QCoreApplication.translate("Form", u"all", None))
        ___qtablewidgetitem3 = self.timeSeriesTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"time", None))
        ___qtablewidgetitem4 = self.timeSeriesTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"intensity", None))
        self.exportPushButton.setText(QCoreApplication.translate("Form", u"Export all time series", None))
        self.showLegendsCheckBox.setText(QCoreApplication.translate("Form", u"show legends", None))
        self.logScaleCheckBox.setText(QCoreApplication.translate("Form", u"y-log scale", None))
        self.rescalePushButton.setText(QCoreApplication.translate("Form", u"autoscale y axis", None))
    # retranslateUi

