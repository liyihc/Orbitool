# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PeakFitFloat.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLayout,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSpinBox, QStatusBar, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(937, 1000)
        MainWindow.setMinimumSize(QSize(400, 500))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.label_18 = QLabel(self.centralwidget)
        self.label_18.setObjectName(u"label_18")

        self.horizontalLayout_10.addWidget(self.label_18)

        self.originCheckBox = QCheckBox(self.centralwidget)
        self.originCheckBox.setObjectName(u"originCheckBox")
        self.originCheckBox.setChecked(True)

        self.horizontalLayout_10.addWidget(self.originCheckBox)

        self.idealCheckBox = QCheckBox(self.centralwidget)
        self.idealCheckBox.setObjectName(u"idealCheckBox")
        self.idealCheckBox.setChecked(True)

        self.horizontalLayout_10.addWidget(self.idealCheckBox)

        self.sumCheckBox = QCheckBox(self.centralwidget)
        self.sumCheckBox.setObjectName(u"sumCheckBox")
        self.sumCheckBox.setChecked(True)

        self.horizontalLayout_10.addWidget(self.sumCheckBox)

        self.residualCheckBox = QCheckBox(self.centralwidget)
        self.residualCheckBox.setObjectName(u"residualCheckBox")
        self.residualCheckBox.setChecked(True)

        self.horizontalLayout_10.addWidget(self.residualCheckBox)

        self.legendCheckBox = QCheckBox(self.centralwidget)
        self.legendCheckBox.setObjectName(u"legendCheckBox")
        self.legendCheckBox.setChecked(True)

        self.horizontalLayout_10.addWidget(self.legendCheckBox)


        self.verticalLayout.addLayout(self.horizontalLayout_10)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QSize(0, 0))

        self.verticalLayout.addWidget(self.widget)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.intensityTableWidget = QTableWidget(self.centralwidget)
        if (self.intensityTableWidget.columnCount() < 2):
            self.intensityTableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.intensityTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.intensityTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.intensityTableWidget.setObjectName(u"intensityTableWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.intensityTableWidget.sizePolicy().hasHeightForWidth())
        self.intensityTableWidget.setSizePolicy(sizePolicy1)
        self.intensityTableWidget.setMinimumSize(QSize(200, 300))
        self.intensityTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.intensityTableWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.intensityTableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.intensityTableWidget.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_4.addWidget(self.intensityTableWidget)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_13 = QLabel(self.centralwidget)
        self.label_13.setObjectName(u"label_13")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy2)

        self.horizontalLayout_15.addWidget(self.label_13)

        self.spinBox = QSpinBox(self.centralwidget)
        self.spinBox.setObjectName(u"spinBox")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.spinBox.sizePolicy().hasHeightForWidth())
        self.spinBox.setSizePolicy(sizePolicy3)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(20)

        self.horizontalLayout_15.addWidget(self.spinBox)


        self.verticalLayout_4.addLayout(self.horizontalLayout_15)

        self.refitPushButton = QPushButton(self.centralwidget)
        self.refitPushButton.setObjectName(u"refitPushButton")
        sizePolicy3.setHeightForWidth(self.refitPushButton.sizePolicy().hasHeightForWidth())
        self.refitPushButton.setSizePolicy(sizePolicy3)

        self.verticalLayout_4.addWidget(self.refitPushButton)


        self.horizontalLayout_12.addLayout(self.verticalLayout_4)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.peaksTableWidget = QTableWidget(self.groupBox_2)
        if (self.peaksTableWidget.columnCount() < 8):
            self.peaksTableWidget.setColumnCount(8)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.peaksTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.peaksTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.peaksTableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.peaksTableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.peaksTableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.peaksTableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.peaksTableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.peaksTableWidget.setHorizontalHeaderItem(7, __qtablewidgetitem9)
        self.peaksTableWidget.setObjectName(u"peaksTableWidget")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.peaksTableWidget.sizePolicy().hasHeightForWidth())
        self.peaksTableWidget.setSizePolicy(sizePolicy4)
        self.peaksTableWidget.setMinimumSize(QSize(0, 280))
        self.peaksTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.peaksTableWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.peaksTableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.peaksTableWidget.horizontalHeader().setMinimumSectionSize(70)
        self.peaksTableWidget.horizontalHeader().setDefaultSectionSize(100)
        self.peaksTableWidget.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_5.addWidget(self.peaksTableWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.closePushButton = QPushButton(self.groupBox_2)
        self.closePushButton.setObjectName(u"closePushButton")
        sizePolicy3.setHeightForWidth(self.closePushButton.sizePolicy().hasHeightForWidth())
        self.closePushButton.setSizePolicy(sizePolicy3)

        self.horizontalLayout.addWidget(self.closePushButton)

        self.savePushButton = QPushButton(self.groupBox_2)
        self.savePushButton.setObjectName(u"savePushButton")
        sizePolicy3.setHeightForWidth(self.savePushButton.sizePolicy().hasHeightForWidth())
        self.savePushButton.setSizePolicy(sizePolicy3)

        self.horizontalLayout.addWidget(self.savePushButton)


        self.verticalLayout_5.addLayout(self.horizontalLayout)


        self.horizontalLayout_12.addWidget(self.groupBox_2)


        self.verticalLayout.addLayout(self.horizontalLayout_12)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 937, 20))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"show", None))
        self.originCheckBox.setText(QCoreApplication.translate("MainWindow", u"origin", None))
        self.idealCheckBox.setText(QCoreApplication.translate("MainWindow", u"ideal", None))
        self.sumCheckBox.setText(QCoreApplication.translate("MainWindow", u"sum", None))
        self.residualCheckBox.setText(QCoreApplication.translate("MainWindow", u"residual", None))
        self.legendCheckBox.setText(QCoreApplication.translate("MainWindow", u"legend", None))
        ___qtablewidgetitem = self.intensityTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"mz", None))
        ___qtablewidgetitem1 = self.intensityTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"intensity", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"peak num", None))
        self.refitPushButton.setText(QCoreApplication.translate("MainWindow", u"Re-fit", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Peaks", None))
        ___qtablewidgetitem2 = self.peaksTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"position", None))
        ___qtablewidgetitem3 = self.peaksTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"original formula", None))
        ___qtablewidgetitem4 = self.peaksTableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"formula", None))
        ___qtablewidgetitem5 = self.peaksTableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"intensity", None))
        ___qtablewidgetitem6 = self.peaksTableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"ppm", None))
        ___qtablewidgetitem7 = self.peaksTableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"area", None))
        ___qtablewidgetitem8 = self.peaksTableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"isotope ratio", None))
        ___qtablewidgetitem9 = self.peaksTableWidget.horizontalHeaderItem(7)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"ref ratio", None))
        self.closePushButton.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.savePushButton.setText(QCoreApplication.translate("MainWindow", u"Save", None))
    # retranslateUi

