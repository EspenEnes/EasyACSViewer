from collections import OrderedDict

import snap7
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QObject, pyqtSignal, QEvent
from PyQt6.QtGui import QEnterEvent

from ECS.functions import UpdateEntityMesh
from Simatic.functions import ConcatDataArrayTree
from PLCSignals.plcSignals_UI import Signaldialog
from Qt_Designs import main_ACS


class Param:
    PLCaddress: str = "192.168.10.103"
    rack: int = 0
    slot: int = 1
    DBadress: int = 2121


class CostumSignals(QObject):
    Data = pyqtSignal(dict)




class ACSviewer(QtWidgets.QMainWindow, main_ACS.Ui_MainWindow):

    def __init__(self, parent=None):
        super(ACSviewer, self).__init__(parent)
        self.setupUi(self)
        self.debugmode = False

        self.debugSimulatorTimer = QtCore.QTimer(self)
        self.debugSimulatorTimer.setInterval(20)  # period, in milliseconds
        self.debugSimulatorTimer.timeout.connect(self.simulator)


        self.filterdData = OrderedDict()

        self.signals = CostumSignals()
        self.openGLWidget.signals.initializeGL_Done.connect(self.GLinitialized)
        self.openGLWidget.signals.EcsScene_Created.connect(self.SceneCreated)
        self.openGLWidget.signals.Entity_clicked.connect(self.textBrowser.setText)

        self.SignalParser = Signaldialog()
        self.actionSignal_parser.triggered.connect(lambda: self.SignalParser.show())
        self.SignalParser.DataSignal.connect(self.aaa)

        self.actionNode_Editor.triggered.connect(lambda: self.EntityCreator.show())

        client = snap7.client.Client()


        #Simulator parameters
        self.TDMainframeZ = 0.0
        self.TDMainframeZ_dir = True

        self.TDToolframeZ = 0.0
        self.TDToolframeZ_dir = True

        self.TDElevframeZ = 0.0
        self.TDElevframeZ_dir = True

    def simulator(self):
        if self.TDMainframeZ_dir:
            self.TDMainframeZ += 0.1
        else:
            self.TDMainframeZ -= 0.1

        if self.TDMainframeZ > 40.0:
            self.TDMainframeZ_dir = False
        elif  self.TDMainframeZ < 5.0:
            self.TDMainframeZ_dir = True
        snap7.util.set_real(self._bytearray, 44, self.TDMainframeZ)

        if self.TDToolframeZ_dir:
            self.TDToolframeZ += 0.5
        else:
            self.TDToolframeZ -= 0.5

        if self.TDToolframeZ > 35.0:
            self.TDToolframeZ_dir = False
        elif  self.TDToolframeZ < 0.0:
            self.TDToolframeZ_dir = True
        snap7.util.set_real(self._bytearray, 72, self.TDToolframeZ)

        if self.TDElevframeZ_dir:
            self.TDElevframeZ += 0.5
        else:
            self.TDElevframeZ -= 0.5

        if self.TDElevframeZ > 20.0:
            self.TDElevframeZ_dir = False
        elif self.TDElevframeZ < 0.0:
            self.TDElevframeZ_dir = True
        snap7.util.set_real(self._bytearray, 100, self.TDElevframeZ)

        self.data = ConcatDataArrayTree(self._bytearray, self.filterdData)
        self.UpdateECS()
        self.debugSimulatorTimer.start()

    def aaa(self, data):
        if self.debugmode:
            self._bytearray = self.debugpopulatData()
            self.debugSimulatorTimer.start()
        self.filterdData = data
        self.data = ConcatDataArrayTree(self._bytearray, self.filterdData)
        self.openGLWidget.signals.Data.emit(self.filterdData)


        self.UpdateECS()



    def debugpopulatData(self):
        with open("res/dbtest", "rb") as f:
            _bytearray = bytearray(f.read())
        return _bytearray


    def GLinitialized(self):
        pass
        # self.openGLWidget.signals.Data.emit(self.filterdData)

    def SceneCreated(self, scene):
        self.treeView.initData(scene)
        self.UpdateECS()

    def UpdateECS(self):
        UpdateEntityMesh(self.data, self.openGLWidget.scene)

    def eventFilter(self, a0: 'QObject', a1: 'QEvent') -> bool:

        # if a0 == self.openGLWidget:
        #     self.openGLWidget.event(a1)
        #     return True
        #
        # if a1.type() == QEvent.Type.KeyPress:
        #     self.openGLWidget.event(a1)
        #     return True
        # if a1.type() == QEvent.Type.KeyRelease:
        #     self.openGLWidget.event(a1)
        #     return True

        if a0 == self.treeView:
            if a1 == QEnterEvent:
                a1: QEnterEvent
            # print(a1.)

        return super().eventFilter(a0, a1)

        # # creatEcsEntitys(filterdData,  self.openGLWidget.scene)
        #
        #
        #
        #

        #
        #
        # if not client.get_connected():
        #     try:
        #         client.connect(Param.PLCaddress, Param.rack, Param.slot)
        #     except Exception as e:
        #         print(e)
        #     finally:
        #         if client.get_connected():
        #             _bytearray = client.db_get(Param.DBadress)
        #
        # data = ConcatDataArrayTree(_bytearray, filterdData)
        #
        # UpdateEntityMesh(data, self.openGLWidget.scene)


