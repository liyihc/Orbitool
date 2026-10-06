# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Noise.ui'
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
    QFormLayout, QFrame, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QSplitter, QTableWidget,
    QTableWidgetItem, QToolBox, QToolButton, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(784, 461)
        self.verticalLayout_4 = QVBoxLayout(Form)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.splitter = QSplitter(Form)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.showAveragePushButton = QPushButton(self.layoutWidget)
        self.showAveragePushButton.setObjectName(u"showAveragePushButton")

        self.verticalLayout.addWidget(self.showAveragePushButton)

        self.toolBox = QToolBox(self.layoutWidget)
        self.toolBox.setObjectName(u"toolBox")
        self.toolBox.setMinimumSize(QSize(285, 0))
        self.toolBox.setMaximumSize(QSize(16777215, 16777215))
        self.toolBox.setBaseSize(QSize(285, 0))
        self.toolBox.setFrameShape(QFrame.Box)
        self.toolBox.setFrameShadow(QFrame.Raised)
        self.noiseTool = QWidget()
        self.noiseTool.setObjectName(u"noiseTool")
        self.noiseTool.setGeometry(QRect(0, 0, 318, 271))
        self.verticalLayout_2 = QVBoxLayout(self.noiseTool)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.noiseTool)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.quantileDoubleSpinBox = QDoubleSpinBox(self.noiseTool)
        self.quantileDoubleSpinBox.setObjectName(u"quantileDoubleSpinBox")
        self.quantileDoubleSpinBox.setValue(0.900000000000000)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.quantileDoubleSpinBox)

        self.label_2 = QLabel(self.noiseTool)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.nSigmaDoubleSpinBox = QDoubleSpinBox(self.noiseTool)
        self.nSigmaDoubleSpinBox.setObjectName(u"nSigmaDoubleSpinBox")
        self.nSigmaDoubleSpinBox.setValue(3.000000000000000)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.nSigmaDoubleSpinBox)

        self.line = QFrame(self.noiseTool)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.SpanningRole, self.line)

        self.sizeDependentLabel = QLabel(self.noiseTool)
        self.sizeDependentLabel.setObjectName(u"sizeDependentLabel")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.sizeDependentLabel)

        self.sizeDependentCheckBox = QCheckBox(self.noiseTool)
        self.sizeDependentCheckBox.setObjectName(u"sizeDependentCheckBox")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.sizeDependentCheckBox)


        self.verticalLayout_2.addLayout(self.formLayout)

        self.groupBox_2 = QGroupBox(self.noiseTool)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.tableWidget = QTableWidget(self.groupBox_2)
        if (self.tableWidget.columnCount() < 3):
            self.tableWidget.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_6.addWidget(self.tableWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit = QLineEdit(self.groupBox_2)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.lineEdit)

        self.addPushButton = QPushButton(self.groupBox_2)
        self.addPushButton.setObjectName(u"addPushButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.addPushButton.sizePolicy().hasHeightForWidth())
        self.addPushButton.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.addPushButton)

        self.delPushButton = QPushButton(self.groupBox_2)
        self.delPushButton.setObjectName(u"delPushButton")
        sizePolicy1.setHeightForWidth(self.delPushButton.sizePolicy().hasHeightForWidth())
        self.delPushButton.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.delPushButton)


        self.verticalLayout_6.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.calculateNoisePushButton = QPushButton(self.noiseTool)
        self.calculateNoisePushButton.setObjectName(u"calculateNoisePushButton")

        self.verticalLayout_2.addWidget(self.calculateNoisePushButton)

        self.toolBox.addItem(self.noiseTool, u"Noise inputs")
        self.paramTool = QWidget()
        self.paramTool.setObjectName(u"paramTool")
        self.paramTool.setGeometry(QRect(0, 0, 242, 190))
        self.verticalLayout_3 = QVBoxLayout(self.paramTool)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.paramTableWidget = QTableWidget(self.paramTool)
        if (self.paramTableWidget.columnCount() < 4):
            self.paramTableWidget.setColumnCount(4)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.paramTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.paramTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.paramTableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.paramTableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem6)
        self.paramTableWidget.setObjectName(u"paramTableWidget")
        self.paramTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.paramTableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.paramTableWidget.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_3.addWidget(self.paramTableWidget)

        self.recalculateNoisePushButton = QPushButton(self.paramTool)
        self.recalculateNoisePushButton.setObjectName(u"recalculateNoisePushButton")

        self.verticalLayout_3.addWidget(self.recalculateNoisePushButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.groupBox = QGroupBox(self.paramTool)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.exportDenoisedSpectrumPushButton = QPushButton(self.groupBox)
        self.exportDenoisedSpectrumPushButton.setObjectName(u"exportDenoisedSpectrumPushButton")

        self.horizontalLayout_4.addWidget(self.exportDenoisedSpectrumPushButton)

        self.exportNoisePeaksPushButton = QPushButton(self.groupBox)
        self.exportNoisePeaksPushButton.setObjectName(u"exportNoisePeaksPushButton")

        self.horizontalLayout_4.addWidget(self.exportNoisePeaksPushButton)


        self.verticalLayout_3.addWidget(self.groupBox)

        self.toolBox.addItem(self.paramTool, u"Noise results")

        self.verticalLayout.addWidget(self.toolBox)

        self.substractCheckBox = QCheckBox(self.layoutWidget)
        self.substractCheckBox.setObjectName(u"substractCheckBox")

        self.verticalLayout.addWidget(self.substractCheckBox)

        self.dependentCheckBox = QCheckBox(self.layoutWidget)
        self.dependentCheckBox.setObjectName(u"dependentCheckBox")
        self.dependentCheckBox.setChecked(True)

        self.verticalLayout.addWidget(self.dependentCheckBox)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.denoisePushButton = QPushButton(self.layoutWidget)
        self.denoisePushButton.setObjectName(u"denoisePushButton")

        self.horizontalLayout_3.addWidget(self.denoisePushButton)

        self.skipPushButton = QPushButton(self.layoutWidget)
        self.skipPushButton.setObjectName(u"skipPushButton")

        self.horizontalLayout_3.addWidget(self.skipPushButton)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.splitter.addWidget(self.layoutWidget)
        self.layoutWidget1 = QWidget(self.splitter)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.verticalLayout_5 = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.layoutWidget1)
        self.widget.setObjectName(u"widget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy2)

        self.verticalLayout_5.addWidget(self.widget)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.spectrumPushButton = QPushButton(self.layoutWidget1)
        self.spectrumPushButton.setObjectName(u"spectrumPushButton")

        self.horizontalLayout_6.addWidget(self.spectrumPushButton)

        self.label_10 = QLabel(self.layoutWidget1)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_6.addWidget(self.label_10)

        self.yLogCheckBox = QCheckBox(self.layoutWidget1)
        self.yLogCheckBox.setObjectName(u"yLogCheckBox")

        self.horizontalLayout_6.addWidget(self.yLogCheckBox)

        self.yAxisPushButton = QPushButton(self.layoutWidget1)
        self.yAxisPushButton.setObjectName(u"yAxisPushButton")

        self.horizontalLayout_6.addWidget(self.yAxisPushButton)

        self.yLimDoubleToolButton = QToolButton(self.layoutWidget1)
        self.yLimDoubleToolButton.setObjectName(u"yLimDoubleToolButton")

        self.horizontalLayout_6.addWidget(self.yLimDoubleToolButton)

        self.yLimHalfToolButton = QToolButton(self.layoutWidget1)
        self.yLimHalfToolButton.setObjectName(u"yLimHalfToolButton")

        self.horizontalLayout_6.addWidget(self.yLimHalfToolButton)


        self.verticalLayout_5.addLayout(self.horizontalLayout_6)

        self.splitter.addWidget(self.layoutWidget1)

        self.verticalLayout_4.addWidget(self.splitter)


        self.retranslateUi(Form)

        self.toolBox.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.showAveragePushButton.setText(QCoreApplication.translate("Form", u"show selected r&aw spectrum in spectra list", None))
#if QT_CONFIG(shortcut)
        self.showAveragePushButton.setShortcut(QCoreApplication.translate("Form", u"Alt+A", None))
#endif // QT_CONFIG(shortcut)
        self.label.setText(QCoreApplication.translate("Form", u"quantile", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"N sigma", None))
        self.sizeDependentLabel.setText(QCoreApplication.translate("Form", u"size-dependent", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"Noise for high-intensity peaks", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"formula", None))
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"delta(integer)", None))
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"mass", None))
        self.addPushButton.setText(QCoreApplication.translate("Form", u"add", None))
        self.delPushButton.setText(QCoreApplication.translate("Form", u"del", None))
        self.calculateNoisePushButton.setText(QCoreApplication.translate("Form", u"&Calc noise for the selected spectrum", None))
