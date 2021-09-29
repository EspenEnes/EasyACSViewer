from collections import OrderedDict

import snap7
from PyQt6 import QtWidgets
from PyQt6.QtCore import QObject, pyqtSignal, QEvent, QThreadPool
from PyQt6.QtGui import QEnterEvent

from ECS.functions import UpdateEntityMesh
from PLCSignals.plcSignals_UI import Signaldialog
from Qt_Designs import main_ACS
from Simatic.plc_simulator import PLC_Worker

class ACSviewer(QtWidgets.QMainWindow, main_ACS.Ui_MainWindow):

    def __init__(self, parent=None):
        super(ACSviewer, self).__init__(parent)
        self.setupUi(self)
        self.debugmode = False

        self.openGLWidget.signals.EcsScene_Created.connect(self.SceneCreated)
        self.openGLWidget.signals.Entity_clicked.connect(self.textBrowser.setText)
        self.actionSignal_parser.triggered.connect(self.openSignalDialog)
        self.threadpool = QThreadPool()


    def openSignalDialog(self):
        #lazy implementation so application starts quicker
        self.SignalParser = Signaldialog()
        self.SignalParser.DataSignal.connect(self.aaa)
        self.SignalParser.show()


    def aaa(self, data):
        if self.debugmode:
            self.worker = PLC_Worker(data)
            self.worker.Signals.PLC_Data.connect(self.newData)
            self.threadpool.start(self.worker)

        self.data = OrderedDict()
        for key in data:
            self.data[key] = 0.0

        self.openGLWidget.signals.Data.emit(data)
        self.UpdateECS()

    def newData(self, data: OrderedDict):
        self.data = data

        self.UpdateECS()


    def SceneCreated(self, scene):
        self.treeView.initData(scene)
        # self.UpdateECS()

    def UpdateECS(self):
        UpdateEntityMesh(self.data, self.openGLWidget.scene)

    def eventFilter(self, a0: 'QObject', a1: 'QEvent') -> bool:
        if a0 == self.treeView:
            if a1 == QEnterEvent:
                a1: QEnterEvent
        return super().eventFilter(a0, a1)


if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    # view = TreeView(scene)
    view = ACSviewer()
    view.debugmode = True
    app.installEventFilter(view)
    view.show()
    # app.exec()
    sys.exit(app.exec())
