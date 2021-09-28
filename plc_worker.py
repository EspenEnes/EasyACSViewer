from PyQt6.QtCore import QRunnable, pyqtSignal
from snap7.client import Client

from Simatic.functions import ConcatDataArrayTree
from functions import PLC_Config
from collections import OrderedDict

class PLC_Worker(QRunnable):
    PLC_Data = pyqtSignal(OrderedDict)
    def __init__(self, client: Client, config: PLC_Config, layout:OrderedDict):
        super(PLC_Worker, self).__init__()
        self.client = client
        self.config = config
        self.layout = layout

    def run(self) -> None:
        while self.client.get_connected():
            _bytearray = self.client.db_get(self.config.Db)
            data = ConcatDataArrayTree(_bytearray, self.layout)

            self.PLC_Data.emit(data)




