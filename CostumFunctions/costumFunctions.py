import random

import numpy as np

import snap7
from collections import OrderedDict

from ACS_ECS.entity import Entity
from ACS_ECS.components import *

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


def CreateNodeTree(parsedData: OrderedDict , **kwargs) -> OrderedDict:
    nodeTree = OrderedDict()

    for key, value in parsedData.items():
        nodes = key.split(".")
        nodeTree  = creatBTree(nodes, 0, nodeTree, value)

    return nodeTree

def creatBTree(data : list, index: int, mdict : OrderedDict, final:tuple) -> OrderedDict:
    if index < len(data):
        if data[index] is None:
            return mdict

        if index != len(data) - 1:
            if data[index] not in mdict: mdict[data[index]]  = OrderedDict()
        else:
            if data[index] not in mdict: mdict[data[index]] = OrderedDict()
            mdict[data[index]] = final

        creatBTree(data, index + 1, mdict[data[index]],final)
    return mdict

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
                data =  snap7.util.get_real(dataArray, byte)
            Output[key] = data

    return Output

def creatEcsEntitys(Nodes : OrderedDict,scene):
    Entitys = []
    for key, value in Nodes.items():
        name = ".".join(key.split(".")[:-1])
        if name not in Entitys:
            Entitys.append(name)
            entity = scene.CreateEntity(name)
            entity.AddComponent(MeshComponent())
            entity.AddComponent(RenderComponent())
            entity.AddComponent(AcsBoxComponent())



def filterParsedData(parsedData: OrderedDict , **kwargs) -> OrderedDict:
    filterdData = OrderedDict()
    keywords = ["xmax", "xmin", "ymax", "ymin", "zmax", "zmin"]
    for key in kwargs.keys():
        if key == "keywords": keywords = kwargs[key]

    for key, value in parsedData.items():
        nodes = key.split(".")

        if nodes[-1].lower() in keywords:
            filterdData[key] = value

    return filterdData

