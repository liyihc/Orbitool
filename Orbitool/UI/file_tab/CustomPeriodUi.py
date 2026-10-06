# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CustomPeriod.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QAbstractSpinBox, QApplication,
    QCheckBox, QDateTimeEdit, QDialog, QDialogButtonBox,
    QDoubleSpinBox, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSlider, QSpacerItem, QSpinBox, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(628, 514)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.startDateTimeEdit = QDateTimeEdit(Dialog)
        self.startDateTimeEdit.setObjectName(u"startDateTimeEdit")

        self.gridLayout.addWidget(self.startDateTimeEdit, 0, 1, 1, 1)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)

        self.label_6 = QLabel(Dialog)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 1, 2, 1, 1)

        self.endDateTimeEdit = QDateTimeEdit(Dialog)
        self.endDateTimeEdit.setObjectName(u"endDateTimeEdit")

        self.gridLayout.addWidget(self.endDateTimeEdit, 0, 3, 1, 1)

        self.numIntervalSpinBox = QSpinBox(Dialog)
        self.numIntervalSpinBox.setObjectName(u"numIntervalSpinBox")
        self.numIntervalSpinBox.setMaximum(9999)

        self.gridLayout.addWidget(self.numIntervalSpinBox, 1, 1, 1, 1)

        self.generateNumPeriodPushButton = QPushButton(Dialog)
        self.generateNumPeriodPushButton.setObjectName(u"generateNumPeriodPushButton")
        self.generateNumPeriodPushButton.setEnabled(True)

        self.gridLayout.addWidget(self.generateNumPeriodPushButton, 1, 3, 1, 1)

        self.label_7 = QLabel(Dialog)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 2, 0, 1, 1)

        self.timeIntervalLineEdit = QLineEdit(Dialog)
        self.timeIntervalLineEdit.setObjectName(u"timeIntervalLineEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timeIntervalLineEdit.sizePolicy().hasHeightForWidth())
        self.timeIntervalLineEdit.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.timeIntervalLineEdit, 2, 1, 1, 1)

        self.label_8 = QLabel(Dialog)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 2, 2, 1, 1)

        self.generateTimePeriodPushButton = QPushButton(Dialog)
        self.generateTimePeriodPushButton.setObjectName(u"generateTimePeriodPushButton")

        self.gridLayout.addWidget(self.generateTimePeriodPushButton, 2, 3, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.tableWidget = QTableWidget(Dialog)
        if (self.tableWidget.columnCount() < 2):
            self.tableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setEditTriggers(QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.tableWidget)

        self.plotWidget = QWidget(Dialog)
        self.plotWidget.setObjectName(u"plotWidget")
        self.plotWidget.setMinimumSize(QSize(0, 60))
        self.plotWidget.setMaximumSize(QSize(16777215, 60))

        self.verticalLayout.addWidget(self.plotWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 16, -1, -1)
        self.label_10 = QLabel(Dialog)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout.addWidget(self.label_10)

        self.plotPositionHorizontalSlider = QSlider(Dialog)
        self.plotPositionHorizontalSlider.setObjectName(u"plotPositionHorizontalSlider")
        self.plotPositionHorizontalSlider.setMaximum(1)
        self.plotPositionHorizontalSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout.addWidget(self.plotPositionHorizontalSlider)

        self.label_9 = QLabel(Dialog)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout.addWidget(self.label_9)

        self.plotFactorDoubleSpinBox = QDoubleSpinBox(Dialog)
        self.plotFactorDoubleSpinBox.setObjectName(u"plotFactorDoubleSpinBox")
        self.plotFactorDoubleSpinBox.setMinimum(0.010000000000000)
        self.plotFactorDoubleSpinBox.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.plotFactorDoubleSpinBox.setValue(1.000000000000000)

        self.horizontalLayout.addWidget(self.plotFactorDoubleSpinBox)

        self.plotHideLabelCheckBox = QCheckBox(Dialog)
        self.plotHideLabelCheckBox.setObjectName(u"plotHideLabelCheckBox")
        self.plotHideLabelCheckBox.setLayoutDirection(Qt.RightToLeft)

        self.horizontalLayout.addWidget(self.plotHideLabelCheckBox)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_2.addWidget(self.label_4)

        self.modifyLineEdit = QLineEdit(Dialog)
        self.modifyLineEdit.setObjectName(u"modifyLineEdit")
        self.modifyLineEdit.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.modifyLineEdit)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.modifyStartPointsPushButton = QPushButton(Dialog)
        self.modifyStartPointsPushButton.setObjectName(u"modifyStartPointsPushButton")

        self.horizontalLayout_2.addWidget(self.modifyStartPointsPushButton)

        self.modifyEndPointsPushButton = QPushButton(Dialog)
        self.modifyEndPointsPushButton.setObjectName(u"modifyEndPointsPushButton")

        self.horizontalLayout_2.addWidget(self.modifyEndPointsPushButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.importPushButton = QPushButton(Dialog)
        self.importPushButton.setObjectName(u"importPushButton")

        self.horizontalLayout_2.addWidget(self.importPushButton)

        self.exportPushButton = QPushButton(Dialog)
        self.exportPushButton.setObjectName(u"exportPushButton")

        self.horizontalLayout_2.addWidget(self.exportPushButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Orbitool - custom periods", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"every", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"from", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"to", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"spectra", None))
#if QT_CONFIG(tooltip)
        self.generateNumPeriodPushButton.setToolTip(QCoreApplication.translate("Dialog", u"coming soon", None))
#endif // QT_CONFIG(tooltip)
        self.generateNumPeriodPushButton.setText(QCoreApplication.translate("Dialog", u"generate by scan number", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"every", None))
        self.timeIntervalLineEdit.setPlaceholderText(QCoreApplication.translate("Dialog", u"2h5m", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"minutes", None))
        self.generateTimePeriodPushButton.setText(QCoreApplication.translate("Dialog", u"generate by time", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"start time/num", None))
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"stop time/num", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"position", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"factor", None))
        self.plotHideLabelCheckBox.setText(QCoreApplication.translate("Dialog", u"hide label", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"add", None))
#if QT_CONFIG(tooltip)
        self.modifyLineEdit.setToolTip(QCoreApplication.translate("Dialog", u"1000s ( 1000 seconds )\n"
"10m5s ( 10 minutes and 5 seconds )\n"
"1h ( 1 hour )", None))
#endif // QT_CONFIG(tooltip)
        self.modifyLineEdit.setPlaceholderText(QCoreApplication.translate("Dialog", u"-5m7s", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"to", None))
        self.modifyStartPointsPushButton.setText(QCoreApplication.translate("Dialog", u"start points", None))
        self.modifyEndPointsPushButton.setText(QCoreApplication.translate("Dialog", u"end points", None))
        self.importPushButton.setText(QCoreApplication.translate("Dialog", u"Import", None))
        self.exportPushButton.setText(QCoreApplication.translate("Dialog", u"Export", None))
    # retranslateUi

