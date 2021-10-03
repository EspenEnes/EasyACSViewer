from PyQt6.QtCore import QRunnable, pyqtSignal, pyqtSlot, QObject
from snap7.client import Client
from snap7.exceptions import Snap7Exception

from Simatic.functions import ConcatDataArrayTree, PLC_Config
from collections import OrderedDict

class Signals(QObject):
    PLC_Data = pyqtSignal(OrderedDict)
    PLC_Error = pyqtSignal(str)
    PLC_Stop = pyqtSignal()

class PLC_Worker(QRunnable):
    def __init__(self, config: PLC_Config, layout:OrderedDict):
        super(PLC_Worker, self).__init__()
        self.signals = Signals()
        self.client = Client()
        self.config = config
        self.layout = layout
        self.stop_exec = False

        self.signals.PLC_Stop.connect(self.stop)

    def run(self) -> None:
        self.connectClient()
        self.stop_exec = False

        while not self.stop_exec and self.client.get_connected():
            _bytearray = self.client.db_get(self.config.Db)
            data = ConcatDataArrayTree(_bytearray, self.layout)

            self.signals.PLC_Data.emit(data)

    def stop(self):
        self.stop_exec = True

    def connectClient(self):
        try:
            self.client.connect(self.config.IP, self.config.Rack, self.config.Slot)
        except Snap7Exception as e:
            self.signals.PLC_Error.emit(str(e))