def ACSCube(Xmin=-1,Xmax=1,Ymin=-1,Ymax=1,Zmin=-1,Zmax=1,color=(5,5,5,5), EntityId=-1):
    Positions =          [Xmin, Ymax, Zmin,0,0,-1,color[0], color[1], color[2], color[3],
                          Xmin, Ymin, Zmin,0,0,-1,color[0], color[1], color[2], color[3],
                          Xmax, Ymin, Zmin,0,0,-1,color[0], color[1], color[2], color[3],
                          Xmax, Ymin, Zmin,0,0,-1,color[0], color[1], color[2], color[3],
                          Xmax, Ymax, Zmin,0,0,-1,color[0], color[1], color[2], color[3],
                          Xmin, Ymax, Zmin,0,0,-1,color[0], color[1], color[2], color[3],

                          Xmin, Ymin, Zmax,-1,0,0,color[0], color[1], color[2], color[3],
                          Xmin, Ymin, Zmin,-1,0,0,color[0], color[1], color[2], color[3],
                          Xmin, Ymax, Zmin,-1,0,0,color[0], color[1], color[2], color[3],
                          Xmin, Ymax, Zmin,-1,0,0,color[0], color[1], color[2], color[3],
                          Xmin, Ymax, Zmax,-1,0,0,color[0], color[1], color[2], color[3],
                          Xmin, Ymin, Zmax,-1,0,0,color[0], color[1], color[2], color[3],

                          Xmax, Ymin, Zmin,1,0,0,color[0], color[1], color[2], color[3],
                          Xmax, Ymin, Zmax,1,0,0,color[0], color[1], color[2], color[3],
                          Xmax, Ymax, Zmax,1,0,0,color[0], color[1], color[2], color[3],
                          Xmax, Ymax, Zmax,1,0,0,color[0], color[1], color[2], color[3],
                          Xmax, Ymax, Zmin,1,0,0,color[0], color[1], color[2], color[3],
                          Xmax, Ymin, Zmin,1,0,0,color[0], color[1], color[2], color[3],

                          Xmin, Ymin, Zmax,0,0,1,color[0], color[1], color[2], color[3],
                          Xmin, Ymax, Zmax,0,0,1,color[0], color[1], color[2], color[3],
                          Xmax, Ymax, Zmax,0,0,1,color[0], color[1], color[2], color[3],
                          Xmax, Ymax, Zmax,0,0,1,color[0], color[1], color[2], color[3],
                          Xmax, Ymin, Zmax,0,0,1,color[0], color[1], color[2], color[3],
                          Xmin, Ymin, Zmax,0,0,1,color[0], color[1], color[2], color[3],

                          Xmin, Ymax, Zmin,0,1,0,color[0], color[1], color[2], color[3],
                          Xmax, Ymax, Zmin,0,1,0,color[0], color[1], color[2], color[3],
                          Xmax, Ymax, Zmax,0,1,0,color[0], color[1], color[2], color[3],
                          Xmax, Ymax, Zmax,0,1,0,color[0], color[1], color[2], color[3],
                          Xmin, Ymax, Zmax,0,1,0,color[0], color[1], color[2], color[3],
                          Xmin, Ymax, Zmin,0,1,0,color[0], color[1], color[2], color[3],

                          Xmin, Ymin, Zmin,0,-1,0,color[0], color[1], color[2], color[3],
                          Xmin, Ymin, Zmax,0,-1,0,color[0], color[1], color[2], color[3],
                          Xmax, Ymin, Zmin,0,-1,0,color[0], color[1], color[2], color[3],
                          Xmax, Ymin, Zmin,0,-1,0,color[0], color[1], color[2], color[3],
                          Xmin, Ymin, Zmax,0,-1,0,color[0], color[1], color[2], color[3],
                          Xmax, Ymin, Zmax,0,-1,0,color[0], color[1], color[2], color[3]]
    #Add inn Color Vector
    # Vertecies = [x for y in (Positions[i:i + 6] + color[0 , color[1*, color[2 , color[3(i < len(Positions) - 4) for i in range(0, len(Positions), 4)) for x in y]
    # Add inn Entity Vector
    Vertecies = [x for y in
                 (Positions[i:i + 10] + [EntityId] * (i < len(Positions) - 1) for i in range(0, len(Positions), 10)) for x
                 in y]



    return np.array(Vertecies, dtype=np.float32)



def SkyboxCube():
    SIZE = 500.0

    Vertecies = np.array([-SIZE, SIZE, -SIZE,
                          -SIZE, -SIZE, -SIZE,
                          SIZE, -SIZE, -SIZE,
                          SIZE, -SIZE, -SIZE,
                          SIZE, SIZE, -SIZE,
                          -SIZE, SIZE, -SIZE,

                          -SIZE, -SIZE, SIZE,
                          -SIZE, -SIZE, -SIZE,
                          -SIZE, SIZE, -SIZE,
                          -SIZE, SIZE, -SIZE,
                          -SIZE, SIZE, SIZE,
                          -SIZE, -SIZE, SIZE,

                          SIZE, -SIZE, -SIZE,
                          SIZE, -SIZE, SIZE,
                          SIZE, SIZE, SIZE,
                          SIZE, SIZE, SIZE,
                          SIZE, SIZE, -SIZE,
                          SIZE, -SIZE, -SIZE,

                          -SIZE, -SIZE, SIZE,
                          -SIZE, SIZE, SIZE,
                          SIZE, SIZE, SIZE,
                          SIZE, SIZE, SIZE,
                          SIZE, -SIZE, SIZE,
                          -SIZE, -SIZE, SIZE,

                          -SIZE, SIZE, -SIZE,
                          SIZE, SIZE, -SIZE,
                          SIZE, SIZE, SIZE,
                          SIZE, SIZE, SIZE,
                          -SIZE, SIZE, SIZE,
                          -SIZE, SIZE, -SIZE,

                          -SIZE, -SIZE, -SIZE,
                          -SIZE, -SIZE, SIZE,
                          SIZE, -SIZE, -SIZE,
                          SIZE, -SIZE, -SIZE,
                          -SIZE, -SIZE, SIZE,
                          SIZE, -SIZE, SIZE], dtype=np.float32)

    return np.array(Vertecies, dtype=np.float32)

