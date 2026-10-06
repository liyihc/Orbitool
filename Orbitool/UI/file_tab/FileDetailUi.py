# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FileDetail.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QHeaderView,
    QLabel, QSizePolicy, QSplitter, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(800, 400)
        self.verticalLayout_3 = QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.splitter = QSplitter(Dialog)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.widget = QWidget(self.splitter)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.spectraListTableWidget = QTableWidget(self.widget)
        if (self.spectraListTableWidget.columnCount() < 7):
            self.spectraListTableWidget.setColumnCount(7)
        __qtablewidgetitem = QTableWidgetItem()
        self.spectraListTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.spectraListTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.spectraListTableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.spectraListTableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.spectraListTableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.spectraListTableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.spectraListTableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        self.spectraListTableWidget.setObjectName(u"spectraListTableWidget")
        self.spectraListTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.spectraListTableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.spectraListTableWidget.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.spectraListTableWidget)

        self.splitter.addWidget(self.widget)
        self.widget1 = QWidget(self.splitter)
        self.widget1.setObjectName(u"widget1")
        self.verticalLayout_2 = QVBoxLayout(self.widget1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.widget1)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.filterCountsTableWidget = QTableWidget(self.widget1)
        if (self.filterCountsTableWidget.columnCount() < 2):
            self.filterCountsTableWidget.setColumnCount(2)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.filterCountsTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.filterCountsTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem8)
        self.filterCountsTableWidget.setObjectName(u"filterCountsTableWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filterCountsTableWidget.sizePolicy().hasHeightForWidth())
        self.filterCountsTableWidget.setSizePolicy(sizePolicy)
        self.filterCountsTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.filterCountsTableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.filterCountsTableWidget.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_2.addWidget(self.filterCountsTableWidget)

        self.splitter.addWidget(self.widget1)

        self.verticalLayout_3.addWidget(self.splitter)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"spectra filter list", None))
        ___qtablewidgetitem = self.spectraListTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"rtime", None))
        ___qtablewidgetitem1 = self.spectraListTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"dt", None))
        ___qtablewidgetitem2 = self.spectraListTableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"mass", None))
        ___qtablewidgetitem3 = self.spectraListTableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog", u"polarity", None))
        ___qtablewidgetitem4 = self.spectraListTableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Dialog", u"CiD", None))
        ___qtablewidgetitem5 = self.spectraListTableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Dialog", u"scan", None))
        ___qtablewidgetitem6 = self.spectraListTableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Dialog", u"string", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"filter counts", None))
        ___qtablewidgetitem7 = self.filterCountsTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Dialog", u"count", None))
        ___qtablewidgetitem8 = self.filterCountsTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Dialog", u"filter", None))
    # retranslateUi

