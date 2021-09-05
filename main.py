import snap7
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QObject, pyqtSignal, QEvent, Qt
from PyQt6.QtGui import QMouseEvent, QEnterEvent

from CostumFunctions.costumFunctions import dataViewParser, filterParsedData, ConcatDataArrayTree, UpdateEntityMesh
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

        self.signals = CostumSignals()
        self.openGLWidget.signals.initializeGL_Done.connect(self.GLinitialized)
        self.openGLWidget.signals.EcsScene_Created.connect(self.SceneCreated)
        self.openGLWidget.signals.Entity_clicked.connect(self.textBrowser.setText)





        client = snap7.client.Client()

        with open("res/dbtest", "rb") as ff:
            _bytearray = bytearray(ff.read())
            snap7.util.set_real(_bytearray, 24, 105)
            snap7.util.set_real(_bytearray, 28, 95)
            snap7.util.set_real(_bytearray, 32, 102)
            snap7.util.set_real(_bytearray, 36, 95)
            snap7.util.set_real(_bytearray, 40, 50.0)
            snap7.util.set_real(_bytearray, 44, 0.0)

            snap7.util.set_real(_bytearray, 52, 102)
            snap7.util.set_real(_bytearray, 56, 98)
            snap7.util.set_real(_bytearray, 60, 102)
            snap7.util.set_real(_bytearray, 64, 98)
            snap7.util.set_real(_bytearray, 68, 50.0)
            snap7.util.set_real(_bytearray, 72, 0.0)

            snap7.util.set_real(_bytearray, 80, 100.5)
            snap7.util.set_real(_bytearray, 84, 99.5)
            snap7.util.set_real(_bytearray, 88, 101)
            snap7.util.set_real(_bytearray, 92, 99)
            snap7.util.set_real(_bytearray, 96, 50.0)
            snap7.util.set_real(_bytearray, 100,0.0)

            snap7.util.set_real(_bytearray, 108, 102)
            snap7.util.set_real(_bytearray, 112, 98)
            snap7.util.set_real(_bytearray, 116, 95)
            snap7.util.set_real(_bytearray, 120, 90)
            snap7.util.set_real(_bytearray, 124, 4.0)
            snap7.util.set_real(_bytearray, 128, 0.0)

            snap7.util.set_real(_bytearray, 136, 102)
            snap7.util.set_real(_bytearray, 140, 98)
            snap7.util.set_real(_bytearray, 144, 95)
            snap7.util.set_real(_bytearray, 148, 93)
            snap7.util.set_real(_bytearray, 152, 2.0)
            snap7.util.set_real(_bytearray, 156, 0.0)

            snap7.util.set_real(_bytearray, 164, 101)
            snap7.util.set_real(_bytearray, 168, 99)
            snap7.util.set_real(_bytearray, 172, 94.5)
            snap7.util.set_real(_bytearray, 176, 93)
            snap7.util.set_real(_bytearray, 180, 4.0)
            snap7.util.set_real(_bytearray, 184, 2.0)

        with open("res/dbtest2", "wb") as ff:
            ff.write(_bytearray)


        with open("res/dbtest2", "rb") as f:
            _bytearray = bytearray(f.read())

        parsed = dataViewParser("res/test")

        self.filterdData = filterParsedData(parsed)


        self.data = ConcatDataArrayTree(_bytearray, self.filterdData)

    def GLinitialized(self):
        self.openGLWidget.signals.Data.emit(self.filterdData)

    def SceneCreated(self, scene):
        self.treeView.initData(scene)

        self.UpdateECS()

    def UpdateECS(self):
        UpdateEntityMesh(self.data, self.openGLWidget.scene)


    def eventFilter(self, a0: 'QObject', a1: 'QEvent') -> bool:

        if a0 == self.openGLWidget:
            self.openGLWidget.event(a1)
            return True

        if a1.type() == QEvent.Type.KeyPress:
            self.openGLWidget.event(a1)
            return True
        if a1.type() == QEvent.Type.KeyRelease:
            self.openGLWidget.event(a1)
            return True


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
with open("res/dbtest", "rb") as f:
    _bytearray = bytearray(f.read())
    snap7.util.set_real(_bytearray,24,99.0)
    snap7.util.set_real(_bytearray, 28, 101.0)
    snap7.util.set_real(_bytearray, 32, 95)
    snap7.util.set_real(_bytearray, 36, 100.2)
    snap7.util.set_real(_bytearray, 40, 10.0)
    snap7.util.set_real(_bytearray, 44, 50)

with open("res/dbtest", "wb") as f:
    f.write(_bytearray)
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
    app.installEventFilter(view)
    view.show()
    # app.exec()
    sys.exit(app.exec())
