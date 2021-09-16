# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Orbitool\UI\PeakFitFloat.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(937, 1000)
        MainWindow.setMinimumSize(QtCore.QSize(400, 500))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_10.addWidget(self.label_18)
        self.originCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.originCheckBox.setChecked(True)
        self.originCheckBox.setObjectName("originCheckBox")
        self.horizontalLayout_10.addWidget(self.originCheckBox)
        self.idealCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.idealCheckBox.setChecked(True)
        self.idealCheckBox.setObjectName("idealCheckBox")
        self.horizontalLayout_10.addWidget(self.idealCheckBox)
        self.sumCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.sumCheckBox.setChecked(True)
        self.sumCheckBox.setObjectName("sumCheckBox")
        self.horizontalLayout_10.addWidget(self.sumCheckBox)
        self.residualCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.residualCheckBox.setChecked(True)
        self.residualCheckBox.setObjectName("residualCheckBox")
        self.horizontalLayout_10.addWidget(self.residualCheckBox)
        self.legendCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.legendCheckBox.setChecked(True)
        self.legendCheckBox.setObjectName("legendCheckBox")
        self.horizontalLayout_10.addWidget(self.legendCheckBox)
        self.verticalLayout.addLayout(self.horizontalLayout_10)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(0, 0))
        self.widget.setObjectName("widget")
        self.verticalLayout.addWidget(self.widget)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.intensityTableWidget = QtWidgets.QTableWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.intensityTableWidget.sizePolicy().hasHeightForWidth())
        self.intensityTableWidget.setSizePolicy(sizePolicy)
        self.intensityTableWidget.setMinimumSize(QtCore.QSize(200, 300))
        self.intensityTableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.intensityTableWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.intensityTableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.intensityTableWidget.setObjectName("intensityTableWidget")
        self.intensityTableWidget.setColumnCount(2)
        self.intensityTableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.intensityTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.intensityTableWidget.setHorizontalHeaderItem(1, item)
        self.intensityTableWidget.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_4.addWidget(self.intensityTableWidget)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_15.addWidget(self.label_13)
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox.sizePolicy().hasHeightForWidth())
        self.spinBox.setSizePolicy(sizePolicy)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(20)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout_15.addWidget(self.spinBox)
        self.verticalLayout_4.addLayout(self.horizontalLayout_15)
        self.refitPushButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refitPushButton.sizePolicy().hasHeightForWidth())
        self.refitPushButton.setSizePolicy(sizePolicy)
        self.refitPushButton.setObjectName("refitPushButton")
        self.verticalLayout_4.addWidget(self.refitPushButton)
        self.horizontalLayout_12.addLayout(self.verticalLayout_4)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.peaksTableWidget = QtWidgets.QTableWidget(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.peaksTableWidget.sizePolicy().hasHeightForWidth())
        self.peaksTableWidget.setSizePolicy(sizePolicy)
        self.peaksTableWidget.setMinimumSize(QtCore.QSize(0, 280))
        self.peaksTableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.peaksTableWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.peaksTableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.peaksTableWidget.setObjectName("peaksTableWidget")
        self.peaksTableWidget.setColumnCount(8)
        self.peaksTableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.peaksTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.peaksTableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.peaksTableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.peaksTableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.peaksTableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.peaksTableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.peaksTableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.peaksTableWidget.setHorizontalHeaderItem(7, item)
        self.peaksTableWidget.horizontalHeader().setDefaultSectionSize(100)
        self.peaksTableWidget.horizontalHeader().setMinimumSectionSize(70)
        self.peaksTableWidget.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_5.addWidget(self.peaksTableWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.closePushButton = QtWidgets.QPushButton(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.closePushButton.sizePolicy().hasHeightForWidth())
        self.closePushButton.setSizePolicy(sizePolicy)
        self.closePushButton.setObjectName("closePushButton")
        self.horizontalLayout.addWidget(self.closePushButton)
        self.savePushButton = QtWidgets.QPushButton(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.savePushButton.sizePolicy().hasHeightForWidth())
        self.savePushButton.setSizePolicy(sizePolicy)
        self.savePushButton.setObjectName("savePushButton")
        self.horizontalLayout.addWidget(self.savePushButton)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.horizontalLayout_12.addWidget(self.groupBox_2)
        self.verticalLayout.addLayout(self.horizontalLayout_12)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 937, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_18.setText(_translate("MainWindow", "show"))
        self.originCheckBox.setText(_translate("MainWindow", "origin"))
        self.idealCheckBox.setText(_translate("MainWindow", "ideal"))
        self.sumCheckBox.setText(_translate("MainWindow", "sum"))
        self.residualCheckBox.setText(_translate("MainWindow", "residual"))
        self.legendCheckBox.setText(_translate("MainWindow", "legend"))
        item = self.intensityTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "mz"))
        item = self.intensityTableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "intensity"))
        self.label_13.setText(_translate("MainWindow", "peak num"))
        self.refitPushButton.setText(_translate("MainWindow", "Re-fit"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Peaks"))
        item = self.peaksTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "position"))
        item = self.peaksTableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "original formula"))
        item = self.peaksTableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "formula"))
        item = self.peaksTableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "intensity"))
        item = self.peaksTableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "ppm"))
        item = self.peaksTableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "area"))
        item = self.peaksTableWidget.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "isotope ratio"))
        item = self.peaksTableWidget.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "ref ratio"))
        self.closePushButton.setText(_translate("MainWindow", "Close"))
        self.savePushButton.setText(_translate("MainWindow", "Save"))

