import re
from collections import OrderedDict

from snap7.util import parse_specification


class Parser():
    @staticmethod
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
            if lineItems[1] == "REAL" or lineItems[1] == "INT":  # todo Fix denne jolly fixen for å få parsingen til å stemme
                if byte % 2 != 0:
                    byte += 1
                    adress += 8
            # Alltid start Byte på eit partall, så lenge forgående type ikkje var Byte.
            if lineItems[1] == "BYTE": #todo nok en jolly fix for å sjekke om forgående signal var byte.
                if not outData.split("\n")[-2].split()[2] == "BYTE":
                    if byte % 2 != 0:
                        byte += 1
                        adress += 8

            bit = adress % 8
            adress += checkType(lineItems[1], Types)

            outData += f"{byte}.{bit}   {lineItems[0]}  {lineItems[1].replace(' ', '')}\n"
            a = 5

        return parse_specification(outData)

    @staticmethod
    def filterParsedData(parsedData: OrderedDict, **kwargs) -> OrderedDict:
        filterdData = OrderedDict()
        keywords = ["xmax", "xmin", "ymax", "ymin", "zmax", "zmin"]
        for key in kwargs.keys():
            if key == "keywords": keywords = kwargs[key]

        for key, value in parsedData.items():
            nodes = key.split(".")

            if len(keywords) == 0:
                filterdData[key] = value

            if nodes[-1] in keywords:
                filterdData[key] = value
            elif nodes[-1].lower() in keywords:
                filterdData[key] = value

        return filterdData
