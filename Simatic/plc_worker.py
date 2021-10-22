import snap7.types
from PyQt6.QtCore import QRunnable, pyqtSignal, pyqtSlot, QObject
from snap7.client import Client
from snap7.exceptions import Snap7Exception

from Simatic.functions import ConcatDataArrayTree, PLC_Config
from collections import OrderedDict
import time

class Signals(QObject):
    PLC_Data = pyqtSignal(OrderedDict)
    PLC_Error = pyqtSignal(str)
    PLC_Stop = pyqtSignal()

class PLC_Worker(QRunnable):
    def __init__(self, config: PLC_Config, layout:OrderedDict):
        super(PLC_Worker, self).__init__()
        self.signals = Signals()
        self.client = Client(lib_location="res/snap7_64.dll")
        self.config = config
        self.layout = layout
        self.stop_exec = False

        self.signals.PLC_Stop.connect(self.stop)
        self.max = self.getMax().__trunc__()
        self.min = self.getMin().__trunc__()


    def run(self) -> None:
        self.connectClient()
        self.stop_exec = False

        while not self.stop_exec and self.client.get_connected():
            # _bytearray = self.client.db_get(self.config.Db)
            # t1 = time.time()
            _bytearray = bytearray(self.max)
            a = self.client.read_area(snap7.types.Areas.DB, self.config.Db, self.min, self.max - self.min)
            _bytearray[self.min:self.min] = a

            data = ConcatDataArrayTree(_bytearray, self.layout)
            # print(t1 - time.time())

            self.signals.PLC_Data.emit(data)

    def stop(self):
        self.stop_exec = True

    def connectClient(self):
        try:
            self.client.connect(self.config.IP, self.config.Rack, self.config.Slot)
        except Snap7Exception as e:
            self.signals.PLC_Error.emit(str(e))

    def getMax(self):
        max = 0.0
        for item in self.layout.values():
            if float(item[0]) > max:
                max = float(item[0])
        return max

    def getMin(self):
        min = 9999.9
        for item in self.layout.values():
            if float(item[0]) < min:
                min = float(item[0])
        return min





