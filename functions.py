import typing
from collections import OrderedDict
from anytree import Node, search


def OrderdDictInsert(root: OrderedDict, index: int, newKey: str, newValue = typing.Any) -> OrderedDict:
    new = OrderedDict()
    for idx, (key , value) in enumerate(root.items()):
        if index == idx:
            new[newKey] = newValue
        new[key] = value
    return new

def createNodeTree(data):
    root = Node("ACS_Boxes")

    for key in data:
        a = root
        value = data[key]
        nodes = key.split(".")
        endnode = key.split(".")[-1]

        for enum, nodeName in enumerate(nodes):
            if nodeName:
                nodeName: str

                result = search.findall(a, lambda node: node.name == nodeName)
                if len(result) < 1:

                    if nodeName != endnode:
                        a = Node(nodeName, parent=a)
                    else:
                        a = Node(nodeName, parent=a)
                        setattr(a, "Tag", key)

                        if not hasattr(a, "Data"):
                            setattr(a, "Data", value)
                else:
                    a = result[0]
    return root
