# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GeneralTab.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QHBoxLayout, QLabel, QLineEdit, QSizePolicy,
    QSpinBox, QToolButton, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(335, 511)
        self.formLayout = QFormLayout(Form)
        self.formLayout.setObjectName(u"formLayout")
        self.themeLabel = QLabel(Form)
        self.themeLabel.setObjectName(u"themeLabel")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.themeLabel)

        self.themeComboBox = QComboBox(Form)
        self.themeComboBox.setObjectName(u"themeComboBox")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.themeComboBox)

        self.defaultSelectLabel = QLabel(Form)
        self.defaultSelectLabel.setObjectName(u"defaultSelectLabel")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.defaultSelectLabel)

        self.defaultSelectCheckBox = QCheckBox(Form)
        self.defaultSelectCheckBox.setObjectName(u"defaultSelectCheckBox")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.defaultSelectCheckBox)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label)

        self.multiCoresSpinBox = QSpinBox(Form)
        self.multiCoresSpinBox.setObjectName(u"multiCoresSpinBox")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.multiCoresSpinBox)

        self.timeFormatLabel = QLabel(Form)
        self.timeFormatLabel.setObjectName(u"timeFormatLabel")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.timeFormatLabel)

        self.timeFormatLineEdit = QLineEdit(Form)
        self.timeFormatLineEdit.setObjectName(u"timeFormatLineEdit")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.timeFormatLineEdit)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.timeFormatShowLabel = QLabel(Form)
        self.timeFormatShowLabel.setObjectName(u"timeFormatShowLabel")
        font = QFont()
        font.setPointSize(8)
        self.timeFormatShowLabel.setFont(font)
        self.timeFormatShowLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.timeFormatShowLabel)

        self.timeFormatRevertButton = QToolButton(Form)
        self.timeFormatRevertButton.setObjectName(u"timeFormatRevertButton")
        self.timeFormatRevertButton.setMaximumSize(QSize(40, 16777215))
        self.timeFormatRevertButton.setFont(font)

        self.horizontalLayout.addWidget(self.timeFormatRevertButton)


        self.formLayout.setLayout(4, QFormLayout.ItemRole.SpanningRole, self.horizontalLayout)

        self.exportTimeFormatLabel = QLabel(Form)
        self.exportTimeFormatLabel.setObjectName(u"exportTimeFormatLabel")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.exportTimeFormatLabel)

        self.exportTimeFormatLineEdit = QLineEdit(Form)
        self.exportTimeFormatLineEdit.setObjectName(u"exportTimeFormatLineEdit")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.exportTimeFormatLineEdit)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.exportTimeFormatShowLabel = QLabel(Form)
        self.exportTimeFormatShowLabel.setObjectName(u"exportTimeFormatShowLabel")
        self.exportTimeFormatShowLabel.setFont(font)
        self.exportTimeFormatShowLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.exportTimeFormatShowLabel)

        self.exportTimeFormatRevertButton = QToolButton(Form)
        self.exportTimeFormatRevertButton.setObjectName(u"exportTimeFormatRevertButton")
        self.exportTimeFormatRevertButton.setMaximumSize(QSize(40, 16777215))
        self.exportTimeFormatRevertButton.setFont(font)

        self.horizontalLayout_2.addWidget(self.exportTimeFormatRevertButton)


        self.formLayout.setLayout(6, QFormLayout.ItemRole.SpanningRole, self.horizontalLayout_2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.themeLabel.setText(QCoreApplication.translate("Form", u"theme", None))
#if QT_CONFIG(tooltip)
        self.defaultSelectLabel.setToolTip(QCoreApplication.translate("Form", u"use first spectrum if nothing is selected", None))
#endif // QT_CONFIG(tooltip)
        self.defaultSelectLabel.setText(QCoreApplication.translate("Form", u"default select", None))
        self.defaultSelectCheckBox.setText("")
        self.label.setText(QCoreApplication.translate("Form", u"use cpu cores", None))
        self.timeFormatLabel.setText(QCoreApplication.translate("Form", u"shown time format", None))
        self.timeFormatShowLabel.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.timeFormatRevertButton.setText(QCoreApplication.translate("Form", u"revert", None))
        self.exportTimeFormatLabel.setText(QCoreApplication.translate("Form", u"export filename time format", None))
        self.exportTimeFormatShowLabel.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.exportTimeFormatRevertButton.setText(QCoreApplication.translate("Form", u"revert", None))
    # retranslateUi

