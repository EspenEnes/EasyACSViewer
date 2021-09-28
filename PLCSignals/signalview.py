import typing
from collections import OrderedDict

from PyQt6.QtCore import QAbstractItemModel, QModelIndex, Qt, QVariant, pyqtSignal
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QTreeView, QMenu

from anytree import Node

from functions import OrderdDictInsert, createNodeTree


class SignalView(QTreeView):
    newData = pyqtSignal(OrderedDict)

    def __init__(self, parent=None):
        super(SignalView, self).__init__(parent)
        self.data = OrderedDict()

        self.currentModel = SignalViewModel()
        self.model1 = self.currentModel
        self.model2 = anytreeTreeModel()
        self.setModel(self.currentModel)

        self.currentModel.dataChanged.connect(self.updateData)

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)
        addSignalSetAction = QAction("Add Signal Above", self)
        addSignalSetAction.triggered.connect(lambda: self.addSignal())
        self._contextMenu = QMenu()
        self._contextMenu.addAction(addSignalSetAction)

    def updateData(self, topLeft: QModelIndex, bottomRight: QModelIndex, roles: typing.Iterable[int] = ...) -> None:
        self.data = self.currentModel.getData

    def showContextMenu(self, position):
        if not self.indexAt(position).isValid():
            self.clearSelection()
        self._contextMenu.exec(self.viewport().mapToGlobal(position))

    def addSignal(self, key=None, value=None):
        print(key)
        idx: QModelIndex = self.currentIndex()
        self.currentModel.insertRow(idx.row(), idx.parent(), key, value)

    def ToggleView(self):
        self.currentModel.dataChanged.disconnect(self.updateData)

        if type(self.currentModel) == SignalViewModel:
            self.currentModel = self.model2
        else:
            self.currentModel = self.model1
        self.setModel(self.currentModel)

        self.currentModel.loadData(self.data)

        self.currentModel.dataChanged.connect(self.updateData)

    def loadData(self, data):
        self.data = data
        self.currentModel.loadData(data)


class SignalViewModel(QAbstractItemModel):
    def __init__(self):
        super(SignalViewModel, self).__init__()
        self._data = OrderedDict()
        self.debug = list()

    def loadData(self, data: OrderedDict):
        self.layoutAboutToBeChanged.emit()
        self._data = data
        self.layoutChanged.emit()

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        """Returns the data stored under the given role for the item referred to by the index.
        Note: If you do not have a value to return, return an invalid QVariant instead of returning 0."""
        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            item = index.internalPointer()
            if index.column() == 0:
                return str(list(self._data.keys())[index.row()])
            if index.column() == 1:
                return str(self._data[item][1])
            if index.column() == 2:
                return str(self._data[item][0])
        return QVariant()

    @property
    def getData(self):
        return self._data

    def rowCount(self, parent: QModelIndex = ...) -> int:
        """Returns the number of rows under the given parent. When the parent is valid it means that rowCount is returning the number of children of parent"""
        if parent.isValid():
            return 0
        return len(self._data)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        """Returns the number of columns for the children of the given parent"""
        if parent.isValid():
            if type(parent.internalPointer()) is list:
                return len(parent.internalPointer())
        return 3

    def index(self, row: int, column: int, parent: QModelIndex = ...) -> QModelIndex:
        """Returns the index of the item in the model specified by the given row, column and parent index."""
        return self.createIndex(row, column, list(self._data.keys())[row])

    def parent(self, child: QModelIndex) -> QModelIndex:
        """Returns the parent of the model item with the given index. If the item has no parent, an invalid QModelIndex
             is returned."""
        return QModelIndex()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        """Returns the data for the given role and section in the header with the specified orientation.
        For horizontal headers, the section number corresponds to the column number. Similarly, for vertical headers,
        the section number corresponds to the row number."""

        if role == Qt.ItemDataRole.DisplayRole:
            if section == 0:
                return "Symbol"
            if section == 1:
                return "Type"
            if section == 2:
                return "Adress"
            return QVariant()

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        if index.column() == 1:
            return Qt.ItemFlag.NoItemFlags

        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemNeverHasChildren

    def insertRow(self, row: int, parent: QModelIndex = ..., key= None, value=None ) -> bool:
        """Inserts a single row before the given row in the child items of the parent specified."""
        newtag = "New"
        if key:
            row = -1
            newtag = key

        if parent.isValid() or newtag in list(self._data.keys()):
            return False

        newtag = "New"
        if key:
            row = -1
            newtag = key





        if row >= 0:
            tag = list(self._data.keys())[row]
            newtag = tag.split('.')
            newtag[-1] = "New"
            newtag = ".".join(newtag)
            self.beginInsertRows(parent, row, row)
            self._data = OrderdDictInsert(self._data, row, newtag, ("", "REAL"))
            self.endInsertRows()
            self.dataChanged.emit(parent, parent)
        else:
            row = len(self._data) + 1
            self.beginInsertRows(parent, row, row)
            self._data[newtag] = ("", "REAL")
            self.endInsertRows()
            self.dataChanged.emit(parent, parent)


        return True


    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        """Sets the role data for the item at index to value.
        Returns true if successful; otherwise returns false.
        The dataChanged() signal should be emitted if the data was successfully set."""



        if len(value) == 0 or str(list(self._data.keys())[index.row()]) == value:
            return False

        if index.column() == 0:
            tag = list(self._data.keys())[index.row()]
            idx = list(self._data.keys()).index(tag)
            keyValue = self._data[tag]
            self._data = OrderdDictInsert(self._data, idx, value, keyValue)
            self._data.pop(tag)
            self.layoutChanged.emit()
            self.dataChanged.emit(index, index)

            return True

        if index.column() == 2:
            tag = list(self._data.keys())[index.row()]
            keyValue = self._data[tag]
            new = (value, keyValue[1])
            self._data[tag] = new
            self.layoutChanged.emit()
            self.dataChanged.emit(index, index)

            return True
        return False


