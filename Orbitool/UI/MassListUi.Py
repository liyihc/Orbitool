# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MassList.ui'
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
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(225, 374)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.addItemLineEdit = QLineEdit(Form)
        self.addItemLineEdit.setObjectName(u"addItemLineEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addItemLineEdit.sizePolicy().hasHeightForWidth())
        self.addItemLineEdit.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.addItemLineEdit)

        self.addPushButton = QPushButton(Form)
        self.addPushButton.setObjectName(u"addPushButton")
        sizePolicy.setHeightForWidth(self.addPushButton.sizePolicy().hasHeightForWidth())
        self.addPushButton.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.addPushButton)

        self.tableWidget = QTableWidget(Form)
        if (self.tableWidget.columnCount() < 2):
            self.tableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy1)
        self.tableWidget.setMaximumSize(QSize(16777215, 16777215))
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)
        self.tableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.tableWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.groupLineEdit = QLineEdit(Form)
        self.groupLineEdit.setObjectName(u"groupLineEdit")

        self.horizontalLayout.addWidget(self.groupLineEdit)

        self.groupPlusPushButton = QPushButton(Form)
        self.groupPlusPushButton.setObjectName(u"groupPlusPushButton")
        sizePolicy.setHeightForWidth(self.groupPlusPushButton.sizePolicy().hasHeightForWidth())
        self.groupPlusPushButton.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.groupPlusPushButton)

        self.groupMinusPushButton = QPushButton(Form)
        self.groupMinusPushButton.setObjectName(u"groupMinusPushButton")
        sizePolicy.setHeightForWidth(self.groupMinusPushButton.sizePolicy().hasHeightForWidth())
        self.groupMinusPushButton.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.groupMinusPushButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy2)

        self.horizontalLayout_14.addWidget(self.label)

        self.doubleSpinBox = QDoubleSpinBox(Form)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")
        sizePolicy.setHeightForWidth(self.doubleSpinBox.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox.setSizePolicy(sizePolicy)
        self.doubleSpinBox.setMinimum(0.010000000000000)
        self.doubleSpinBox.setMaximum(999.990000000000009)
        self.doubleSpinBox.setSingleStep(0.100000000000000)
        self.doubleSpinBox.setValue(1.000000000000000)

        self.horizontalLayout_14.addWidget(self.doubleSpinBox)


        self.verticalLayout.addLayout(self.horizontalLayout_14)

        self.removePushButton = QPushButton(Form)
        self.removePushButton.setObjectName(u"removePushButton")
        sizePolicy.setHeightForWidth(self.removePushButton.sizePolicy().hasHeightForWidth())
        self.removePushButton.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.removePushButton)

        self.importCompareMergePushButton = QPushButton(Form)
        self.importCompareMergePushButton.setObjectName(u"importCompareMergePushButton")
        sizePolicy.setHeightForWidth(self.importCompareMergePushButton.sizePolicy().hasHeightForWidth())
        self.importCompareMergePushButton.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.importCompareMergePushButton)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.splitFormulaCheckBox = QCheckBox(Form)
        self.splitFormulaCheckBox.setObjectName(u"splitFormulaCheckBox")

        self.horizontalLayout_2.addWidget(self.splitFormulaCheckBox)

        self.exportPushButton = QPushButton(Form)
        self.exportPushButton.setObjectName(u"exportPushButton")
        sizePolicy.setHeightForWidth(self.exportPushButton.sizePolicy().hasHeightForWidth())
        self.exportPushButton.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.exportPushButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.addPushButton.setText(QCoreApplication.translate("Form", u"Add", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"mz", None))
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"formula", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"group", None))
        self.groupPlusPushButton.setText(QCoreApplication.translate("Form", u"plus", None))
        self.groupMinusPushButton.setText(QCoreApplication.translate("Form", u"minus", None))
#if QT_CONFIG(tooltip)
        self.label.setToolTip(QCoreApplication.translate("Form", u"When adding, importing, merging or comparing masses, a new mass joins an existing mass-list entry if within this \u00b1ppm; otherwise a new entry is created.", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("Form", u"tolerance(ppm)", None))
        self.removePushButton.setText(QCoreApplication.translate("Form", u"Remove selected", None))
        self.importCompareMergePushButton.setText(QCoreApplication.translate("Form", u"Import, Compare and Merge", None))
        self.splitFormulaCheckBox.setText(QCoreApplication.translate("Form", u"split formula", None))
        self.exportPushButton.setText(QCoreApplication.translate("Form", u"Export", None))
    # retranslateUi

