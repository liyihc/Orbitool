# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DenoiseTab.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QLabel,
    QPlainTextEdit, QSizePolicy, QSpacerItem, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(335, 511)
        Form.setLayoutDirection(Qt.LeftToRight)
        self.formLayout = QFormLayout(Form)
        self.formLayout.setObjectName(u"formLayout")
        self.peaksLabel = QLabel(Form)
        self.peaksLabel.setObjectName(u"peaksLabel")
        self.peaksLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.peaksLabel)

        self.peaksPlainTextEdit = QPlainTextEdit(Form)
        self.peaksPlainTextEdit.setObjectName(u"peaksPlainTextEdit")
        self.peaksPlainTextEdit.setMaximumSize(QSize(16777215, 50))

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.peaksPlainTextEdit)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.formLayout.setItem(2, QFormLayout.ItemRole.LabelRole, self.verticalSpacer)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.noiseDifferentColorCheckBox = QCheckBox(Form)
        self.noiseDifferentColorCheckBox.setObjectName(u"noiseDifferentColorCheckBox")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.noiseDifferentColorCheckBox)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
#if QT_CONFIG(tooltip)
        self.peaksLabel.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.peaksLabel.setText(QCoreApplication.translate("Form", u"High-intensity peaks\n"
"initial list", None))
        self.label.setText(QCoreApplication.translate("Form", u"Plot noise in different color", None))
        self.noiseDifferentColorCheckBox.setText("")
    # retranslateUi

