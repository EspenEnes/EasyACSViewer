import typing
from collections import OrderedDict

from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QAbstractItemModel, QModelIndex, Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QTreeView, QMenu

from ACS_ECS.components import *
from ACS_ECS.scene import Scene


class TreeModel(QAbstractItemModel):

    def __init__(self, data):
        super(TreeModel, self).__init__()
        self.rootItem = TreeItem(["AcsBoxes"])
        # self.setupModelData(data, self.rootItem)
        self.scene: Scene = data
        self.setupModelFromScene(self.scene, self.rootItem)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        if parent.isValid():
            return parent.internalPointer().columnCount()
        return self.rootItem.columnCount()

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            item: TreeItem = index.internalPointer()
            return item.data(index.column())

        if role == Qt.ItemDataRole.DecorationRole:
            item: TreeItem = index.internalPointer()
            if item.EntityId != -1:
                ren = self.scene.scene.component_for_entity(item.EntityId, RenderComponent)

                if not ren.Visible:
                    return QtGui.QIcon("icons/hide-Icon.png")

            if item.EntityId == -1:
                child: TreeItem
                Visible = False

                if not self.checkVisibe(item, Visible):
                    return QtGui.QIcon("icons/hide-Icon.png")

    def checkVisibe(self, item, Visible):
        for child in item.m_childItems:
            if child.EntityId != -1:
                ren = self.scene.scene.component_for_entity(child.EntityId, RenderComponent)
                if ren.Visible: Visible = True
            else:
                Visible = self.checkVisibe(child, Visible)
        return Visible

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.rootItem.data(section)
        return None

    def index(self, row: int, column: int, parent: QModelIndex = ...) -> QModelIndex:
        if not QtCore.QAbstractItemModel.hasIndex(self, row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem: TreeItem = self.rootItem
        else:
            parentItem: TreeItem = parent.internalPointer()

        childItem: TreeItem = parentItem.child(row)

        if childItem:
            return QtCore.QAbstractItemModel.createIndex(self, row, column, childItem)
        else:
            return QModelIndex()

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled

    def parent(self, child: QModelIndex) -> QModelIndex:
        if not child.isValid():
            return QModelIndex()

        childItem: TreeItem = child.internalPointer()
        parentItem: TreeItem = childItem.parentItem()

        if parentItem == self.rootItem:
            return QModelIndex()

        return QtCore.QAbstractItemModel.createIndex(self, parentItem.row(), 0, parentItem)

    def rowCount(self, parent: QModelIndex = ...) -> int:
        parentitem: TreeItem
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentitem = self.rootItem
        else:
            parentitem = parent.internalPointer()
        return parentitem.childCount()

    def setupModelData(self, data, parent):
        for key, value in data.items():
            child = TreeItem([key], parent)

            if type(value) == dict or type(value) == OrderedDict:
                self.setupModelData(value, child)
                parent.appendChild(child)
            elif type(value) == int:
                child.EntityId = value
                parent.appendChild(child)

    def setupModelFromScene(self, scene, parent):
        parent: TreeItem
        test = OrderedDict()
        for ent, (Tag, ren) in scene.scene.get_components(TagComponent, RenderComponent):
            Tag: TagComponent
            if not Tag.FriendlyName in test: test[Tag.FriendlyName] = ent
        NodeTree = self.CreateNodeTree(test)
        self.setupModelData(NodeTree, parent)

    def CreateNodeTree(self, parsedData: OrderedDict, **kwargs) -> OrderedDict:
        nodeTree = OrderedDict()

        for key, value in parsedData.items():
            entityID: int = value
            nodes = key.split(".")
            nodeTree = self.creatBTree(nodes, 0, nodeTree, entityID)

        return nodeTree

    def creatBTree(self, data: list, index: int, mdict: OrderedDict, value) -> OrderedDict:
        if index < len(data):
            if data[index] is None:
                return mdict

            if data[index] not in mdict: mdict[data[index]] = OrderedDict()

            if index == len(data) - 1:
                mdict[data[index]] = value

            self.creatBTree(data, index + 1, mdict[data[index]], value)
        return mdict


class TreeItem():
    def __init__(self, data, parent=None):
        self.m_parentItem = parent
        self.m_itemData = data
        self.m_childItems = list()
        self.EntityId = -1

    def appendChild(self, item):
        self.m_childItems.append(item)

    def child(self, row):
        return self.m_childItems[row]

    def childCount(self):
        return len(self.m_childItems)

    def columnCount(self):
        return len(self.m_itemData)

    def data(self, column):
        return self.m_itemData[column]

    def parentItem(self):
        return self.m_parentItem

    def row(self):
        if self.m_parentItem:
            return 0

    def getAncestors(self) -> list:
        parent: TreeItem
        if self.m_parentItem is None:
            # return [self.m_itemData[0]]
            return []
        else:
            data = self.m_parentItem.getAncestors()
            data.append(self.m_itemData[0])
            return data


class TreeView(QTreeView):
    def __init__(self, parent, ):
        super(TreeView, self).__init__(parent)

        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.test)

    def initData(self, data):
        self.modelData = TreeModel(data)
        self.setModel(self.modelData)





    def test(self, position, **kwargs):
        menu = QMenu()
        index: QModelIndex = self.selectedIndexes()[0]
        item: TreeItem = index.internalPointer()

        if item.childCount() == 0:
            actionHide = QAction(self)
            actionHide.setText("Hide")
            actionHide.triggered.connect(lambda: self.SingleHide(item))

            actionUnHide = QAction(self)
            actionUnHide.setText("UnHide")
            actionUnHide.triggered.connect(lambda: self.SingleUnHide(item))

            menu.addAction(actionHide)
            menu.addAction(actionUnHide)

        if item.childCount() > 0:
            actionHideAll = QAction(self)
            actionHideAll.setText("Hide(All)")
            actionHideAll.triggered.connect(lambda: self.HideAll(item))

            actionUnHideAll = QAction()
            actionUnHideAll.setText("UnHide(All)")
            actionUnHideAll.setIcon(QtGui.QIcon("icons/hide-Icon.png"))
            actionUnHideAll.triggered.connect(lambda: self.UnHideAll(item))

            menu.addAction(actionHideAll)
            menu.addAction(actionUnHideAll)

        menu.exec(self.viewport().mapToGlobal(position))

    def SingleHide(self, item: TreeItem):
        scene: Scene = self.modelData.scene
        ren: RenderComponent
        ren = scene.scene.component_for_entity(item.EntityId, RenderComponent)
        ren.Visible = False


    def SingleUnHide(self, item: TreeItem):
        scene: Scene = self.modelData.scene
        ren: RenderComponent
        ren = scene.scene.component_for_entity(item.EntityId, RenderComponent)
        ren.Visible = True

    def HideAll(self, item: TreeItem):
        scene: Scene = self.modelData.scene
        for child in item.m_childItems:
            if child.EntityId != -1:
                ren: RenderComponent = scene.scene.component_for_entity(child.EntityId, RenderComponent)
                ren.Visible = False
            else:
                self.HideAll(child)

    def UnHideAll(self, item: TreeItem):
        scene: Scene = self.modelData.scene
        for child in item.m_childItems:
            if child.EntityId != -1:
                ren: RenderComponent = scene.scene.component_for_entity(child.EntityId, RenderComponent)
                ren.Visible = True
            else:
                self.HideAll(child)


if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication, QTreeView

    app = QApplication(sys.argv)
    view = TreeView({"Espen": {"Enes": (1, 2, 3)}, "Christine": {"Enes": (1, 2, 3)}})
    view.show()
    app.exec()
