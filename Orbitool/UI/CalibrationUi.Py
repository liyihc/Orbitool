# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Calibration.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QDoubleSpinBox,
    QFormLayout, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QListView, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QSplitter, QTabWidget, QTableWidget, QTableWidgetItem,
    QToolButton, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(743, 516)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.calibrationSplitter = QSplitter(Form)
        self.calibrationSplitter.setObjectName(u"calibrationSplitter")
        self.calibrationSplitter.setOrientation(Qt.Horizontal)
        self.calibrationSplitter.setOpaqueResize(True)
        self.calibrationSplitter.setHandleWidth(5)
        self.layoutWidget = QWidget(self.calibrationSplitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout_10 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.rtolLabel = QLabel(self.layoutWidget)
        self.rtolLabel.setObjectName(u"rtolLabel")

        self.horizontalLayout_2.addWidget(self.rtolLabel)

        self.rtolDoubleSpinBox = QDoubleSpinBox(self.layoutWidget)
        self.rtolDoubleSpinBox.setObjectName(u"rtolDoubleSpinBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rtolDoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.rtolDoubleSpinBox.setSizePolicy(sizePolicy)
        self.rtolDoubleSpinBox.setMinimum(0.010000000000000)
        self.rtolDoubleSpinBox.setMaximum(999.990000000000009)
        self.rtolDoubleSpinBox.setValue(2.000000000000000)

        self.horizontalLayout_2.addWidget(self.rtolDoubleSpinBox)


        self.verticalLayout_10.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.separatorListWidget = QListWidget(self.layoutWidget)
        self.separatorListWidget.setObjectName(u"separatorListWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Ignored)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.separatorListWidget.sizePolicy().hasHeightForWidth())
        self.separatorListWidget.setSizePolicy(sizePolicy1)
        self.separatorListWidget.setMinimumSize(QSize(0, 0))
        self.separatorListWidget.setLayoutDirection(Qt.LeftToRight)
        self.separatorListWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.separatorListWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.separatorListWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.separatorListWidget.setSelectionMode(QAbstractItemView.ContiguousSelection)
        self.separatorListWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.separatorListWidget.setFlow(QListView.LeftToRight)
        self.separatorListWidget.setResizeMode(QListView.Fixed)
        self.separatorListWidget.setLayoutMode(QListView.SinglePass)

        self.horizontalLayout_3.addWidget(self.separatorListWidget)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.separatorDoubleSpinBox = QDoubleSpinBox(self.layoutWidget)
        self.separatorDoubleSpinBox.setObjectName(u"separatorDoubleSpinBox")
        self.separatorDoubleSpinBox.setMaximum(9999.989999999999782)
        self.separatorDoubleSpinBox.setValue(300.000000000000000)

        self.verticalLayout_2.addWidget(self.separatorDoubleSpinBox)

        self.separatorAddPushButton = QPushButton(self.layoutWidget)
        self.separatorAddPushButton.setObjectName(u"separatorAddPushButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.separatorAddPushButton.sizePolicy().hasHeightForWidth())
        self.separatorAddPushButton.setSizePolicy(sizePolicy2)
        self.separatorAddPushButton.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setPointSize(7)
        self.separatorAddPushButton.setFont(font)

        self.verticalLayout_2.addWidget(self.separatorAddPushButton)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)


        self.verticalLayout_10.addLayout(self.horizontalLayout_3)

        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_10.addWidget(self.label_2)

        self.ionsTableWidget = QTableWidget(self.layoutWidget)
        if (self.ionsTableWidget.columnCount() < 2):
            self.ionsTableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.ionsTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.ionsTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.ionsTableWidget.setObjectName(u"ionsTableWidget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.ionsTableWidget.sizePolicy().hasHeightForWidth())
        self.ionsTableWidget.setSizePolicy(sizePolicy3)
        self.ionsTableWidget.setMinimumSize(QSize(300, 0))
        self.ionsTableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.ionsTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ionsTableWidget.setDragEnabled(True)
        self.ionsTableWidget.setDragDropMode(QAbstractItemView.DropOnly)
        self.ionsTableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.ionsTableWidget.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_10.addWidget(self.ionsTableWidget)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.ionLineEdit = QLineEdit(self.layoutWidget)
        self.ionLineEdit.setObjectName(u"ionLineEdit")
        sizePolicy.setHeightForWidth(self.ionLineEdit.sizePolicy().hasHeightForWidth())
        self.ionLineEdit.setSizePolicy(sizePolicy)

        self.horizontalLayout_4.addWidget(self.ionLineEdit)

        self.addIonToolButton = QToolButton(self.layoutWidget)
        self.addIonToolButton.setObjectName(u"addIonToolButton")
        self.addIonToolButton.setMaximumSize(QSize(20, 20))
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        brush1 = QBrush(QColor(0, 85, 0, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush1)
        brush2 = QBrush(QColor(0, 0, 0, 128))
        brush2.setStyle(Qt.BrushStyle.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush2)
#endif
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush1)
        brush3 = QBrush(QColor(0, 0, 0, 128))
        brush3.setStyle(Qt.BrushStyle.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush3)
#endif
        brush4 = QBrush(QColor(120, 120, 120, 255))
        brush4.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush4)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush4)
        brush5 = QBrush(QColor(0, 0, 0, 128))
        brush5.setStyle(Qt.BrushStyle.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush5)
#endif
        self.addIonToolButton.setPalette(palette)
        font1 = QFont()
        font1.setFamilies([u"Consolas"])
        font1.setPointSize(12)
        font1.setBold(True)
        self.addIonToolButton.setFont(font1)

        self.horizontalLayout_4.addWidget(self.addIonToolButton)

        self.delIonToolButton = QToolButton(self.layoutWidget)
        self.delIonToolButton.setObjectName(u"delIonToolButton")
        self.delIonToolButton.setMaximumSize(QSize(20, 20))
        palette1 = QPalette()
        brush6 = QBrush(QColor(170, 0, 0, 255))
        brush6.setStyle(Qt.BrushStyle.SolidPattern)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush6)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush6)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush4)
        self.delIonToolButton.setPalette(palette1)
        self.delIonToolButton.setFont(font1)

        self.horizontalLayout_4.addWidget(self.delIonToolButton)

        self.ionsImportToolButton = QToolButton(self.layoutWidget)
        self.ionsImportToolButton.setObjectName(u"ionsImportToolButton")
        self.ionsImportToolButton.setMaximumSize(QSize(35, 16777215))
        self.ionsImportToolButton.setFont(font)

        self.horizontalLayout_4.addWidget(self.ionsImportToolButton)

        self.ionsExportToolButton = QToolButton(self.layoutWidget)
        self.ionsExportToolButton.setObjectName(u"ionsExportToolButton")
        self.ionsExportToolButton.setMaximumSize(QSize(35, 16777215))
        self.ionsExportToolButton.setFont(font)

        self.horizontalLayout_4.addWidget(self.ionsExportToolButton)


        self.verticalLayout_10.addLayout(self.horizontalLayout_4)

        self.formLayout_6 = QFormLayout()
        self.formLayout_6.setObjectName(u"formLayout_6")
        self.degreeLabel = QLabel(self.layoutWidget)
        self.degreeLabel.setObjectName(u"degreeLabel")

        self.formLayout_6.setWidget(1, QFormLayout.ItemRole.LabelRole, self.degreeLabel)

        self.degreeSpinBox = QSpinBox(self.layoutWidget)
        self.degreeSpinBox.setObjectName(u"degreeSpinBox")
        sizePolicy.setHeightForWidth(self.degreeSpinBox.sizePolicy().hasHeightForWidth())
        self.degreeSpinBox.setSizePolicy(sizePolicy)
        self.degreeSpinBox.setMinimum(1)
        self.degreeSpinBox.setMaximum(5)
        self.degreeSpinBox.setValue(2)

        self.formLayout_6.setWidget(1, QFormLayout.ItemRole.FieldRole, self.degreeSpinBox)

        self.nIonsLabel = QLabel(self.layoutWidget)
        self.nIonsLabel.setObjectName(u"nIonsLabel")

        self.formLayout_6.setWidget(2, QFormLayout.ItemRole.LabelRole, self.nIonsLabel)

        self.nIonsSpinBox = QSpinBox(self.layoutWidget)
        self.nIonsSpinBox.setObjectName(u"nIonsSpinBox")
        sizePolicy.setHeightForWidth(self.nIonsSpinBox.sizePolicy().hasHeightForWidth())
        self.nIonsSpinBox.setSizePolicy(sizePolicy)
        self.nIonsSpinBox.setMinimum(1)
        self.nIonsSpinBox.setMaximum(999)
        self.nIonsSpinBox.setValue(3)

        self.formLayout_6.setWidget(2, QFormLayout.ItemRole.FieldRole, self.nIonsSpinBox)

        self.filterLabel = QLabel(self.layoutWidget)
        self.filterLabel.setObjectName(u"filterLabel")

        self.formLayout_6.setWidget(0, QFormLayout.ItemRole.LabelRole, self.filterLabel)

        self.filterSpinBox = QSpinBox(self.layoutWidget)
        self.filterSpinBox.setObjectName(u"filterSpinBox")
        self.filterSpinBox.setMaximum(100000000)
        self.filterSpinBox.setValue(100)

        self.formLayout_6.setWidget(0, QFormLayout.ItemRole.FieldRole, self.filterSpinBox)

        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.formLayout_6.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.segmentRtolDoubleSpinBox = QDoubleSpinBox(self.layoutWidget)
        self.segmentRtolDoubleSpinBox.setObjectName(u"segmentRtolDoubleSpinBox")
        self.segmentRtolDoubleSpinBox.setMinimum(0.010000000000000)
        self.segmentRtolDoubleSpinBox.setMaximum(999.990000000000009)
        self.segmentRtolDoubleSpinBox.setValue(2.000000000000000)

        self.formLayout_6.setWidget(3, QFormLayout.ItemRole.FieldRole, self.segmentRtolDoubleSpinBox)


        self.verticalLayout_10.addLayout(self.formLayout_6)

        self.calibrationSplitter.addWidget(self.layoutWidget)
        self.tabWidget = QTabWidget(self.calibrationSplitter)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy4)
        self.tabWidget.setTabPosition(QTabWidget.West)
        self.figureTabWidgetPage = QWidget()
        self.figureTabWidgetPage.setObjectName(u"figureTabWidgetPage")
        self.tabWidget.addTab(self.figureTabWidgetPage, "")
        self.tableTabWidgetPage = QWidget()
        self.tableTabWidgetPage.setObjectName(u"tableTabWidgetPage")
        self.verticalLayout_3 = QVBoxLayout(self.tableTabWidgetPage)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.caliInfoTableWidget = QTableWidget(self.tableTabWidgetPage)
        self.caliInfoTableWidget.setObjectName(u"caliInfoTableWidget")
        self.caliInfoTableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.verticalLayout_3.addWidget(self.caliInfoTableWidget)

        self.tabWidget.addTab(self.tableTabWidgetPage, "")
        self.calibrationSplitter.addWidget(self.tabWidget)

        self.verticalLayout.addWidget(self.calibrationSplitter)

        self.calcInfoPushButton = QPushButton(Form)
        self.calcInfoPushButton.setObjectName(u"calcInfoPushButton")
        sizePolicy.setHeightForWidth(self.calcInfoPushButton.sizePolicy().hasHeightForWidth())
        self.calcInfoPushButton.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.calcInfoPushButton)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.showDetailsPushButton = QPushButton(Form)
        self.showDetailsPushButton.setObjectName(u"showDetailsPushButton")
        sizePolicy.setHeightForWidth(self.showDetailsPushButton.sizePolicy().hasHeightForWidth())
        self.showDetailsPushButton.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.showDetailsPushButton)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.finishPushButton = QPushButton(Form)
        self.finishPushButton.setObjectName(u"finishPushButton")
        sizePolicy.setHeightForWidth(self.finishPushButton.sizePolicy().hasHeightForWidth())
        self.finishPushButton.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.finishPushButton)

        self.skipPushButton = QPushButton(Form)
        self.skipPushButton.setObjectName(u"skipPushButton")

        self.horizontalLayout.addWidget(self.skipPushButton)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Segments", None))
