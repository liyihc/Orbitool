# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'File.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QCheckBox,
    QDateTimeEdit, QDoubleSpinBox, QFormLayout, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QRadioButton, QScrollArea,
    QSizePolicy, QSpacerItem, QSpinBox, QTableWidget,
    QTableWidgetItem, QToolButton, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(699, 479)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.addFilePushButton = QPushButton(Form)
        self.addFilePushButton.setObjectName(u"addFilePushButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addFilePushButton.sizePolicy().hasHeightForWidth())
        self.addFilePushButton.setSizePolicy(sizePolicy)

        self.verticalLayout_5.addWidget(self.addFilePushButton)

        self.addFolderPushButton = QPushButton(Form)
        self.addFolderPushButton.setObjectName(u"addFolderPushButton")
        sizePolicy.setHeightForWidth(self.addFolderPushButton.sizePolicy().hasHeightForWidth())
        self.addFolderPushButton.setSizePolicy(sizePolicy)

        self.verticalLayout_5.addWidget(self.addFolderPushButton)

        self.recursionCheckBox = QCheckBox(Form)
        self.recursionCheckBox.setObjectName(u"recursionCheckBox")
        self.recursionCheckBox.setChecked(True)

        self.verticalLayout_5.addWidget(self.recursionCheckBox)

        self.verticalSpacer_3 = QSpacerItem(20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_5.addItem(self.verticalSpacer_3)

        self.removeFilePushButton = QPushButton(Form)
        self.removeFilePushButton.setObjectName(u"removeFilePushButton")
        sizePolicy.setHeightForWidth(self.removeFilePushButton.sizePolicy().hasHeightForWidth())
        self.removeFilePushButton.setSizePolicy(sizePolicy)

        self.verticalLayout_5.addWidget(self.removeFilePushButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout_5)

        self.tableWidget = QTableWidget(Form)
        if (self.tableWidget.columnCount() < 5):
            self.tableWidget.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setDragEnabled(True)
        self.tableWidget.setDragDropMode(QAbstractItemView.DropOnly)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.tableWidget.setTextElideMode(Qt.ElideNone)
        self.tableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(150)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.horizontalLayout.addWidget(self.tableWidget)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.scrollArea = QScrollArea(Form)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMaximumSize(QSize(300, 16777215))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 277, 410))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName(u"groupBox")
        self.formLayout = QFormLayout(self.groupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_7)

        self.startDateTimeEdit = QDateTimeEdit(self.groupBox)
        self.startDateTimeEdit.setObjectName(u"startDateTimeEdit")
        sizePolicy.setHeightForWidth(self.startDateTimeEdit.sizePolicy().hasHeightForWidth())
        self.startDateTimeEdit.setSizePolicy(sizePolicy)
        self.startDateTimeEdit.setMaximumDateTime(QDateTime(QDate(9999, 12, 31), QTime(23, 59, 59)))
        self.startDateTimeEdit.setCalendarPopup(True)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.startDateTimeEdit)

        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_8)

        self.endDateTimeEdit = QDateTimeEdit(self.groupBox)
        self.endDateTimeEdit.setObjectName(u"endDateTimeEdit")
        sizePolicy.setHeightForWidth(self.endDateTimeEdit.sizePolicy().hasHeightForWidth())
        self.endDateTimeEdit.setSizePolicy(sizePolicy)
        self.endDateTimeEdit.setCalendarPopup(True)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.endDateTimeEdit)

        self.autoTimeCheckBox = QCheckBox(self.groupBox)
        self.autoTimeCheckBox.setObjectName(u"autoTimeCheckBox")
        self.autoTimeCheckBox.setChecked(True)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.autoTimeCheckBox)

        self.timeAdjustPushButton = QPushButton(self.groupBox)
        self.timeAdjustPushButton.setObjectName(u"timeAdjustPushButton")
        self.timeAdjustPushButton.setMaximumSize(QSize(16777215, 20))

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.timeAdjustPushButton)


        self.verticalLayout_3.addWidget(self.groupBox)

        self.averageGroupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.averageGroupBox.setObjectName(u"averageGroupBox")
        self.averageGroupBox.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.averageGroupBox.sizePolicy().hasHeightForWidth())
        self.averageGroupBox.setSizePolicy(sizePolicy1)
        self.averageGroupBox.setCheckable(True)
        self.averageGroupBox.setChecked(True)
        self.gridLayout = QGridLayout(self.averageGroupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(3)
        self.gridLayout.setContentsMargins(9, 9, 9, 9)
        self.periodToolButton = QToolButton(self.averageGroupBox)
        self.periodToolButton.setObjectName(u"periodToolButton")
        sizePolicy.setHeightForWidth(self.periodToolButton.sizePolicy().hasHeightForWidth())
        self.periodToolButton.setSizePolicy(sizePolicy)
        self.periodToolButton.setMaximumSize(QSize(16777215, 20))

        self.gridLayout.addWidget(self.periodToolButton, 2, 1, 1, 1)

        self.label = QLabel(self.averageGroupBox)
        self.label.setObjectName(u"label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.label, 0, 2, 1, 1)

        self.nMinutesLineEdit = QLineEdit(self.averageGroupBox)
        self.nMinutesLineEdit.setObjectName(u"nMinutesLineEdit")
        sizePolicy.setHeightForWidth(self.nMinutesLineEdit.sizePolicy().hasHeightForWidth())
        self.nMinutesLineEdit.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.nMinutesLineEdit, 1, 1, 1, 2)

        self.label_4 = QLabel(self.averageGroupBox)
        self.label_4.setObjectName(u"label_4")
        sizePolicy2.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.label_4, 2, 2, 1, 1)

        self.nMinutesRadioButton = QRadioButton(self.averageGroupBox)
        self.nMinutesRadioButton.setObjectName(u"nMinutesRadioButton")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.nMinutesRadioButton.sizePolicy().hasHeightForWidth())
        self.nMinutesRadioButton.setSizePolicy(sizePolicy3)
        self.nMinutesRadioButton.setChecked(True)

        self.gridLayout.addWidget(self.nMinutesRadioButton, 1, 0, 1, 1)

        self.nSpectraSpinBox = QSpinBox(self.averageGroupBox)
        self.nSpectraSpinBox.setObjectName(u"nSpectraSpinBox")
        sizePolicy.setHeightForWidth(self.nSpectraSpinBox.sizePolicy().hasHeightForWidth())
        self.nSpectraSpinBox.setSizePolicy(sizePolicy)
        self.nSpectraSpinBox.setMaximumSize(QSize(16777215, 18))
        self.nSpectraSpinBox.setMinimum(1)
        self.nSpectraSpinBox.setMaximum(9999)
        self.nSpectraSpinBox.setValue(10)

        self.gridLayout.addWidget(self.nSpectraSpinBox, 0, 1, 1, 1)

        self.nSpectraRadioButton = QRadioButton(self.averageGroupBox)
        self.nSpectraRadioButton.setObjectName(u"nSpectraRadioButton")
        self.nSpectraRadioButton.setEnabled(True)
        sizePolicy3.setHeightForWidth(self.nSpectraRadioButton.sizePolicy().hasHeightForWidth())
        self.nSpectraRadioButton.setSizePolicy(sizePolicy3)
        self.nSpectraRadioButton.setChecked(False)

        self.gridLayout.addWidget(self.nSpectraRadioButton, 0, 0, 1, 1)

        self.periodRadioButton = QRadioButton(self.averageGroupBox)
        self.periodRadioButton.setObjectName(u"periodRadioButton")
        sizePolicy3.setHeightForWidth(self.periodRadioButton.sizePolicy().hasHeightForWidth())
        self.periodRadioButton.setSizePolicy(sizePolicy3)
        self.periodRadioButton.setChecked(False)

        self.gridLayout.addWidget(self.periodRadioButton, 2, 0, 1, 1)


        self.verticalLayout_3.addWidget(self.averageGroupBox)

        self.groupBox_6 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_6.setObjectName(u"groupBox_6")
        sizePolicy1.setHeightForWidth(self.groupBox_6.sizePolicy().hasHeightForWidth())
        self.groupBox_6.setSizePolicy(sizePolicy1)
        self.verticalLayout = QVBoxLayout(self.groupBox_6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.refreshFilterPushButton = QPushButton(self.groupBox_6)
        self.refreshFilterPushButton.setObjectName(u"refreshFilterPushButton")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.refreshFilterPushButton.sizePolicy().hasHeightForWidth())
        self.refreshFilterPushButton.setSizePolicy(sizePolicy4)
        self.refreshFilterPushButton.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout.addWidget(self.refreshFilterPushButton)

        self.filterTableWidget = QTableWidget(self.groupBox_6)
        if (self.filterTableWidget.columnCount() < 3):
            self.filterTableWidget.setColumnCount(3)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.filterTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.filterTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.filterTableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem7)
        self.filterTableWidget.setObjectName(u"filterTableWidget")
        self.filterTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.filterTableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.filterTableWidget.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.filterTableWidget)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.addFilterToolButton = QToolButton(self.groupBox_6)
        self.addFilterToolButton.setObjectName(u"addFilterToolButton")
        self.addFilterToolButton.setMaximumSize(QSize(20, 20))
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
        self.addFilterToolButton.setPalette(palette)
        font = QFont()
        font.setFamilies([u"Consolas"])
        font.setPointSize(12)
        font.setBold(True)
        self.addFilterToolButton.setFont(font)

        self.horizontalLayout_3.addWidget(self.addFilterToolButton)

        self.delFilterToolButton = QToolButton(self.groupBox_6)
        self.delFilterToolButton.setObjectName(u"delFilterToolButton")
        self.delFilterToolButton.setMaximumSize(QSize(20, 20))
        palette1 = QPalette()
        brush6 = QBrush(QColor(170, 0, 0, 255))
        brush6.setStyle(Qt.BrushStyle.SolidPattern)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush6)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush6)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush4)
        self.delFilterToolButton.setPalette(palette1)
        self.delFilterToolButton.setFont(font)

        self.horizontalLayout_3.addWidget(self.delFilterToolButton)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.verticalLayout_3.addWidget(self.groupBox_6)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_2.addWidget(self.scrollArea)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.rtolLabel = QLabel(Form)
        self.rtolLabel.setObjectName(u"rtolLabel")

        self.horizontalLayout_4.addWidget(self.rtolLabel)

        self.rtolDoubleSpinBox = QDoubleSpinBox(Form)
        self.rtolDoubleSpinBox.setObjectName(u"rtolDoubleSpinBox")
        sizePolicy.setHeightForWidth(self.rtolDoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.rtolDoubleSpinBox.setSizePolicy(sizePolicy)
        self.rtolDoubleSpinBox.setMinimum(0.010000000000000)
        self.rtolDoubleSpinBox.setMaximum(99.989999999999995)
        self.rtolDoubleSpinBox.setSingleStep(0.500000000000000)
        self.rtolDoubleSpinBox.setValue(1.000000000000000)

        self.horizontalLayout_4.addWidget(self.rtolDoubleSpinBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)


        self.verticalLayout_6.addLayout(self.verticalLayout_2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_5.addWidget(self.label_2)

        self.selectedPushButton = QPushButton(Form)
        self.selectedPushButton.setObjectName(u"selectedPushButton")
        sizePolicy.setHeightForWidth(self.selectedPushButton.sizePolicy().hasHeightForWidth())
        self.selectedPushButton.setSizePolicy(sizePolicy)
        self.selectedPushButton.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_5.addWidget(self.selectedPushButton)

        self.allPushButton = QPushButton(Form)
        self.allPushButton.setObjectName(u"allPushButton")
        sizePolicy.setHeightForWidth(self.allPushButton.sizePolicy().hasHeightForWidth())
        self.allPushButton.setSizePolicy(sizePolicy)
        self.allPushButton.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_5.addWidget(self.allPushButton)


        self.verticalLayout_6.addLayout(self.horizontalLayout_5)


        self.horizontalLayout.addLayout(self.verticalLayout_6)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
#if QT_CONFIG(tooltip)
        self.addFilePushButton.setToolTip(QCoreApplication.translate("Form", u"Alt+I", None))
#endif // QT_CONFIG(tooltip)
        self.addFilePushButton.setText(QCoreApplication.translate("Form", u"&Import file(s)", None))
#if QT_CONFIG(shortcut)
        self.addFilePushButton.setShortcut(QCoreApplication.translate("Form", u"Alt+I", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.addFolderPushButton.setToolTip(QCoreApplication.translate("Form", u"Alt+F", None))
#endif // QT_CONFIG(tooltip)
        self.addFolderPushButton.setText(QCoreApplication.translate("Form", u"Import &folder", None))
#if QT_CONFIG(shortcut)
        self.addFolderPushButton.setShortcut(QCoreApplication.translate("Form", u"Alt+F", None))
#endif // QT_CONFIG(shortcut)
        self.recursionCheckBox.setText(QCoreApplication.translate("Form", u"Subdirectory", None))
#if QT_CONFIG(tooltip)
        self.removeFilePushButton.setToolTip(QCoreApplication.translate("Form", u"Del Key", None))
#endif // QT_CONFIG(tooltip)
        self.removeFilePushButton.setText(QCoreApplication.translate("Form", u"Remove selected", None))
#if QT_CONFIG(shortcut)
        self.removeFilePushButton.setShortcut(QCoreApplication.translate("Form", u"Del", None))
#endif // QT_CONFIG(shortcut)
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"Name", None))
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"Start time", None))
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"End time", None))
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"Scan num", None))
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"Path", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Use time range", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"from", None))
        self.startDateTimeEdit.setDisplayFormat(QCoreApplication.translate("Form", u"yyyy/M/d H:mm:ss", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"to", None))
        self.endDateTimeEdit.setDisplayFormat(QCoreApplication.translate("Form", u"yyyy/M/d H:mm:ss", None))
        self.autoTimeCheckBox.setText(QCoreApplication.translate("Form", u"auto", None))
        self.timeAdjustPushButton.setText(QCoreApplication.translate("Form", u"adjust to selected files", None))
        self.averageGroupBox.setTitle(QCoreApplication.translate("Form", u"Average", None))
        self.periodToolButton.setText(QCoreApplication.translate("Form", u"custom", None))
        self.label.setText(QCoreApplication.translate("Form", u"spectra", None))
