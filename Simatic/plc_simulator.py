import snap7
from PyQt6.QtCore import QRunnable, pyqtSignal, QObject

from Simatic.functions import ConcatDataArrayTree
from collections import OrderedDict
from dataclasses import dataclass
from time import sleep

@dataclass
class SimulatorMachineData:
    xmax: float = 0.0
    xmin: float = 0.0
    ymax: float = 0.0
    ymin: float = 0.0
    zmax: float = 0.0
    zmin: float = 0.0
    xPosDir: bool = True
    yPosDir: bool = True
    zPosDir: bool = True


@dataclass
class Simulator:
    TdMainFrame = SimulatorMachineData()
    TdToolFrame = SimulatorMachineData()
    TdElevFrame = SimulatorMachineData()

class Signals(QObject):
    PLC_Data = pyqtSignal(OrderedDict)
    PLC_Error = pyqtSignal(str)


class PLC_Worker(QRunnable):

    def __init__(self, layout:OrderedDict):
        super(PLC_Worker, self).__init__()
        self.Signals = Signals()
        self.layout = layout
        self.run_exec = True

        self.Machines = Simulator

    def run(self) -> None:
        with open("res/dbtest", "rb") as f:
            _bytearray = bytearray(f.read())

        self.simulatorDataInit(_bytearray)

        while self.run_exec:
            self.moveMachinesZdir(self.Machines.TdMainFrame, 40.0, 5.0, 0.6)
            snap7.util.set_real(_bytearray, 44, self.Machines.TdMainFrame.zmin)
            data = ConcatDataArrayTree(_bytearray, self.layout)
            self.Signals.PLC_Data.emit(data)
            sleep(0.05)



    def start_exec(self, run: bool):
        self.run_exec = run

    def connectClient(self):
        with open("res/dbtest", "rb") as f:
            _bytearray = bytearray(f.read())

    def simulatorDataInit(self, array: bytearray):
        self.Machines.TdMainFrame.zmin = snap7.util.get_real(array, 44)
        self.Machines.TdToolFrame.zmin = snap7.util.get_real(array, 72)
        self.Machines.TdElevFrame.zmin = snap7.util.get_real(array, 100)

    def moveMachinesZdir(self, machineData: SimulatorMachineData, limitUp: float, limitDown: float, speed: float):
        if machineData.zmin > limitUp:
            machineData.zPosDir = False
        elif machineData.zmin < limitDown:
            machineData.zPosDir = True

        if machineData.zPosDir:
            machineData.zmin += speed
        else:
            machineData.zmin -= speed