#if QT_CONFIG(tooltip)
        self.rtolLabel.setToolTip(QCoreApplication.translate("Form", u"used to average spectra\n"
"used to cut spectrum by separators", None))
#endif // QT_CONFIG(tooltip)
        self.rtolLabel.setText(QCoreApplication.translate("Form", u"tolerance(ppm)", None))
#if QT_CONFIG(tooltip)
        self.separatorAddPushButton.setToolTip(QCoreApplication.translate("Form", u"You can select multiple adjacent segments and choose Merge in the context menu", None))
#endif // QT_CONFIG(tooltip)
        self.separatorAddPushButton.setText(QCoreApplication.translate("Form", u"separate", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Current Segment Ions", None))
        ___qtablewidgetitem = self.ionsTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"Ions", None))
        ___qtablewidgetitem1 = self.ionsTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"Mass", None))
        self.ionLineEdit.setPlaceholderText(QCoreApplication.translate("Form", u"HNO3O3-, C6H3O2NNO3, C6H5O3NNO3-", None))
        self.addIonToolButton.setText(QCoreApplication.translate("Form", u"+", None))
#if QT_CONFIG(shortcut)
        self.addIonToolButton.setShortcut(QCoreApplication.translate("Form", u"+", None))
#endif // QT_CONFIG(shortcut)
        self.delIonToolButton.setText(QCoreApplication.translate("Form", u"-", None))