#if QT_CONFIG(tooltip)
        self.nMinutesLineEdit.setToolTip(QCoreApplication.translate("Form", u"1000s ( 1000 seconds )\n"
"10m5s ( 10 minutes and 5 seconds )\n"
"1h ( 1 hour )", None))
#endif // QT_CONFIG(tooltip)
        self.nMinutesLineEdit.setText(QCoreApplication.translate("Form", u"2h5m", None))
        self.nMinutesLineEdit.setPlaceholderText(QCoreApplication.translate("Form", u"2h5m", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"periods", None))
        self.nMinutesRadioButton.setText(QCoreApplication.translate("Form", u"every", None))
        self.nSpectraRadioButton.setText(QCoreApplication.translate("Form", u"every", None))
        self.periodRadioButton.setText("")
        self.groupBox_6.setTitle(QCoreApplication.translate("Form", u"Spectrum filters", None))
        self.refreshFilterPushButton.setText(QCoreApplication.translate("Form", u"refresh filter", None))
        ___qtablewidgetitem5 = self.filterTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Form", u"property", None))
        ___qtablewidgetitem6 = self.filterTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Form", u"operator", None))
        ___qtablewidgetitem7 = self.filterTableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Form", u"value", None))
        self.addFilterToolButton.setText(QCoreApplication.translate("Form", u"+", None))
