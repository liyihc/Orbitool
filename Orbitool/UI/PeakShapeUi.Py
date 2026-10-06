# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PeakShape.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(499, 305)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.spinBox = QSpinBox(Form)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setValue(50)

        self.horizontalLayout.addWidget(self.spinBox)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.comboBox = QComboBox(Form)
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout.addWidget(self.comboBox)

        self.showPushButton = QPushButton(Form)
        self.showPushButton.setObjectName(u"showPushButton")

        self.horizontalLayout.addWidget(self.showPushButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.widget)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.exportPushButton = QPushButton(Form)
        self.exportPushButton.setObjectName(u"exportPushButton")

        self.horizontalLayout_3.addWidget(self.exportPushButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.cancelPushButton = QPushButton(Form)
        self.cancelPushButton.setObjectName(u"cancelPushButton")

        self.horizontalLayout_3.addWidget(self.cancelPushButton)

        self.finishPushButton = QPushButton(Form)
        self.finishPushButton.setObjectName(u"finishPushButton")

        self.horizontalLayout_3.addWidget(self.finishPushButton)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"use the highest N peaks", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Peak distribution", None))
        self.showPushButton.setText(QCoreApplication.translate("Form", u"&show", None))
#if QT_CONFIG(shortcut)
        self.showPushButton.setShortcut(QCoreApplication.translate("Form", u"Alt+S", None))
#endif // QT_CONFIG(shortcut)
        self.exportPushButton.setText(QCoreApplication.translate("Form", u"&Export peak shape info", None))
#if QT_CONFIG(shortcut)
        self.exportPushButton.setShortcut(QCoreApplication.translate("Form", u"Alt+E", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.cancelPushButton.setToolTip(QCoreApplication.translate("Form", u"Ctrl+Z", None))
#endif // QT_CONFIG(tooltip)
        self.cancelPushButton.setText(QCoreApplication.translate("Form", u"Cancel removal", None))
#if QT_CONFIG(shortcut)
        self.cancelPushButton.setShortcut(QCoreApplication.translate("Form", u"Ctrl+Z", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.finishPushButton.setToolTip(QCoreApplication.translate("Form", u"Return Key", None))
#endif // QT_CONFIG(tooltip)
        self.finishPushButton.setText(QCoreApplication.translate("Form", u"Finish and continue", None))
#if QT_CONFIG(shortcut)
        self.finishPushButton.setShortcut(QCoreApplication.translate("Form", u"Return", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