#if QT_CONFIG(shortcut)
        self.delIonToolButton.setShortcut(QCoreApplication.translate("Form", u"Del", None))
#endif // QT_CONFIG(shortcut)
        self.ionsImportToolButton.setText(QCoreApplication.translate("Form", u"Import", None))
        self.ionsExportToolButton.setText(QCoreApplication.translate("Form", u"Export", None))
        self.degreeLabel.setText(QCoreApplication.translate("Form", u"polynomial degree", None))
        self.nIonsLabel.setText(QCoreApplication.translate("Form", u"use best N ions", None))
        self.filterLabel.setText(QCoreApplication.translate("Form", u"intensity filter", None))
#if QT_CONFIG(tooltip)
        self.label_3.setToolTip(QCoreApplication.translate("Form", u"used to find peaks within this rtol around ions", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("Form", u"tolerance(ppm)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.figureTabWidgetPage), QCoreApplication.translate("Form", u"Figure", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tableTabWidgetPage), QCoreApplication.translate("Form", u"Table", None))
#if QT_CONFIG(tooltip)
        self.calcInfoPushButton.setToolTip(QCoreApplication.translate("Form", u"Alt+C", None))
#endif // QT_CONFIG(tooltip)
        self.calcInfoPushButton.setText(QCoreApplication.translate("Form", u"&Calc calibrate info", None))
#if QT_CONFIG(shortcut)
        self.calcInfoPushButton.setShortcut(QCoreApplication.translate("Form", u"Alt+C", None))
#endif // QT_CONFIG(shortcut)
        self.showDetailsPushButton.setText(QCoreApplication.translate("Form", u"Show details", None))
#if QT_CONFIG(tooltip)
        self.finishPushButton.setToolTip(QCoreApplication.translate("Form", u"Return Key", None))
#endif // QT_CONFIG(tooltip)
        self.finishPushButton.setText(QCoreApplication.translate("Form", u"Calibrate and continue", None))
#if QT_CONFIG(shortcut)
        self.finishPushButton.setShortcut(QCoreApplication.translate("Form", u"Return", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.skipPushButton.setToolTip(QCoreApplication.translate("Form", u"Alt+P", None))
#endif // QT_CONFIG(tooltip)
        self.skipPushButton.setText(QCoreApplication.translate("Form", u"Ski&p calibration", None))
#if QT_CONFIG(shortcut)
        self.skipPushButton.setShortcut(QCoreApplication.translate("Form", u"Alt+P", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

