# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FormulaResult.ui'
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
    QLineEdit, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QTableWidget,
    QTableWidgetItem, QToolButton, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1147, 596)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_4.addWidget(self.lineEdit)

        self.calcPushButton = QPushButton(self.centralwidget)
        self.calcPushButton.setObjectName(u"calcPushButton")

        self.horizontalLayout_4.addWidget(self.calcPushButton)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.resultTableWidget = QTableWidget(self.centralwidget)
        if (self.resultTableWidget.columnCount() < 4):
            self.resultTableWidget.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.resultTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.resultTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.resultTableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.resultTableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.resultTableWidget.setObjectName(u"resultTableWidget")
        self.resultTableWidget.setMinimumSize(QSize(340, 0))
        self.resultTableWidget.setMaximumSize(QSize(560, 16777215))
        self.resultTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.resultTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.resultTableWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.resultTableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.resultTableWidget.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_4.addWidget(self.resultTableWidget)

        self.showDistributionPushButton = QPushButton(self.centralwidget)
        self.showDistributionPushButton.setObjectName(u"showDistributionPushButton")

        self.verticalLayout_4.addWidget(self.showDistributionPushButton)


        self.horizontalLayout.addLayout(self.verticalLayout_4)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.isotopesTableWidget = QTableWidget(self.centralwidget)
        self.isotopesTableWidget.setObjectName(u"isotopesTableWidget")
        self.isotopesTableWidget.setMinimumSize(QSize(360, 0))
        self.isotopesTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.isotopesTableWidget.setSelectionBehavior(QAbstractItemView.SelectColumns)
        self.isotopesTableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.isotopesTableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.verticalLayout_2.addWidget(self.isotopesTableWidget)

        self.editPeakPushButton = QPushButton(self.centralwidget)
        self.editPeakPushButton.setObjectName(u"editPeakPushButton")

        self.verticalLayout_2.addWidget(self.editPeakPushButton)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.deleteToolButton = QToolButton(self.centralwidget)
        self.deleteToolButton.setObjectName(u"deleteToolButton")

        self.horizontalLayout_2.addWidget(self.deleteToolButton)

        self.useSelectedToolButton = QToolButton(self.centralwidget)
        self.useSelectedToolButton.setObjectName(u"useSelectedToolButton")

        self.horizontalLayout_2.addWidget(self.useSelectedToolButton)

        self.closeToolButton = QToolButton(self.centralwidget)
        self.closeToolButton.setObjectName(u"closeToolButton")

        self.horizontalLayout_2.addWidget(self.closeToolButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1147, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Formula Calculation Result", None))
        self.calcPushButton.setText(QCoreApplication.translate("MainWindow", u"Calc", None))
        ___qtablewidgetitem = self.resultTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"formula", None))
        ___qtablewidgetitem1 = self.resultTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"mass", None))
        ___qtablewidgetitem2 = self.resultTableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"tolerance(ppm)", None))
        ___qtablewidgetitem3 = self.resultTableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"unsaturation", None))
#if QT_CONFIG(tooltip)
        self.resultTableWidget.setToolTip(QCoreApplication.translate("MainWindow", u"Double-click a row to show its natural isotope distribution.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.showDistributionPushButton.setToolTip(QCoreApplication.translate("MainWindow", u"Fills the isotope table with the selected formula's natural isotope distribution.", None))
#endif // QT_CONFIG(tooltip)
        self.showDistributionPushButton.setText(QCoreApplication.translate("MainWindow", u"Show actual distribution of selected formula", None))
#if QT_CONFIG(tooltip)
        self.isotopesTableWidget.setToolTip(QCoreApplication.translate("MainWindow", u"Double-click a cell to write that isotope's formula to the nearest peak in the Peak List; the peak may be in another segment.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.editPeakPushButton.setToolTip(QCoreApplication.translate("MainWindow", u"Writes the selected isotope's formula to the nearest peak in the Peak List; the peak may be in another segment.", None))
#endif // QT_CONFIG(tooltip)
        self.editPeakPushButton.setText(QCoreApplication.translate("MainWindow", u"Edit selected peak's formula", None))
        self.deleteToolButton.setText(QCoreApplication.translate("MainWindow", u"Delete formula", None))
        self.useSelectedToolButton.setText(QCoreApplication.translate("MainWindow", u"Use selected formula", None))
        self.closeToolButton.setText(QCoreApplication.translate("MainWindow", u"Close", None))
    # retranslateUi