#if QT_CONFIG(shortcut)
        self.calculateNoisePushButton.setShortcut(QCoreApplication.translate("Form", u"Alt+C", None))
#endif // QT_CONFIG(shortcut)
        self.toolBox.setItemText(self.toolBox.indexOf(self.noiseTool), QCoreApplication.translate("Form", u"Noise inputs", None))
        ___qtablewidgetitem3 = self.paramTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"enabled", None))
        ___qtablewidgetitem4 = self.paramTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"type", None))
        ___qtablewidgetitem5 = self.paramTableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Form", u"noise", None))
        ___qtablewidgetitem6 = self.paramTableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Form", u"LOD", None))
        self.recalculateNoisePushButton.setText(QCoreApplication.translate("Form", u"&Recalulate noise", None))
#if QT_CONFIG(shortcut)
        self.recalculateNoisePushButton.setShortcut(QCoreApplication.translate("Form", u"Alt+R", None))
#endif // QT_CONFIG(shortcut)
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Export", None))
        self.exportDenoisedSpectrumPushButton.setText(QCoreApplication.translate("Form", u"Denoised spectrum", None))
#if QT_CONFIG(shortcut)
        self.exportDenoisedSpectrumPushButton.setShortcut(QCoreApplication.translate("Form", u"Ctrl+Alt+D", None))
