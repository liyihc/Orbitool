# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Formula.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QDoubleSpinBox,
    QFormLayout, QFrame, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QSpinBox,
    QSplitter, QTableWidget, QTableWidgetItem, QToolButton,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1000, 450)
        Form.setMinimumSize(QSize(700, 450))
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(Form)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.groupBox_search = QGroupBox(self.splitter)
        self.groupBox_search.setObjectName(u"groupBox_search")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_search)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.searchScrollArea = QScrollArea(self.groupBox_search)
        self.searchScrollArea.setObjectName(u"searchScrollArea")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchScrollArea.sizePolicy().hasHeightForWidth())
        self.searchScrollArea.setSizePolicy(sizePolicy)
        self.searchScrollArea.setFrameShape(QFrame.NoFrame)
        self.searchScrollArea.setWidgetResizable(True)
        self.searchScrollAreaWidgetContents = QWidget()
        self.searchScrollAreaWidgetContents.setObjectName(u"searchScrollAreaWidgetContents")
        self.searchScrollAreaWidgetContents.setGeometry(QRect(0, 0, 300, 400))
        self.verticalLayout_7 = QVBoxLayout(self.searchScrollAreaWidgetContents)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.searchScrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label)

        self.mzMinDoubleSpinBox = QDoubleSpinBox(self.searchScrollAreaWidgetContents)
        self.mzMinDoubleSpinBox.setObjectName(u"mzMinDoubleSpinBox")
        self.mzMinDoubleSpinBox.setMaximum(9999.989999999999782)

        self.horizontalLayout_3.addWidget(self.mzMinDoubleSpinBox)

        self.label_2 = QLabel(self.searchScrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label_2)

        self.mzMaxDoubleSpinBox = QDoubleSpinBox(self.searchScrollAreaWidgetContents)
        self.mzMaxDoubleSpinBox.setObjectName(u"mzMaxDoubleSpinBox")
        self.mzMaxDoubleSpinBox.setMaximum(9999.989999999999782)

        self.horizontalLayout_3.addWidget(self.mzMaxDoubleSpinBox)


        self.verticalLayout_7.addLayout(self.horizontalLayout_3)

        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.chargeLabel = QLabel(self.searchScrollAreaWidgetContents)
        self.chargeLabel.setObjectName(u"chargeLabel")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.LabelRole, self.chargeLabel)

        self.chargeSpinBox = QSpinBox(self.searchScrollAreaWidgetContents)
        self.chargeSpinBox.setObjectName(u"chargeSpinBox")
        self.chargeSpinBox.setFocusPolicy(Qt.StrongFocus)
        self.chargeSpinBox.setMinimum(-99)

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.FieldRole, self.chargeSpinBox)

        self.tolerancePpmLabel = QLabel(self.searchScrollAreaWidgetContents)
        self.tolerancePpmLabel.setObjectName(u"tolerancePpmLabel")

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.LabelRole, self.tolerancePpmLabel)

        self.rtolDoubleSpinBox = QDoubleSpinBox(self.searchScrollAreaWidgetContents)
        self.rtolDoubleSpinBox.setObjectName(u"rtolDoubleSpinBox")
        self.rtolDoubleSpinBox.setFocusPolicy(Qt.StrongFocus)

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.FieldRole, self.rtolDoubleSpinBox)

        self.globalLimitLabel = QLabel(self.searchScrollAreaWidgetContents)
        self.globalLimitLabel.setObjectName(u"globalLimitLabel")

        self.formLayout_3.setWidget(2, QFormLayout.ItemRole.LabelRole, self.globalLimitLabel)

        self.globalLimitSpinBox = QSpinBox(self.searchScrollAreaWidgetContents)
        self.globalLimitSpinBox.setObjectName(u"globalLimitSpinBox")
        self.globalLimitSpinBox.setFocusPolicy(Qt.StrongFocus)

        self.formLayout_3.setWidget(2, QFormLayout.ItemRole.FieldRole, self.globalLimitSpinBox)


        self.verticalLayout_7.addLayout(self.formLayout_3)

        self.groupBox_2 = QGroupBox(self.searchScrollAreaWidgetContents)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.nitrogenRuleCheckBox = QCheckBox(self.groupBox_2)
        self.nitrogenRuleCheckBox.setObjectName(u"nitrogenRuleCheckBox")
        self.nitrogenRuleCheckBox.setLayoutDirection(Qt.LeftToRight)

        self.verticalLayout_5.addWidget(self.nitrogenRuleCheckBox)

        self.dbeLimitCheckBox = QCheckBox(self.groupBox_2)
        self.dbeLimitCheckBox.setObjectName(u"dbeLimitCheckBox")

        self.verticalLayout_5.addWidget(self.dbeLimitCheckBox)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setLayoutDirection(Qt.LeftToRight)
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_5)

        self.dbeMinDoubleSpinBox = QDoubleSpinBox(self.groupBox_2)
        self.dbeMinDoubleSpinBox.setObjectName(u"dbeMinDoubleSpinBox")
        self.dbeMinDoubleSpinBox.setFocusPolicy(Qt.StrongFocus)
        self.dbeMinDoubleSpinBox.setMinimum(-99.000000000000000)

        self.horizontalLayout.addWidget(self.dbeMinDoubleSpinBox)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setLayoutDirection(Qt.LeftToRight)
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_4)

        self.dbeMaxDoubleSpinBox = QDoubleSpinBox(self.groupBox_2)
        self.dbeMaxDoubleSpinBox.setObjectName(u"dbeMaxDoubleSpinBox")
        self.dbeMaxDoubleSpinBox.setFocusPolicy(Qt.StrongFocus)
        self.dbeMaxDoubleSpinBox.setMinimum(-99.000000000000000)

        self.horizontalLayout.addWidget(self.dbeMaxDoubleSpinBox)


        self.verticalLayout_5.addLayout(self.horizontalLayout)


        self.verticalLayout_7.addWidget(self.groupBox_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer)

        self.searchScrollArea.setWidget(self.searchScrollAreaWidgetContents)

        self.verticalLayout_6.addWidget(self.searchScrollArea)

        self.splitter.addWidget(self.groupBox_search)
        self.groupBox_4 = QGroupBox(self.splitter)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.elementTableWidget = QTableWidget(self.groupBox_4)
        if (self.elementTableWidget.columnCount() < 8):
            self.elementTableWidget.setColumnCount(8)
        __qtablewidgetitem = QTableWidgetItem()
        self.elementTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.elementTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.elementTableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.elementTableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.elementTableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.elementTableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.elementTableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.elementTableWidget.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        self.elementTableWidget.setObjectName(u"elementTableWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.elementTableWidget.sizePolicy().hasHeightForWidth())
        self.elementTableWidget.setSizePolicy(sizePolicy1)
        self.elementTableWidget.setMinimumSize(QSize(0, 150))
        self.elementTableWidget.setMaximumSize(QSize(16777215, 16777215))
        self.elementTableWidget.setBaseSize(QSize(0, 0))
        self.elementTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.elementTableWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.elementTableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.elementTableWidget.horizontalHeader().setMinimumSectionSize(40)
        self.elementTableWidget.horizontalHeader().setDefaultSectionSize(60)
        self.elementTableWidget.horizontalHeader().setStretchLastSection(True)
        self.elementTableWidget.verticalHeader().setVisible(False)

        self.verticalLayout_8.addWidget(self.elementTableWidget)

        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.elementLineEdit = QLineEdit(self.groupBox_4)
        self.elementLineEdit.setObjectName(u"elementLineEdit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.elementLineEdit.sizePolicy().hasHeightForWidth())
        self.elementLineEdit.setSizePolicy(sizePolicy2)

        self.horizontalLayout_30.addWidget(self.elementLineEdit)

        self.elementAddToolButton = QToolButton(self.groupBox_4)
        self.elementAddToolButton.setObjectName(u"elementAddToolButton")
        self.elementAddToolButton.setMaximumSize(QSize(20, 20))
        palette = QPalette()
        brush = QBrush(QColor(0, 85, 0, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush)
        brush1 = QBrush(QColor(120, 120, 120, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush1)
        self.elementAddToolButton.setPalette(palette)
        font = QFont()
        font.setFamilies([u"Consolas"])
        font.setPointSize(12)
        font.setBold(True)
        self.elementAddToolButton.setFont(font)

        self.horizontalLayout_30.addWidget(self.elementAddToolButton)


        self.verticalLayout_8.addLayout(self.horizontalLayout_30)

        self.splitter.addWidget(self.groupBox_4)
        self.groupBox_3 = QGroupBox(self.splitter)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.isotopeTreeWidget = QTreeWidget(self.groupBox_3)
        self.isotopeTreeWidget.setObjectName(u"isotopeTreeWidget")
        sizePolicy1.setHeightForWidth(self.isotopeTreeWidget.sizePolicy().hasHeightForWidth())
        self.isotopeTreeWidget.setSizePolicy(sizePolicy1)
        self.isotopeTreeWidget.setMinimumSize(QSize(0, 200))
        self.isotopeTreeWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.isotopeTreeWidget.setExpandsOnDoubleClick(False)
        self.isotopeTreeWidget.header().setVisible(True)
        self.isotopeTreeWidget.header().setCascadingSectionResizes(False)
        self.isotopeTreeWidget.header().setMinimumSectionSize(40)
        self.isotopeTreeWidget.header().setDefaultSectionSize(55)
        self.isotopeTreeWidget.header().setProperty(u"showSortIndicator", False)

        self.verticalLayout_2.addWidget(self.isotopeTreeWidget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.isotopeLineEdit = QLineEdit(self.groupBox_3)
        self.isotopeLineEdit.setObjectName(u"isotopeLineEdit")

        self.horizontalLayout_2.addWidget(self.isotopeLineEdit)

        self.isotopeAddToolButton = QToolButton(self.groupBox_3)
        self.isotopeAddToolButton.setObjectName(u"isotopeAddToolButton")
        self.isotopeAddToolButton.setMaximumSize(QSize(20, 20))
        palette1 = QPalette()
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush1)
        self.isotopeAddToolButton.setPalette(palette1)
        self.isotopeAddToolButton.setFont(font)

        self.horizontalLayout_2.addWidget(self.isotopeAddToolButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.splitter.addWidget(self.groupBox_3)

        self.verticalLayout.addWidget(self.splitter)

        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy3)
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.inputLineEdit = QLineEdit(self.groupBox)
        self.inputLineEdit.setObjectName(u"inputLineEdit")
        sizePolicy2.setHeightForWidth(self.inputLineEdit.sizePolicy().hasHeightForWidth())
        self.inputLineEdit.setSizePolicy(sizePolicy2)
        font1 = QFont()
        font1.setFamilies([u"Consolas"])
        self.inputLineEdit.setFont(font1)

        self.horizontalLayout_4.addWidget(self.inputLineEdit)

        self.calcPushButton = QPushButton(self.groupBox)
        self.calcPushButton.setObjectName(u"calcPushButton")
        sizePolicy2.setHeightForWidth(self.calcPushButton.sizePolicy().hasHeightForWidth())
        self.calcPushButton.setSizePolicy(sizePolicy2)
        self.calcPushButton.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_4.addWidget(self.calcPushButton)


        self.verticalLayout.addWidget(self.groupBox)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox_search.setTitle(QCoreApplication.translate("Form", u"Search", None))
        self.label.setText(QCoreApplication.translate("Form", u"mz min", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"mz max", None))
        self.chargeLabel.setText(QCoreApplication.translate("Form", u"charge", None))
        self.tolerancePpmLabel.setText(QCoreApplication.translate("Form", u"tolerance(ppm)", None))
#if QT_CONFIG(tooltip)
        self.globalLimitLabel.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>In the calculation, the sum of isotopes marked with &quot;global limit&quot; will not exceed this value</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.globalLimitLabel.setText(QCoreApplication.translate("Form", u"global limit", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"DBE limit", None))
#if QT_CONFIG(tooltip)
        self.nitrogenRuleCheckBox.setToolTip(QCoreApplication.translate("Form", u"the restriction that DBE must be an integer", None))
#endif // QT_CONFIG(tooltip)
        self.nitrogenRuleCheckBox.setText(QCoreApplication.translate("Form", u"enable Nitrogen Rule", None))
#if QT_CONFIG(tooltip)
        self.dbeLimitCheckBox.setToolTip(QCoreApplication.translate("Form", u"DBE range limit and O and H quantity limit. Please check the instruction manual for the specific calculation method.\n"
"You can update the DBE of the element and the attributes that affect the number of O and H in the \"element infos\".", None))
#endif // QT_CONFIG(tooltip)
        self.dbeLimitCheckBox.setText(QCoreApplication.translate("Form", u"enable DBE limit and O H limit", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"min", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"max", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Form", u"element infos", None))
        ___qtablewidgetitem = self.elementTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"e", None))
        ___qtablewidgetitem1 = self.elementTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"mass", None))
        ___qtablewidgetitem2 = self.elementTableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"del", None))
        ___qtablewidgetitem3 = self.elementTableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"2DBE", None))
        ___qtablewidgetitem4 = self.elementTableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"Hmin", None))
        ___qtablewidgetitem5 = self.elementTableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Form", u"Hmax", None))
        ___qtablewidgetitem6 = self.elementTableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Form", u"Omin", None))
        ___qtablewidgetitem7 = self.elementTableWidget.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Form", u"Omax", None))
        self.elementAddToolButton.setText(QCoreApplication.translate("Form", u"+", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Form", u"isotopes", None))
        ___qtreewidgetitem = self.isotopeTreeWidget.headerItem()
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("Form", u"attrs", None))
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("Form", u"max", None))
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Form", u"min", None))
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Form", u"del", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Form", u"Isotope", None))
        self.isotopeAddToolButton.setText(QCoreApplication.translate("Form", u"+", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Mass calculator", None))
        self.calcPushButton.setText(QCoreApplication.translate("Form", u"Calc", None))
    # retranslateUi

