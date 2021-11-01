import socket
import struct

import snap7.util
from PyQt6.QtCore import QRunnable, pyqtSignal, pyqtSlot, QObject


from Simatic.functions import ConcatDataArrayTree, MULTICAST_CONFIG
from collections import OrderedDict

class Signals(QObject):
    PLC_Data = pyqtSignal(OrderedDict)
    PLC_Error = pyqtSignal(str)
    PLC_Stop = pyqtSignal()

class Multicast_Worker(QRunnable):
    def __init__(self, config: MULTICAST_CONFIG, layout: OrderedDict):
        super(Multicast_Worker, self).__init__()
        self.signals = Signals()
        self.socket = self.bindSocket()
        self.config = config
        self.layout = layout
        self.stop_exec = False

        self.signals.PLC_Stop.connect(self.stop)

    def run(self) -> None:
        self.stop_exec = False

        while not self.stop_exec:
            _bytes = self.socket.recv(480)
            _bytearray = bytearray(_bytes)
            data = ConcatDataArrayTree(_bytearray, self.layout)
            self.signals.PLC_Data.emit(data)

        self.socket.close()

    def stop(self):
        self.stop_exec = True

    def bindSocket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_IP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("", MULTICAST_CONFIG.MCAST_PORT))
        mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_CONFIG.MCAST_GRP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        return sock






