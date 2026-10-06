# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TimeseriesTab.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QLabel,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(335, 511)
        self.formLayout = QFormLayout(Form)
        self.formLayout.setObjectName(u"formLayout")
        self.timeformatLabel = QLabel(Form)
        self.timeformatLabel.setObjectName(u"timeformatLabel")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.timeformatLabel)

        self.timeformatVerticalLayout = QVBoxLayout()
        self.timeformatVerticalLayout.setObjectName(u"timeformatVerticalLayout")

        self.formLayout.setLayout(2, QFormLayout.ItemRole.FieldRole, self.timeformatVerticalLayout)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.mzRangeTargetComboBox = QComboBox(Form)
        self.mzRangeTargetComboBox.setObjectName(u"mzRangeTargetComboBox")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.mzRangeTargetComboBox)

        self.mzRangePeakfitFuncCommboBox = QComboBox(Form)
        self.mzRangePeakfitFuncCommboBox.setObjectName(u"mzRangePeakfitFuncCommboBox")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.mzRangePeakfitFuncCommboBox)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.timeformatLabel.setText(QCoreApplication.translate("Form", u"export time formats", None))
        self.label.setText(QCoreApplication.translate("Form", u"mz range sum target", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"mz range sum peakfit func", None))
    # retranslateUi

