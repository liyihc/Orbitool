# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Setting.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QDialog,
    QDialogButtonBox, QHBoxLayout, QListView, QListWidget,
    QListWidgetItem, QScrollArea, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(700, 332)
        Dialog.setMinimumSize(QSize(700, 300))
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.listWidget = QListWidget(Dialog)
        self.listWidget.setObjectName(u"listWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setMinimumSize(QSize(200, 0))
        self.listWidget.setMaximumSize(QSize(200, 16777215))
        font = QFont()
        font.setPointSize(12)
        self.listWidget.setFont(font)
        self.listWidget.setSelectionMode(QAbstractItemView.NoSelection)
        self.listWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.listWidget.setIconSize(QSize(40, 40))
        self.listWidget.setResizeMode(QListView.Fixed)

        self.horizontalLayout.addWidget(self.listWidget)

        self.scrollArea = QScrollArea(Dialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 472, 280))
        self.scrollAreaLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollAreaLayout.setSpacing(0)
        self.scrollAreaLayout.setObjectName(u"scrollAreaLayout")
        self.scrollAreaLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout.addWidget(self.scrollArea)


        self.verticalLayout.addLayout(self.horizontalLayout)

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
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
    # retranslateUi