def UpdateEntityMesh(data, scene):
    data2 = OrderedDict()
    for key, value in data.items():
        name = ".".join(key.split(".")[:-1])
        surfix = key.split(".")[-1]
        if name not in data2: data2[name] = {}
        data2[name][surfix] = value

    for ent, (mesh, tag, acs,) in scene.scene.get_components(MeshComponent, TagComponent, AcsBoxComponent):
        tag: TagComponent
        mesh: MeshComponent
        acs : AcsBoxComponent

        if tag.FriendlyName in data2:
            Xmin, Xmax, Ymin, Ymax, Zmin, Zmax = 0, 0, 0, 0, 0, 0
            color = [random.randrange(10,100) / 100, random.randrange(10,100) / 100, random.randrange(10,100) / 100, .9]
            for key, value in data2[tag.FriendlyName].items():

                if key.lower() == "xmin":
                    Xmin = value
                    acs.Xmin = value
                elif key.lower() == "xmax":
                    Xmax = value
                    acs.Xmax = value
                elif key.lower() == "ymin":
                    Ymin = value
                    acs.Ymin = value
                elif key.lower() == "ymax":
                    Ymax = value
                    acs.Ymax = value
                elif key.lower() == "zmin":
                    Zmin = value
                    acs.Zmin = value
                elif key.lower() == "zmax":
                    Zmax = value
                    acs.Zmax = value




            mesh.Vertesies = ACSCube(0 - Xmax, 0-Xmin, Zmin, Zmax,  Ymin, Ymax, color,ent)
            mesh.Indesies = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                                 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]

def Quad2d(x, y, z, size, TexID=0, color=None, roll=0.0, pitch=0.0, entityID=-1):
    width, hight = size

    transformPos = glm.translate(glm.mat4(), glm.vec3(x, y, z))
    transformRoll = glm.rotate(glm.mat4(), glm.radians(roll), glm.vec3(0, 0, 1))
    transformPitch = glm.rotate(glm.mat4(), glm.radians(pitch), glm.vec3(1, 0, 0))
    transform = transformPos * transformRoll * transformPitch
    position = glm.vec4()

    # np.array([entityID],dtype=np.uintc)

    if color is None:
        r, g, b, a = (1, 1, 1, 1)
    else:
        r, g, b, a = color

    # V1
    position.x = - width / 2
    position.z = - hight / 2
    position.y = 0
    position.w = 1.0
    positions = list(transform * position)[:-1]

    # positions = [x, y, 50]
    color = [r, g, b, a]
    normals = [0,1,0]
    TextureCorr = [0, 0]
    TextureID = [TexID]
    v1 = positions + normals  + color + [entityID]

    # v2
    position.x = width / 2
    position.z = - hight / 2
    position.y = 0
    position.w = 1.0
    positions = list(transform * position)[:-1]

    # positions = [x + width, y, 50]
    color = [r, g, b, a]
    normals = [0,1,0]
    TextureCorr = [1.0, 0.0]
    TextureID = [TexID]
    v2 = positions + normals + color + [entityID]

    # v3
    position.x = width / 2
    position.z = hight / 2
    position.y = 0
    position.w = 1.0
    positions = list(transform * position)[:-1]

    # positions = [x + width, y + hight, 50]
    color = [r, g, b, a]
    normals = [0, 1, 0]
    TextureCorr = [1.0, 1.0]
    TextureID = [TexID]
    v3 = positions + normals + color + [entityID]

    # v4
    position.x = - width / 2
    position.z = hight / 2
    position.y = 0
    position.w = 1.0
    positions = list(transform * position)[:-1]

    # positions = [x, y + hight, 50]
    color = [r, g, b, a]
    normals = [0, 1, 0]
    TextureCorr = [0.0, 1.0]
    TextureID = [TexID]
    v4 = positions + normals + color + [entityID]

    Vertecies = v1 + v2 + v3 + v4
    Indesies =  [0, 1, 2, 2, 3, 0]

    return Vertecies, Indesies