#
#
#
# # Read in test DB bytearray
# with open("res/dbtest", "rb") as f:
#     _bytearray = bytearray(f.read())
#     snap7.util.set_real(_bytearray, 24, 95.0)
#     snap7.util.set_real(_bytearray, 28, 105.0)
#     snap7.util.set_real(_bytearray, 32, 95)
#     snap7.util.set_real(_bytearray, 36, 100.2)
#     snap7.util.set_real(_bytearray, 40, 50.0)
#     snap7.util.set_real(_bytearray, 44, 10)
#     #
#     snap7.util.set_real(_bytearray, 52, 96.0)
#     snap7.util.set_real(_bytearray, 56, 104.0)
#     snap7.util.set_real(_bytearray, 60, 96)
#     snap7.util.set_real(_bytearray, 64, 100.2)
#     snap7.util.set_real(_bytearray, 68, 50.0)
#     snap7.util.set_real(_bytearray, 72, 9)
#
#     snap7.util.set_real(_bytearray, 80, 97.0)
#     snap7.util.set_real(_bytearray, 84, 103.0)
#     snap7.util.set_real(_bytearray, 88, 97)
#     snap7.util.set_real(_bytearray, 92, 100.2)
#     snap7.util.set_real(_bytearray, 96, 50.0)
#     snap7.util.set_real(_bytearray, 100, 8)
#
# with open("res/dbtest", "wb") as f:
#     f.write(_bytearray)
#
#
# # Create a Client to of Snap7
# client = snap7.client.Client()
#
# # Create a db specification derived from a
# #    dataview of a db in which the byte layout
# #    is not specified
# parsed = dataViewParser("res/test")
#
# # Filter the parsed dataView data with a spesific surfix
# # ["xmax", "xmin", "ymax", "ymin", "zmax", "zmin"]
# filterdData = filterParsedData(parsed)
#
# # Create a Scene and add ACS entityes to this scene
# scene = Scene()
# creatEcsEntitys(filterdData, scene)
#
# # Estabish connection with client and read content of a DB
# if not client.get_connected():
#     try:
#         client.connect(Param.PLCaddress, Param.rack, Param.slot)
#     except Exception as e:
#         print(e)
#     finally:
#         if client.get_connected():
#             bytearray = client.db_get(Param.DBadress)
#
# # query the bytearray for the value of the given leaf and add it to the leaf tuple
# data = ConcatDataArrayTree(_bytearray, filterdData)
#
# # Update scene Entitys mesh component with new data.
# UpdateEntityMesh(data, scene)
#
# # Create a Dictonary NodeTree struct layout from the dataView.
# # ACSNodes = CreateNodeTree(filterdData)
#
# # Construct a model for the TreeView with the data in ACSNodes
# # model = TreeModel(scene)

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
