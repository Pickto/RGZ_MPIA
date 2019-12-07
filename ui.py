from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import config_ui
import core, config_core

def set_turn(nodeUI, player):
    core.set_turn(nodeUI.node, player)
    nodeUI.mark = MarkUI(nodeUI, player)

class Window(QWidget):
    def __init__(self):
        super().__init__()
        config_ui.window = self
        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet(f"background-color : {config_ui.mainColor}")
        self.setFixedSize(config_ui.Width, config_ui.Height)
        self.setWindowTitle(config_ui.Title)
        self.loadPixmaps()
        self.mapUI = MapUI()

    def loadPixmaps(self):
        config_ui.PlayerMark[0] = QPixmap(config_ui.PlayerMark[0]).scaled(QSize(config_ui.TileSize, config_ui.TileSize), Qt.KeepAspectRatio)
        config_ui.PlayerMark[1] = QPixmap(config_ui.PlayerMark[1]).scaled(QSize(config_ui.TileSize, config_ui.TileSize), Qt.KeepAspectRatio)

class MapUI(QWidget):
    def __init__(self):
        super().__init__(config_ui.window)

        self.nodesUI = []
        for i in range(config_core.map.size[1]):
            self.nodesUI.append([])
            for j in range(config_core.map.size[0]):
                self.nodesUI[i].append(NodeUI(config_core.map.get_node(j, i)))

class NodeUI(QLabel):
    def __init__(self, node):
        super().__init__(config_ui.window)

        self.node = node
        self.mark = None
        self.x = node.x
        self.y = node.y
        self.resize(config_ui.TileSize, config_ui.TileSize)
        self.move(self.x * config_ui.TileSize, self.y * config_ui.TileSize)

    def mouseReleaseEvent(self, event):
        super(NodeUI, self).mouseReleaseEvent(event)
        if config_core.state == "game":
            if config_core.turn == 1:
                set_turn(self, 1)


class MarkUI(QLabel):
    def __init__(self, node, player):
        super().__init__(config_ui.window)
        self.resize(config_ui.TileSize, config_ui.TileSize)
        self.setPixmap(config_ui.PlayerMark[player - 1])
        self.move(node.x * config_ui.TileSize, node.y * config_ui.TileSize)
        self.show()