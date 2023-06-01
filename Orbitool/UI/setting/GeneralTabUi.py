# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Orbitool\UI\setting\GeneralTab.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(335, 511)
        self.formLayout = QtWidgets.QFormLayout(Form)
        self.formLayout.setObjectName("formLayout")
        self.defaultSelectLabel = QtWidgets.QLabel(Form)
        self.defaultSelectLabel.setObjectName("defaultSelectLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.defaultSelectLabel)
        self.defaultSelectCheckBox = QtWidgets.QCheckBox(Form)
        self.defaultSelectCheckBox.setText("")
        self.defaultSelectCheckBox.setObjectName("defaultSelectCheckBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.defaultSelectCheckBox)
        self.timeFormatLabel = QtWidgets.QLabel(Form)
        self.timeFormatLabel.setObjectName("timeFormatLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.timeFormatLabel)
        self.timeFormatLineEdit = QtWidgets.QLineEdit(Form)
        self.timeFormatLineEdit.setObjectName("timeFormatLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.timeFormatLineEdit)
        self.exportTimeFormatLabel = QtWidgets.QLabel(Form)
        self.exportTimeFormatLabel.setObjectName("exportTimeFormatLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.exportTimeFormatLabel)
        self.exportTimeFormatLineEdit = QtWidgets.QLineEdit(Form)
        self.exportTimeFormatLineEdit.setObjectName("exportTimeFormatLineEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.exportTimeFormatLineEdit)
        self.timeFormatShowLabel = QtWidgets.QLabel(Form)
        self.timeFormatShowLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.timeFormatShowLabel.setObjectName("timeFormatShowLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.timeFormatShowLabel)
        self.exportTimeFormatShowLabel = QtWidgets.QLabel(Form)
        self.exportTimeFormatShowLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.exportTimeFormatShowLabel.setObjectName("exportTimeFormatShowLabel")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.exportTimeFormatShowLabel)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.defaultSelectLabel.setToolTip(_translate("Form", "use first spectrum if nothing is selected"))
        self.defaultSelectLabel.setText(_translate("Form", "default select"))
        self.timeFormatLabel.setText(_translate("Form", "shown time format"))
        self.exportTimeFormatLabel.setText(_translate("Form", "export filename time format"))
        self.timeFormatShowLabel.setText(_translate("Form", "TextLabel"))
        self.exportTimeFormatShowLabel.setText(_translate("Form", "TextLabel"))
