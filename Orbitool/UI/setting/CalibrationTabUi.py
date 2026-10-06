# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CalibrationTab.ui'
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
    QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(335, 511)
        Form.setLayoutDirection(Qt.LeftToRight)
        self.formLayout = QFormLayout(Form)
        self.formLayout.setObjectName(u"formLayout")
        self.dragDropReplaceLabel = QLabel(Form)
        self.dragDropReplaceLabel.setObjectName(u"dragDropReplaceLabel")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.dragDropReplaceLabel)

        self.dragDropReplaceCheckBox = QCheckBox(Form)
        self.dragDropReplaceCheckBox.setObjectName(u"dragDropReplaceCheckBox")
        self.dragDropReplaceCheckBox.setLayoutDirection(Qt.LeftToRight)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.dragDropReplaceCheckBox)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
#if QT_CONFIG(tooltip)
        self.dragDropReplaceLabel.setToolTip(QCoreApplication.translate("Form", u"Drag and drop csv-files or text into ions table will replace current ions", None))
#endif // QT_CONFIG(tooltip)
        self.dragDropReplaceLabel.setText(QCoreApplication.translate("Form", u"Drag drop replace ions", None))
        self.dragDropReplaceCheckBox.setText("")
    # retranslateUi

