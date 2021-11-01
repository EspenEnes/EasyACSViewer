from collections import OrderedDict
from dataclasses import dataclass
from snap7.util import parse_specification
import re

import snap7


def dataViewParser(DataBlock_Str: str) -> OrderedDict:
    def checkType(type: str, types: dict) -> int:

        if type.startswith('STRING'):
            size = re.search(r'\d+', type).group(0)
            return int((int(types.get('STRING')) * int(size) + 16))

        else:
            return int(types.get(type))

    Types = {"BOOL": 1, "BYTE": 8, "WORD": 16, "DWORD": 32, "INT": 16, "DINT": 32, "REAL": 32, "S5TIME": 16,
             "TIME": 32,
             "DATE": 16, "TIME_OF:DAY": 32, "CHAR": 8, "STRING": 16}

    adress = 0
    outData = str()
    #
    # with open(path, "r") as f:
    #     clipboard = f.read()
    # if not clipboard:
    #     return OrderedDict()

    clipboard = DataBlock_Str

    for line in clipboard.split("\n"):
        if not len(line) > 0: break

        lineItems = [x.strip(" ") for x in line.split() if len(x) > 0]
        byte = adress // 8

        # Alltid start REAL og int på eit partall
        if lineItems[1] == "REAL" or lineItems[
            1] == "INT":  # todo Fix denne jolly fixen for å få parsingen til å stemme
            if byte % 2 != 0:
                byte += 1
                adress += 8
        # Alltid start Byte på eit partall, så lenge forgående type ikkje var Byte.
        if lineItems[1] == "BYTE":  # todo nok en jolly fix for å sjekke om forgående signal var byte.
            if not outData.split("\n")[-2].split()[2] == "BYTE":
                if byte % 2 != 0:
                    byte += 1
                    adress += 8

        bit = adress % 8
        adress += checkType(lineItems[1], Types)

        outData += f"{byte}.{bit}   {lineItems[0]}  {lineItems[1].replace(' ', '')}\n"
        a = 5

    return parse_specification(outData)


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
    Db: int = 2521

@dataclass
class MULTICAST_CONFIG:
    MCAST_GRP: str = "224.10.10.106"
    MCAST_PORT: int = 20123
    Len: int = 480
    a = 0.0
