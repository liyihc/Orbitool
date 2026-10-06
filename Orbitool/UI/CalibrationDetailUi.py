# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CalibrationDetail.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QHeaderView,
    QLabel, QSizePolicy, QSplitter, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(996, 641)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.calibrationSplitter = QSplitter(Form)
        self.calibrationSplitter.setObjectName(u"calibrationSplitter")
        self.calibrationSplitter.setOrientation(Qt.Horizontal)
        self.calibrationSplitter.setOpaqueResize(True)
        self.calibrationSplitter.setHandleWidth(5)
        self.layoutWidget = QWidget(self.calibrationSplitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout_4 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.spectraTableWidget = QTableWidget(self.layoutWidget)
        if (self.spectraTableWidget.columnCount() < 1):
            self.spectraTableWidget.setColumnCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        self.spectraTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        self.spectraTableWidget.setObjectName(u"spectraTableWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spectraTableWidget.sizePolicy().hasHeightForWidth())
        self.spectraTableWidget.setSizePolicy(sizePolicy)
        self.spectraTableWidget.setMinimumSize(QSize(200, 200))
        self.spectraTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.spectraTableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.spectraTableWidget.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_2.addWidget(self.spectraTableWidget)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_6.addWidget(self.label_4)

        self.spectrumIonsTableWidget = QTableWidget(self.layoutWidget)
        if (self.spectrumIonsTableWidget.columnCount() < 3):
            self.spectrumIonsTableWidget.setColumnCount(3)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.spectrumIonsTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.spectrumIonsTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.spectrumIonsTableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem3)
        self.spectrumIonsTableWidget.setObjectName(u"spectrumIonsTableWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.spectrumIonsTableWidget.sizePolicy().hasHeightForWidth())
        self.spectrumIonsTableWidget.setSizePolicy(sizePolicy1)
        self.spectrumIonsTableWidget.setMinimumSize(QSize(0, 200))
        self.spectrumIonsTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.spectrumIonsTableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.spectrumIonsTableWidget.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_6.addWidget(self.spectrumIonsTableWidget)


        self.horizontalLayout.addLayout(self.verticalLayout_6)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.label)

        self.spectrumPlotWidget = QWidget(self.layoutWidget)
        self.spectrumPlotWidget.setObjectName(u"spectrumPlotWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.spectrumPlotWidget.sizePolicy().hasHeightForWidth())
        self.spectrumPlotWidget.setSizePolicy(sizePolicy2)

        self.verticalLayout_4.addWidget(self.spectrumPlotWidget)

        self.calibrationSplitter.addWidget(self.layoutWidget)
        self.horizontalLayoutWidget = QWidget(self.calibrationSplitter)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.verticalLayout_5 = QVBoxLayout(self.horizontalLayoutWidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_3 = QLabel(self.horizontalLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)

        self.filesTableWidget = QTableWidget(self.horizontalLayoutWidget)
        if (self.filesTableWidget.columnCount() < 2):
            self.filesTableWidget.setColumnCount(2)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.filesTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.filesTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem5)
        self.filesTableWidget.setObjectName(u"filesTableWidget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.filesTableWidget.sizePolicy().hasHeightForWidth())
        self.filesTableWidget.setSizePolicy(sizePolicy3)
        self.filesTableWidget.setMinimumSize(QSize(200, 200))
        self.filesTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.filesTableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.filesTableWidget.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_3.addWidget(self.filesTableWidget)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_5 = QLabel(self.horizontalLayoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_7.addWidget(self.label_5)

        self.fileIonsTableWidget = QTableWidget(self.horizontalLayoutWidget)
        if (self.fileIonsTableWidget.columnCount() < 4):
            self.fileIonsTableWidget.setColumnCount(4)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.fileIonsTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.fileIonsTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.fileIonsTableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.fileIonsTableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem9)
        self.fileIonsTableWidget.setObjectName(u"fileIonsTableWidget")
        sizePolicy1.setHeightForWidth(self.fileIonsTableWidget.sizePolicy().hasHeightForWidth())
        self.fileIonsTableWidget.setSizePolicy(sizePolicy1)
        self.fileIonsTableWidget.setMinimumSize(QSize(0, 200))
        self.fileIonsTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.fileIonsTableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.fileIonsTableWidget.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_7.addWidget(self.fileIonsTableWidget)


        self.horizontalLayout_3.addLayout(self.verticalLayout_7)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)

        self.filePlotWidget = QWidget(self.horizontalLayoutWidget)
        self.filePlotWidget.setObjectName(u"filePlotWidget")
        sizePolicy2.setHeightForWidth(self.filePlotWidget.sizePolicy().hasHeightForWidth())
        self.filePlotWidget.setSizePolicy(sizePolicy2)

        self.verticalLayout_5.addWidget(self.filePlotWidget)

        self.calibrationSplitter.addWidget(self.horizontalLayoutWidget)

        self.verticalLayout.addWidget(self.calibrationSplitter)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Calibration Detail", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Spectra List", None))
        ___qtablewidgetitem = self.spectraTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"time range", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Ions", None))
        ___qtablewidgetitem1 = self.spectrumIonsTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"mz", None))
        ___qtablewidgetitem2 = self.spectrumIonsTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"rtol", None))
        ___qtablewidgetitem3 = self.spectrumIonsTableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"intensity", None))
#if QT_CONFIG(tooltip)
        self.label.setToolTip(QCoreApplication.translate("Form", u"sometimes the position of the highest value of the original peak\n"
" is closer to the calibrated ion,\n"
"but please note that Orbitool  treats the peak as a Gaussian curve,\n"
"so the highest value is not the position of the actual peak", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("Form", u"Tips: the highest value is not the position of the actual peak", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"File List", None))
        ___qtablewidgetitem4 = self.filesTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"create time", None))
        ___qtablewidgetitem5 = self.filesTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Form", u"path", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Ions", None))
        ___qtablewidgetitem6 = self.fileIonsTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Form", u"theoretic mz", None))
        ___qtablewidgetitem7 = self.fileIonsTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Form", u"mz", None))
        ___qtablewidgetitem8 = self.fileIonsTableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Form", u"rtol(ppm)", None))
        ___qtablewidgetitem9 = self.fileIonsTableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("Form", u"use for calibration", None))
    # retranslateUi

