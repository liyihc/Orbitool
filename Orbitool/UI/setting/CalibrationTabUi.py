# Form implementation generated from reading ui file 'Orbitool\UI\setting\CalibrationTab.ui'
#
# Created by: PyQt6 UI code generator 6.5.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(335, 511)
        Form.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.formLayout = QtWidgets.QFormLayout(Form)
        self.formLayout.setObjectName("formLayout")
        self.dragDropReplaceLabel = QtWidgets.QLabel(parent=Form)
        self.dragDropReplaceLabel.setObjectName("dragDropReplaceLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.dragDropReplaceLabel)
        self.dragDropReplaceCheckBox = QtWidgets.QCheckBox(parent=Form)
        self.dragDropReplaceCheckBox.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.dragDropReplaceCheckBox.setText("")
        self.dragDropReplaceCheckBox.setObjectName("dragDropReplaceCheckBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.dragDropReplaceCheckBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.dragDropReplaceLabel.setToolTip(_translate("Form", "Drag and drop csv-files or text into ions table will replace current ions"))
        self.dragDropReplaceLabel.setText(_translate("Form", "Drag drop replace ions"))
