# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Orbitool\UI\setting\DenoiseTab.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(335, 511)
        Form.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.formLayout = QtWidgets.QFormLayout(Form)
        self.formLayout.setObjectName("formLayout")
        self.peaksLabel = QtWidgets.QLabel(Form)
        self.peaksLabel.setToolTip("")
        self.peaksLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.peaksLabel.setObjectName("peaksLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.peaksLabel)
        self.peaksPlainTextEdit = QtWidgets.QPlainTextEdit(Form)
        self.peaksPlainTextEdit.setMaximumSize(QtCore.QSize(16777215, 50))
        self.peaksPlainTextEdit.setObjectName("peaksPlainTextEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.peaksPlainTextEdit)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(2, QtWidgets.QFormLayout.LabelRole, spacerItem)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.noiseDifferentColorCheckBox = QtWidgets.QCheckBox(Form)
        self.noiseDifferentColorCheckBox.setText("")
        self.noiseDifferentColorCheckBox.setObjectName("noiseDifferentColorCheckBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.noiseDifferentColorCheckBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.peaksLabel.setText(_translate("Form", "High-intensity peaks\n"
"initial list"))
        self.label.setText(_translate("Form", "Plot noise in different color"))
