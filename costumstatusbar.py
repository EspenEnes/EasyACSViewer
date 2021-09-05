from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import QStatusBar


class CostumStatusBar(QStatusBar):
    def __init__(self,parent):
        super(CostumStatusBar, self).__init__()
        self.details = QtWidgets.QPushButton("Details")
        self.details.setIcon(QtGui.QIcon("QT_Design/details-icon.png"))
        self.details.clicked.connect(lambda: parent.dockWidget.show())
        self.addWidget(self.details)
