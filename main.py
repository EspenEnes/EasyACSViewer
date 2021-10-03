from collections import OrderedDict

from PyQt6.QtCore import QObject, pyqtSignal, QEvent, QThreadPool
from PyQt6.QtGui import QEnterEvent
from PyQt6.QtWidgets import QMainWindow

from ECS.functions import UpdateEntityMesh
from PLCSignals.plcSignals_UI import Signaldialog
from Qt_Designs import main_ACS
from Simatic.plc_simulator import Simulator_Worker
from Simatic.plc_worker import PLC_Worker
from Simatic.functions import PLC_Config
from serializer import Serializer

class ACSviewer(QMainWindow, main_ACS.Ui_MainWindow):


    def __init__(self, parent=None):
        super(ACSviewer, self).__init__(parent)
        self.setupUi(self)
        self.PLC_Config = PLC_Config()
        self.signalLayout = OrderedDict()

        self.openGLWidget.signals.EcsScene_Created.connect(self.onSceneCreated)
        self.openGLWidget.signals.Entity_clicked.connect(self.textBrowser.setText)
        self.threadpool = QThreadPool()


    def onDeSerialize(self):
        self.signalLayout, self.PLC_Config = Serializer.deserrialize()
        self.onFilterdSignalList(self.signalLayout)

    def onSerialize(self):
       Serializer.serialize(self.signalLayout , self.PLC_Config)

    def onRun(self):
        if self.actionRun.isChecked():
            self.plcWorker = PLC_Worker(self.PLC_Config, self.signalLayout)
            self.plcWorker.signals.PLC_Error.connect(self.onPlcError)
            self.plcWorker.signals.PLC_Data.connect(self.onNewData)
            self.threadpool.start(self.plcWorker)
            self.actionSimulator.setDisabled(True)
        else:
            self.plcWorker.signals.PLC_Stop.emit()
            self.actionSimulator.setEnabled(True)


    def onSimulator(self):
        if self.actionSimulator.isChecked():
            self.simulatorWorker = Simulator_Worker(self.signalLayout)
            self.simulatorWorker.Signals.PLC_Data.connect(self.onNewData)
            self.threadpool.start(self.simulatorWorker)
            self.actionRun.setDisabled(True)
            print("Simulator Mode On")
        else:
            self.simulatorWorker.Signals.PLC_Stop.emit()
            self.actionRun.setEnabled(True)
            print("Simulator Mode Off")

    def onPlcError(self, error):
        self.actionRun.setChecked(False)
        self.actionSimulator.setEnabled(True)
        self.textBrowser.setText(error)



    def onOpenNodeDialog(self):
        pass #todo lage en node creator, der man bruker signalene man får fra SignalDialogen


    def onOpenSignalDialog(self):
        #lazy implementation so application starts quicker
        self.SignalParser = Signaldialog(self.signalLayout)
        self.SignalParser.DataSignal.connect(self.onFilterdSignalList)
        self.SignalParser.show()


    def onFilterdSignalList(self, data):
        """Recives the applied signal list from Signaldialog widget"""
        self.signalLayout = data

        self.data = OrderedDict()
        for key in data:
            self.data[key] = 0.0

        self.openGLWidget.signals.Data.emit(data)
        self.onUpdateECS()

    def onNewData(self, data: OrderedDict):
        self.data = data

        self.onUpdateECS()


    def onSceneCreated(self, scene):
        self.treeView.initData(scene)
        # self.UpdateECS()

    def onUpdateECS(self):
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
    app.installEventFilter(view)
    view.show()
    # app.exec()
    sys.exit(app.exec())
