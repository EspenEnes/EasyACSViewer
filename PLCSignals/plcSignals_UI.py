from PyQt6 import QtWidgets
from PyQt6.QtCore import pyqtSignal

from PLCSignals import PlcSignals
from collections import OrderedDict
from Simatic.dataViewParser import Parser


class Signaldialog(QtWidgets.QWidget, PlcSignals.Ui_Dialog):
    addSignalKeyValue = pyqtSignal(str, str)
    DataSignal = pyqtSignal(OrderedDict)

    def __init__(self, parent=None):
        super(Signaldialog, self).__init__(parent)
        self.setupUi(self)

        self.Signal_treeView.newData.connect(self.applyNewData)

        self.filterKeywords = ["xmax", "xmin", "ymax", "ymin", "zmax", "zmin"]
        self.filterdData = OrderedDict()
        self.Signal_treeView.loadData(self.filterdData)

    def applyNewData(self, data):
        self.filterdData = data

    def applySignals(self):
        self.DataSignal.emit(self.filterdData)
        self.close()

    def parseDatablock(self):
        data = self.datablokTextBrowser.toPlainText()
        parsedData = Parser.dataViewParser(data)
        self.filterdData = Parser.filterParsedData(parsedData, keywords=self.filterKeywords)
        self.Signal_treeView.loadData(self.filterdData)

    def addSignal(self):
        name = self.nameEdit.text()
        adress = self.adressEdit.text()
        self.addSignalKeyValue.emit(name, adress)

    def applyFilter(self):
        filterValues = self.filterEdit.text().split(",")
        filterValues = [x.strip(" ") for x in filterValues if len(x) > 0]
        self.filterKeywords = filterValues

    def saveData(self):
        f = open("savedata", "w+")
        data = self.datablokTextBrowser.toPlainText()
        f.write(data)
        f.close()

    def loadData(self):
        try:
            with open("savedata", "r") as f:
                data = f.read()
                self.datablokTextBrowser.clear()
                self.datablokTextBrowser.insertPlainText(data)
        except:
            self.datablokTextBrowser.clear()
            self.datablokTextBrowser.insertPlainText("No SaveData to load \n"
                                                     "please copy in dataview and parse")


if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication, QFileDialog

    app = QApplication(sys.argv)
    view = Signaldialog()
    view.show()
    sys.exit(app.exec())
