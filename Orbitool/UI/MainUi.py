# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Main.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.workspaceSaveAction = QAction(MainWindow)
        self.workspaceSaveAction.setObjectName(u"workspaceSaveAction")
        self.workspaceLoadAction = QAction(MainWindow)
        self.workspaceLoadAction.setObjectName(u"workspaceLoadAction")
        self.workspaceSaveAsAction = QAction(MainWindow)
        self.workspaceSaveAsAction.setObjectName(u"workspaceSaveAsAction")
        self.configLoadAction = QAction(MainWindow)
        self.configLoadAction.setObjectName(u"configLoadAction")
        self.configSaveAction = QAction(MainWindow)
        self.configSaveAction.setObjectName(u"configSaveAction")
        self.actionss = QAction(MainWindow)
        self.actionss.setObjectName(u"actionss")
        self.settingAction = QAction(MainWindow)
        self.settingAction.setObjectName(u"settingAction")
        self.formulaAction = QAction(MainWindow)
        self.formulaAction.setObjectName(u"formulaAction")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")

        self.verticalLayout.addWidget(self.tabWidget)

        self.processWidget = QWidget(self.centralwidget)
        self.processWidget.setObjectName(u"processWidget")
        self.horizontalLayout_2 = QHBoxLayout(self.processWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.progressBarLayout = QVBoxLayout()
        self.progressBarLayout.setObjectName(u"progressBarLayout")

        self.horizontalLayout_2.addLayout(self.progressBarLayout)

        self.abortPushButton = QPushButton(self.processWidget)
        self.abortPushButton.setObjectName(u"abortPushButton")

        self.horizontalLayout_2.addWidget(self.abortPushButton)


        self.verticalLayout.addWidget(self.processWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menuWorkspace = QMenu(self.menubar)
        self.menuWorkspace.setObjectName(u"menuWorkspace")
        self.menuOrbitool = QMenu(self.menubar)
        self.menuOrbitool.setObjectName(u"menuOrbitool")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuWorkspace.menuAction())
        self.menubar.addAction(self.menuOrbitool.menuAction())
        self.menubar.addAction(self.formulaAction)
        self.menuWorkspace.addAction(self.workspaceLoadAction)
        self.menuWorkspace.addAction(self.workspaceSaveAction)
        self.menuWorkspace.addAction(self.workspaceSaveAsAction)
        self.menuWorkspace.addSeparator()
        self.menuWorkspace.addAction(self.configLoadAction)
        self.menuWorkspace.addAction(self.configSaveAction)
        self.menuOrbitool.addAction(self.settingAction)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.workspaceSaveAction.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(shortcut)
        self.workspaceSaveAction.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.workspaceLoadAction.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.workspaceSaveAsAction.setText(QCoreApplication.translate("MainWindow", u"Save as", None))
        self.configLoadAction.setText(QCoreApplication.translate("MainWindow", u"Load config from workspace", None))
#if QT_CONFIG(tooltip)
        self.configLoadAction.setToolTip(QCoreApplication.translate("MainWindow", u"Load Config from Workspace", None))
#endif // QT_CONFIG(tooltip)
        self.configSaveAction.setText(QCoreApplication.translate("MainWindow", u"Save config to workspace", None))
#if QT_CONFIG(tooltip)
        self.configSaveAction.setToolTip(QCoreApplication.translate("MainWindow", u"Save Config to Workspace", None))
#endif // QT_CONFIG(tooltip)
        self.actionss.setText(QCoreApplication.translate("MainWindow", u"ss", None))
        self.settingAction.setText(QCoreApplication.translate("MainWindow", u"Setting", None))
        self.formulaAction.setText(QCoreApplication.translate("MainWindow", u"Formula", None))
        self.abortPushButton.setText(QCoreApplication.translate("MainWindow", u"Abort", None))
        self.menuWorkspace.setTitle(QCoreApplication.translate("MainWindow", u"Workspace", None))
        self.menuOrbitool.setTitle(QCoreApplication.translate("MainWindow", u"Orbitool", None))
    # retranslateUi

