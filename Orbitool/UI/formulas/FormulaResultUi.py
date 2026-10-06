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
    QLabel, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QTableWidget, QTableWidgetItem, QToolButton, QVBoxLayout,
    QWidget)

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
        self.resultTableWidget.setMinimumSize(QSize(600, 0))
        self.resultTableWidget.setMaximumSize(QSize(800, 16777215))
        self.resultTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.resultTableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.resultTableWidget.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_4.addWidget(self.resultTableWidget)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.label)

        self.isotopesTableWidget = QTableWidget(self.centralwidget)
        if (self.isotopesTableWidget.columnCount() < 6):
            self.isotopesTableWidget.setColumnCount(6)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.isotopesTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.isotopesTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.isotopesTableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.isotopesTableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.isotopesTableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.isotopesTableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem9)
        self.isotopesTableWidget.setObjectName(u"isotopesTableWidget")
        self.isotopesTableWidget.setMinimumSize(QSize(600, 0))
        self.isotopesTableWidget.setMaximumSize(QSize(800, 16777215))
        self.isotopesTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.isotopesTableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.isotopesTableWidget.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_4.addWidget(self.isotopesTableWidget)


        self.horizontalLayout.addLayout(self.verticalLayout_4)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.widget)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.showAllToolButton = QToolButton(self.centralwidget)
        self.showAllToolButton.setObjectName(u"showAllToolButton")

        self.horizontalLayout_3.addWidget(self.showAllToolButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.acceptEmptyToolButton = QToolButton(self.centralwidget)
        self.acceptEmptyToolButton.setObjectName(u"acceptEmptyToolButton")

        self.horizontalLayout_2.addWidget(self.acceptEmptyToolButton)

        self.acceptToolButton = QToolButton(self.centralwidget)
        self.acceptToolButton.setObjectName(u"acceptToolButton")

        self.horizontalLayout_2.addWidget(self.acceptToolButton)

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
        self.resultTableWidget.setToolTip(QCoreApplication.translate("MainWindow", u"Double to show isotopes for this formula", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("MainWindow", u"Double-clicking above table will display the natural isotope distribution", None))
        ___qtablewidgetitem4 = self.isotopesTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"formula", None))
        ___qtablewidgetitem5 = self.isotopesTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"mass", None))
        ___qtablewidgetitem6 = self.isotopesTableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"tolerance(ppm)", None))
        ___qtablewidgetitem7 = self.isotopesTableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"abundance", None))
        ___qtablewidgetitem8 = self.isotopesTableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"actual intensity", None))
        ___qtablewidgetitem9 = self.isotopesTableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"actual ratio", None))
#if QT_CONFIG(tooltip)
        self.isotopesTableWidget.setToolTip(QCoreApplication.translate("MainWindow", u"Double click to save formula for peaks", None))
#endif // QT_CONFIG(tooltip)
        self.showAllToolButton.setText(QCoreApplication.translate("MainWindow", u"show all", None))
        self.acceptEmptyToolButton.setText(QCoreApplication.translate("MainWindow", u"Accept empty list", None))
        self.acceptToolButton.setText(QCoreApplication.translate("MainWindow", u"Accept", None))
        self.closeToolButton.setText(QCoreApplication.translate("MainWindow", u"Close", None))
    # retranslateUi

