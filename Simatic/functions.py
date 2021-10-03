from collections import OrderedDict
from dataclasses import dataclass

import snap7

def dataViewParser(path: str) -> OrderedDict:
    Types = {"BOOL": 1, "BYTE": 8, "WORD": 16, "DWORD": 32, "INT": 16, "DINT": 32, "REAL": 32, "S5TIME": 16, "TIME": 32,
             "DATE": 16, "TIME_OF:DAY": 32, "CHAR": 8, "STRING": 26 }

    adress = 0
    outData = str()

    with open(path, "r") as f:
        clipboard = f.read()
    if not clipboard:
        return OrderedDict()

    for line in clipboard.split("\n"):
        if not len(line) > 0: break

        lineItems = line.split("\t")
        byte = adress // 8
        bit = adress % 8
        adress += Types.get(lineItems[1])
        outData += f"{byte}.{bit}   {lineItems[0]}  {lineItems[1]}\n"

    return snap7.util.parse_specification(outData)


def ConcatDataArrayTree(dataArray: bytearray, Nodes: OrderedDict) -> OrderedDict:
    Output = OrderedDict()
    for key,value in Nodes.items():

        if type(value) is tuple:
            dataType: str = value[1]
            offsett: str = value[0]

            byte, bit = [int(x) for x in offsett.split(".")]
            data = None

            if dataType == "BOOL":
                data = snap7.util.get_bool(dataArray, byte, bit)

            if dataType == "WORD":
                data = snap7.util.get_word(dataArray, byte)

            if dataType == "INT":
                data = snap7.util.get_int(dataArray, byte)

            if dataType == "REAL":
                data = snap7.util.get_real(dataArray, byte)
            Output[key] = data

    return Output


@dataclass
class PLC_Config:
    IP: str = "192.168.10.118"
    Rack: int = 0
    Slot: int = 2
    Db: int = 2121