from Simatic.functions import PLC_Config

from PyQt6 import QtWidgets
from PyQt6.QtGui import QIntValidator, QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression, pyqtSignal

from PLCConfig import PlcConfig


class PlcConfigdialog(QtWidgets.QWidget, PlcConfig.Ui_Dialog):
    data = pyqtSignal(PLC_Config)

    def __init__(self, config,  parent=None):
        super(PlcConfigdialog, self).__init__(parent)
        self.setupUi(self)
        self.PLC_Config: PLC_Config = config

        validator = QIntValidator()
        self.lineEdit_Slot.setValidator(validator)
        self.lineEdit_Rack.setValidator(validator)
        self.lineEdit_Datablock.setValidator(validator)

        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"
        # Regulare expression
        ipRegex = QRegularExpression("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
        ipValidator = QRegularExpressionValidator(ipRegex, self)
        self.lineEdit_IP.setValidator(ipValidator)

        self.dataInvalid = False

        self.loadData()

    def loadData(self):
        if len(self.PLC_Config.IP.split(".")) == 4:
            self.lineEdit_IP.setText(self.PLC_Config.IP)
        self.lineEdit_Rack.setText(str(self.PLC_Config.Rack))
        self.lineEdit_Slot.setText(str(self.PLC_Config.Slot))
        self.lineEdit_Datablock.setText(str(self.PLC_Config.Db))




    def accept(self):
        self.dataInvalid = False
        if len(self.lineEdit_IP.text().split(".")) == 4:
            self.PLC_Config.IP = self.lineEdit_IP.text()
        else:
            self.lineEdit_IP.setText("Invalid IP")
            self.dataInvalid = True

        if len(self.lineEdit_Rack.text().split()) == 1:
            self.PLC_Config.Rack = int(self.lineEdit_Rack.text())
        else:
            self.lineEdit_Rack.setText("Invalid Rack")
            self.dataInvalid = True

        if len(self.lineEdit_Slot.text().split()) == 1:
            self.PLC_Config.Slot = int(self.lineEdit_Slot.text())
        else:
            self.lineEdit_Slot.setText("Invalid Slot")
            self.dataInvalid = True

        if len(self.lineEdit_Datablock.text().split()) == 1:
            self.PLC_Config.Db = int(self.lineEdit_Datablock.text())
        else:
            self.lineEdit_Datablock.setText("Invalid DataBlock")
            self.dataInvalid = True

        if not self.dataInvalid:
            self.data.emit(self.PLC_Config)
            self.close()





    def reject(self):
        self.close()





if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication, QFileDialog

    app = QApplication(sys.argv)
    view = PlcCofig_UI()
    view.show()
    sys.exit(app.exec())