#if QT_CONFIG(shortcut)
        self.addFilterToolButton.setShortcut(QCoreApplication.translate("Form", u"+", None))
#endif // QT_CONFIG(shortcut)
        self.delFilterToolButton.setText(QCoreApplication.translate("Form", u"-", None))
#if QT_CONFIG(shortcut)
        self.delFilterToolButton.setShortcut(QCoreApplication.translate("Form", u"Del", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.rtolLabel.setToolTip(QCoreApplication.translate("Form", u"When averaging scans, peaks from different scans are merged only if their m/z agree within this \u00b1ppm.", None))
#endif // QT_CONFIG(tooltip)
        self.rtolLabel.setText(QCoreApplication.translate("Form", u"tolerance(ppm)", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Show spectra for", None))
#if QT_CONFIG(tooltip)
        self.selectedPushButton.setToolTip(QCoreApplication.translate("Form", u"Alt+S", None))
#endif // QT_CONFIG(tooltip)
        self.selectedPushButton.setText(QCoreApplication.translate("Form", u"&Selected file(s)", None))
#if QT_CONFIG(shortcut)
        self.selectedPushButton.setShortcut(QCoreApplication.translate("Form", u"Alt+S", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.allPushButton.setToolTip(QCoreApplication.translate("Form", u"Return Key", None))
#endif // QT_CONFIG(tooltip)
        self.allPushButton.setText(QCoreApplication.translate("Form", u"&All file(s)", None))
#if QT_CONFIG(shortcut)
        self.allPushButton.setShortcut(QCoreApplication.translate("Form", u"Return", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