class anytreeTreeModel(QAbstractItemModel):
    """This model takes in a anytree NodeTree and creates a model for a QTreeView,
    it returns two columns where the leaf data is displayed in column 2"""

    def __init__(self):
        super(anytreeTreeModel, self).__init__()
        self.rootItem = Node("ACS")
        self._data = OrderedDict()

    def loadData(self, data: OrderedDict):
        self.layoutAboutToBeChanged.emit()
        self._data = data.copy()
        self.rootItem = createNodeTree(self._data)
        self.layoutChanged.emit()

    @property
    def getData(self):
        return self._data

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        """Returns the data stored under the given role for the item referred to by the index.
        Note: If you do not have a value to return, return an invalid QVariant instead of returning 0."""
        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            if index.column() == 0:
                return index.internalPointer().name
            elif index.column() == 1:
                node: Node = index.internalPointer()
                if hasattr(node, "Data"):
                    return node.Data[1]
            elif index.column() == 2:
                node: Node = index.internalPointer()
                if hasattr(node, "Data"):
                    return node.Data[0]
        return QVariant()

    def columnCount(self, parent: QModelIndex = ...) -> int:
        """Returns the number of columns for the children of the given parent"""
        if parent.isValid():
            node: Node = parent.internalPointer()
            if True in [hasattr(x, "Data") for x in node.children]:
                return 3
        return 3

    def rowCount(self, parent: QModelIndex = ...) -> int:
        """Returns the number of rows under the given parent. When the parent is valid it means that rowCount is returning the number of children of parent"""
        if parent.isValid():
            node: Node = parent.internalPointer()
            return len(node.children)
        if self.rootItem.is_leaf:
            return 0
        return len(self.rootItem.children)

    def index(self, row: int, column: int, parent: QModelIndex = ...) -> QModelIndex:
        """Returns the index of the item in the model specified by the given row, column and parent index."""
        if parent.isValid():
            node: Node = parent.internalPointer()
        else:
            node: Node = self.rootItem

        """needed to att this compare due to model craching when removing last child of a node """
        if row + 1 <= len(node.children):
            return QAbstractItemModel.createIndex(self, row, column, node.children[row])
        return QModelIndex()

    def parent(self, child: QModelIndex) -> QModelIndex:
        """Returns the parent of the model item with the given index. If the item has no parent, an invalid QModelIndex
        is returned."""
        node: Node = child.internalPointer()
        if hasattr(node, "parent"):

            if node.parent:
                parent: Node = node.parent
                if parent.parent:
                    Gparent: Node = parent.parent
                    row = Gparent.children.index(parent)
                    return QAbstractItemModel.createIndex(self, row, 0, parent)

        return QModelIndex()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        """Returns the data for the given role and section in the header with the specified orientation.
        For horizontal headers, the section number corresponds to the column number. Similarly, for vertical headers,
        the section number corresponds to the row number."""

        if role == Qt.ItemDataRole.DisplayRole:
            if section == 0:
                return "Symbol"
            if section == 1:
                return "Type"
            if section == 2:
                return "Adress"
            return QVariant()

    def insertRow(self, row: int, parent: QModelIndex = ..., key=None, value=None) -> bool:
        """Inserts a single row before the given row in the child items of the parent specified."""

        if parent.isValid():
            pnode: Node = parent.internalPointer()

            if hasattr(pnode.children[row], "Tag"):
                tag: str = getattr(pnode.children[row], "Tag")
                newtag = f"{'.'.join(tag.split('.')[:-1])}.New"
                if newtag in list(self._data.keys()):
                    return False

                new_children = list(pnode.children)
                self.beginInsertRows(parent, row, row)
                new_Node = Node("New")
                setattr(new_Node, "Tag", newtag)
                setattr(new_Node, "Data", ("", "REAL"))
                new_children.insert(row, new_Node)
                pnode.children = new_children
                idx = list(self._data.keys()).index(tag)
                self._data = OrderdDictInsert(self._data, idx, newtag, ("", "REAL")).copy()
                self.endInsertRows()
                self.dataChanged.emit(parent, parent)
                return True

        NewNode = Node("New_Group", self.rootItem)
        self.layoutChanged.emit()
        return True

    def removeRow(self, row: int, parent: QModelIndex = ...) -> bool:
        """Removes the given row from the child items of the parent specified."""
        if parent.isValid():
            pnode: Node = parent.internalPointer()
            node: Node = pnode.children[row]

            self.beginRemoveRows(parent, row, row)
            node.parent = None
            self.endRemoveRows()
            return True

        self.beginRemoveRows(parent, row, row)
        node: Node = self.rootItem.children[row]
        node.parent = None
        self.endRemoveRows()
        self.dataChanged.emit(parent, parent)
        return True

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        if index.isValid():
            node: Node = index.internalPointer()
            if index.column() == 2:
                if hasattr(node, "Data"):
                    return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemNeverHasChildren
            if index.column() == 0:
                return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable

        return Qt.ItemFlag.NoItemFlags

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        """Sets the role data for the item at index to value.
        Returns true if successful; otherwise returns false.
        The dataChanged() signal should be emitted if the data was successfully set."""

        if len(value) == 0 or index.internalPointer().name == value:
            return False

        node: Node = index.internalPointer()
        if index.column() == 0:
            node.name = value
            depth = int(node.depth) - 1

            for leave in node.leaves:
                tag = leave.Tag
                newTag = tag.split('.')
                newTag[depth] = value
                newTag = ".".join(newTag)
                leave.Tag = newTag

                idx = list(self._data.keys()).index(tag)
                keyValue = self._data.pop(tag)
                self._data = OrderdDictInsert(self._data, idx, newTag, keyValue)
            self.dataChanged.emit(index, index)
            return True

        if index.column() == 2:
            if hasattr(node, "Tag"):
                adress, type = node.Data
                adress = value
                node.Data = (adress, type)

                tag = node.Tag
                keyValue = self._data[tag]
                new = (value, keyValue[1])
                self._data[tag] = new
                self.dataChanged.emit(index, index)
                return True
        return False
