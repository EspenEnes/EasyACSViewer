from collections import OrderedDict
from random import randrange

from CostumFunctions.costumFunctions import ACSCube
from ECS.components import MeshComponent, RenderComponent, AcsBoxComponent, ColorComponent, TagComponent


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
            entity.AddComponent(ColorComponent())
            color: ColorComponent = entity.GetComponent(ColorComponent)
            color.RGBA = (randrange(10, 100) / 100, randrange(10, 100) / 100, randrange(10, 100) / 100, 0.9)


def UpdateEntityMesh(data, scene):
    data2 = OrderedDict()
    for key, value in data.items():
        name = ".".join(key.split(".")[:-1])
        surfix = key.split(".")[-1]
        if name not in data2: data2[name] = {}
        data2[name][surfix] = value

    for ent, (mesh, tag, acs, color, ) in scene.scene.get_components(MeshComponent, TagComponent, AcsBoxComponent, ColorComponent):
        tag: TagComponent
        mesh: MeshComponent
        acs: AcsBoxComponent
        color:  ColorComponent


        if tag.FriendlyName in data2:
            Xmin, Xmax, Ymin, Ymax, Zmin, Zmax = 0, 0, 0, 0, 0, 0
            color1 = color.RGBA
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





            mesh.Vertesies = ACSCube(0 - Xmax, 0-Xmin, Zmax, Zmin,  Ymin, Ymax, color1,ent)
            mesh.Indesies = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                                 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]