#endif // QT_CONFIG(shortcut)
        self.exportNoisePeaksPushButton.setText(QCoreApplication.translate("Form", u"Noise peaks", None))
#if QT_CONFIG(shortcut)
        self.exportNoisePeaksPushButton.setShortcut(QCoreApplication.translate("Form", u"Ctrl+Alt+N", None))
#endif // QT_CONFIG(shortcut)
        self.toolBox.setItemText(self.toolBox.indexOf(self.paramTool), QCoreApplication.translate("Form", u"Noise results", None))
        self.substractCheckBox.setText(QCoreApplication.translate("Form", u"Subtract noise level from peaks", None))
        self.dependentCheckBox.setText(QCoreApplication.translate("Form", u"Spectrum-dependent params", None))
        self.denoisePushButton.setText(QCoreApplication.translate("Form", u"denoise", None))
#if QT_CONFIG(shortcut)
        self.denoisePushButton.setShortcut(QCoreApplication.translate("Form", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.skipPushButton.setText(QCoreApplication.translate("Form", u"ski&p", None))
#if QT_CONFIG(shortcut)
        self.skipPushButton.setShortcut(QCoreApplication.translate("Form", u"Alt+P", None))
#endif // QT_CONFIG(shortcut)
        self.spectrumPushButton.setText(QCoreApplication.translate("Form", u"Scale to spectrum", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"y-lim", None))
        self.yLogCheckBox.setText(QCoreApplication.translate("Form", u"log scale", None))
        self.yAxisPushButton.setText(QCoreApplication.translate("Form", u"rescale", None))
        self.yLimDoubleToolButton.setText(QCoreApplication.translate("Form", u"\u00d72 (\u2191)", None))
#if QT_CONFIG(shortcut)
        self.yLimDoubleToolButton.setShortcut(QCoreApplication.translate("Form", u"Up", None))
#endif // QT_CONFIG(shortcut)
        self.yLimHalfToolButton.setText(QCoreApplication.translate("Form", u"\u00f72 (\u2193)", None))
#if QT_CONFIG(shortcut)
        self.yLimHalfToolButton.setShortcut(QCoreApplication.translate("Form", u"Down", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

