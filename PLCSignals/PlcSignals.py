# Form implementation generated from reading ui file 'PlcSignals.ui'
#
# Created by: PyQt6 UI code generator 6.1.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(771, 686)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.Signal_treeView = SignalView(self.groupBox_2)
        self.Signal_treeView.setObjectName("Signal_treeView")
        self.gridLayout_3.addWidget(self.Signal_treeView, 1, 0, 1, 2)
        self.SignalApplyBtn = QtWidgets.QPushButton(self.groupBox_2)
        self.SignalApplyBtn.setObjectName("SignalApplyBtn")
        self.gridLayout_3.addWidget(self.SignalApplyBtn, 2, 0, 1, 1)
        self.toolButton = QtWidgets.QToolButton(self.groupBox_2)
        self.toolButton.setObjectName("toolButton")
        self.gridLayout_3.addWidget(self.toolButton, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.filterApplyBtn = QtWidgets.QPushButton(self.groupBox_3)
        self.filterApplyBtn.setObjectName("filterApplyBtn")
        self.gridLayout_5.addWidget(self.filterApplyBtn, 1, 1, 1, 1)
        self.filterEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.filterEdit.setObjectName("filterEdit")
        self.gridLayout_5.addWidget(self.filterEdit, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setObjectName("label")
        self.gridLayout_5.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_3, 0, 1, 1, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.datablokTextBrowser = QtWidgets.QTextBrowser(self.groupBox_4)
        self.datablokTextBrowser.setReadOnly(False)
        self.datablokTextBrowser.setObjectName("datablokTextBrowser")
        self.gridLayout_6.addWidget(self.datablokTextBrowser, 0, 0, 1, 1)
        self.DatablockParseBtn = QtWidgets.QPushButton(self.groupBox_4)
        self.DatablockParseBtn.setObjectName("DatablockParseBtn")
        self.gridLayout_6.addWidget(self.DatablockParseBtn, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_4, 1, 1, 1, 1)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.saveBtn = QtWidgets.QPushButton(self.frame)
        self.saveBtn.setObjectName("saveBtn")
        self.gridLayout_4.addWidget(self.saveBtn, 2, 0, 1, 1)
        self.cancelBtn = QtWidgets.QPushButton(self.frame)
        self.cancelBtn.setObjectName("cancelBtn")
        self.gridLayout_4.addWidget(self.cancelBtn, 4, 0, 1, 1)
        self.loadBtn = QtWidgets.QPushButton(self.frame)
        self.loadBtn.setObjectName("loadBtn")
        self.gridLayout_4.addWidget(self.loadBtn, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 2, 0, 1, 2)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.adressEdit = QtWidgets.QLineEdit(self.groupBox)
        self.adressEdit.setObjectName("adressEdit")
        self.gridLayout_7.addWidget(self.adressEdit, 1, 1, 1, 1)
        self.adressLabel = QtWidgets.QLabel(self.groupBox)
        self.adressLabel.setObjectName("adressLabel")
        self.gridLayout_7.addWidget(self.adressLabel, 0, 1, 1, 1)
        self.nameEdit = QtWidgets.QLineEdit(self.groupBox)
        self.nameEdit.setObjectName("nameEdit")
        self.gridLayout_7.addWidget(self.nameEdit, 1, 0, 1, 1)
        self.nameLabel = QtWidgets.QLabel(self.groupBox)
        self.nameLabel.setObjectName("nameLabel")
        self.gridLayout_7.addWidget(self.nameLabel, 0, 0, 1, 1)
        self.signalAddBtn = QtWidgets.QPushButton(self.groupBox)
        self.signalAddBtn.setObjectName("signalAddBtn")
        self.gridLayout_7.addWidget(self.signalAddBtn, 1, 2, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.SignalApplyBtn.clicked.connect(Dialog.applySignals)
        self.DatablockParseBtn.clicked.connect(Dialog.parseDatablock)
        self.filterApplyBtn.clicked.connect(Dialog.applyFilter)
        self.toolButton.clicked.connect(self.Signal_treeView.ToggleView)
        self.saveBtn.clicked.connect(Dialog.saveData)
        self.loadBtn.clicked.connect(Dialog.loadData)
        self.cancelBtn.clicked.connect(Dialog.close)
        self.signalAddBtn.clicked.connect(Dialog.addSignal)
        Dialog.addSignalKeyValue.connect(self.Signal_treeView.addSignal)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox_2.setTitle(_translate("Dialog", "Signals"))
        self.SignalApplyBtn.setText(_translate("Dialog", "Apply"))
        self.toolButton.setText(_translate("Dialog", "..."))
        self.groupBox_3.setTitle(_translate("Dialog", "Filter"))
        self.filterApplyBtn.setText(_translate("Dialog", "Apply"))
        self.filterEdit.setText(_translate("Dialog", "xmax, xmin, ymax, ymin, zmax, zmin"))
        self.label.setText(_translate("Dialog", "Comma seperated sufix filter"))
        self.groupBox_4.setTitle(_translate("Dialog", "Datablock Layout"))
        self.DatablockParseBtn.setText(_translate("Dialog", "Parse"))
        self.saveBtn.setText(_translate("Dialog", "Save"))
        self.cancelBtn.setText(_translate("Dialog", "Cancel"))
        self.loadBtn.setText(_translate("Dialog", "Load"))
        self.groupBox.setTitle(_translate("Dialog", "Add Signal"))
        self.adressLabel.setText(_translate("Dialog", "Adress"))
        self.nameLabel.setText(_translate("Dialog", "Name"))
        self.signalAddBtn.setText(_translate("Dialog", "Add"))
from PLCSignals.signalview import SignalView
