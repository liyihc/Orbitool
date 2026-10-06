# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PeakList.ui'
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
    QHBoxLayout, QHeaderView, QLabel, QPushButton,
    QSizePolicy, QTableWidget, QTableWidgetItem, QToolButton,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(263, 336)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.bindPlotCheckBox = QCheckBox(Form)
        self.bindPlotCheckBox.setObjectName(u"bindPlotCheckBox")
        self.bindPlotCheckBox.setChecked(True)

        self.verticalLayout.addWidget(self.bindPlotCheckBox)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.doubleSpinBox = QDoubleSpinBox(Form)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")
        self.doubleSpinBox.setMaximum(9999.989999999999782)
        self.doubleSpinBox.setValue(300.000000000000000)

        self.horizontalLayout.addWidget(self.doubleSpinBox)

        self.gotoToolButton = QToolButton(Form)
        self.gotoToolButton.setObjectName(u"gotoToolButton")

        self.horizontalLayout.addWidget(self.gotoToolButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tableWidget = QTableWidget(Form)
        if (self.tableWidget.columnCount() < 7):
            self.tableWidget.setColumnCount(7)
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
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)
        self.tableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.tableWidget)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_29 = QLabel(Form)
        self.label_29.setObjectName(u"label_29")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_29.sizePolicy().hasHeightForWidth())
        self.label_29.setSizePolicy(sizePolicy1)

        self.horizontalLayout_18.addWidget(self.label_29)

        self.exportSpectrumPushButton = QPushButton(Form)
        self.exportSpectrumPushButton.setObjectName(u"exportSpectrumPushButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.exportSpectrumPushButton.sizePolicy().hasHeightForWidth())
        self.exportSpectrumPushButton.setSizePolicy(sizePolicy2)

        self.horizontalLayout_18.addWidget(self.exportSpectrumPushButton)

        self.exportPeaksPushButton = QPushButton(Form)
        self.exportPeaksPushButton.setObjectName(u"exportPeaksPushButton")
        sizePolicy2.setHeightForWidth(self.exportPeaksPushButton.sizePolicy().hasHeightForWidth())
        self.exportPeaksPushButton.setSizePolicy(sizePolicy2)

        self.horizontalLayout_18.addWidget(self.exportPeaksPushButton)

        self.exportIsotopePushButton = QPushButton(Form)
        self.exportIsotopePushButton.setObjectName(u"exportIsotopePushButton")
        sizePolicy2.setHeightForWidth(self.exportIsotopePushButton.sizePolicy().hasHeightForWidth())
        self.exportIsotopePushButton.setSizePolicy(sizePolicy2)

        self.horizontalLayout_18.addWidget(self.exportIsotopePushButton)


        self.verticalLayout.addLayout(self.horizontalLayout_18)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.bindPlotCheckBox.setText(QCoreApplication.translate("Form", u"bind to plot", None))
        self.gotoToolButton.setText(QCoreApplication.translate("Form", u"goto", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"position", None))
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"formula", None))
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"intensity", None))
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"ppm", None))
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"area", None))
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Form", u"tag", None))
        ___qtablewidgetitem6 = self.tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Form", u"peaks num", None))
#if QT_CONFIG(tooltip)
        self.tableWidget.setToolTip(QCoreApplication.translate("Form", u"Double click to edit peak", None))
#endif // QT_CONFIG(tooltip)
        self.label_29.setText(QCoreApplication.translate("Form", u"Export", None))
        self.exportSpectrumPushButton.setText(QCoreApplication.translate("Form", u"Spectrum", None))
        self.exportPeaksPushButton.setText(QCoreApplication.translate("Form", u"peaks", None))
        self.exportIsotopePushButton.setText(QCoreApplication.translate("Form", u"isotope", None))
    # retranslateUi

