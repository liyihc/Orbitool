# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SpectraList.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QComboBox,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(274, 300)
        Form.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.comboBox = QComboBox(Form)
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout_2.addWidget(self.comboBox)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.tableWidget = QTableWidget(Form)
        if (self.tableWidget.columnCount() < 2):
            self.tableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setMaximumSize(QSize(16777215, 16777215))
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.tableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.tableWidget)

        self.groupBox_export = QGroupBox(Form)
        self.groupBox_export.setObjectName(u"groupBox_export")
        self.horizontalLayout_export = QHBoxLayout(self.groupBox_export)
        self.horizontalLayout_export.setObjectName(u"horizontalLayout_export")
        self.exportSelectPushButton = QPushButton(self.groupBox_export)
        self.exportSelectPushButton.setObjectName(u"exportSelectPushButton")

        self.horizontalLayout_export.addWidget(self.exportSelectPushButton)

        self.exportAllPushButton = QPushButton(self.groupBox_export)
        self.exportAllPushButton.setObjectName(u"exportAllPushButton")

        self.horizontalLayout_export.addWidget(self.exportAllPushButton)

        self.exportNoiseLODPushButton = QPushButton(self.groupBox_export)
        self.exportNoiseLODPushButton.setObjectName(u"exportNoiseLODPushButton")

        self.horizontalLayout_export.addWidget(self.exportNoiseLODPushButton)


        self.verticalLayout.addWidget(self.groupBox_export)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"show spectra after", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"start time", None))
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"end time", None))
        self.groupBox_export.setTitle(QCoreApplication.translate("Form", u"Export", None))
        self.exportSelectPushButton.setText(QCoreApplication.translate("Form", u"Select spectra", None))
        self.exportAllPushButton.setText(QCoreApplication.translate("Form", u"All spectra", None))
        self.exportNoiseLODPushButton.setText(QCoreApplication.translate("Form", u"Noise results", None))
    # retranslateUi

