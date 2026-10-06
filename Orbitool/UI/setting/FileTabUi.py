# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FileTab.ui'
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
    QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(335, 511)
        self.formLayout = QFormLayout(Form)
        self.formLayout.setObjectName(u"formLayout")
        self.dotnetDriverLabel = QLabel(Form)
        self.dotnetDriverLabel.setObjectName(u"dotnetDriverLabel")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.dotnetDriverLabel)

        self.dotnetDriverComboBox = QComboBox(Form)
        self.dotnetDriverComboBox.setObjectName(u"dotnetDriverComboBox")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.dotnetDriverComboBox)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.SpanningRole, self.label)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
#if QT_CONFIG(tooltip)
        self.dotnetDriverLabel.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.dotnetDriverLabel.setText(QCoreApplication.translate("Form", u".Net driver", None))
        self.label.setText(QCoreApplication.translate("Form", u"Takes effect after reopening.\n"
"Avoid non-ASCII chars in program and file paths", None))
    # retranslateUi

