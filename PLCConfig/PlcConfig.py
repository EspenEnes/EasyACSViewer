# Form implementation generated from reading ui file 'PLCConfig.ui'
#
# Created by: PyQt6 UI code generator 6.1.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignTop)
        self.label_4.setWordWrap(False)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 2)
        self.lineEdit_IP = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_IP.setObjectName("lineEdit_IP")
        self.gridLayout.addWidget(self.lineEdit_IP, 1, 1, 1, 1)
        self.lineEdit_Rack = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Rack.setObjectName("lineEdit_Rack")
        self.gridLayout.addWidget(self.lineEdit_Rack, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.lineEdit_Slot = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Slot.setObjectName("lineEdit_Slot")
        self.gridLayout.addWidget(self.lineEdit_Slot, 3, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.lineEdit_Datablock = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Datablock.setObjectName("lineEdit_Datablock")
        self.gridLayout.addWidget(self.lineEdit_Datablock, 4, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.label.setBuddy(self.lineEdit_IP)
        self.label_3.setBuddy(self.lineEdit_Slot)
        self.label_2.setBuddy(self.lineEdit_Rack)
        self.label_5.setBuddy(self.lineEdit_Datablock)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_4.setText(_translate("Dialog", "PLC Config"))
        self.label.setText(_translate("Dialog", "IP"))
        self.label_3.setText(_translate("Dialog", "Slot"))
        self.label_2.setText(_translate("Dialog", "Rack"))
        self.label_5.setText(_translate("Dialog", "Datablock"))
