from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import config_ui
import core, config_core
import ai
import random


def ai_turn(player=2):
    node = ai.get_turn(config_core.map)
    set_turn(config_ui.window.mapUI.nodesUI[node.y][node.x], player)

def set_turn(nodeUI, player):
    core.set_turn(nodeUI.node, player)
    nodeUI.mark = MarkUI(nodeUI, player)
    if config_core.state != "game":
        config_ui.pop_up = QWidget()
        config_ui.pop_up.setWindowTitle("Итог")
        config_ui.pop_up.setFixedSize(300, 100)
        label = QLabel(config_ui.pop_up)
        if config_core.state == "draw":
            label.setText(f"Ничья")
        else:
            label.setText(f"Победитель - игрок {config_core.turn}")
        label.move(30, 30)
        buttonExit = QPushButton("Выход", config_ui.pop_up)
        buttonExit.move(80, 70)
        buttonExit.resize(60, 20)
        buttonExit.clicked.connect(config_ui.window.clickExit)
        buttonExit = QPushButton("Заново", config_ui.pop_up)
        buttonExit.move(160, 70)
        buttonExit.resize(60, 20)
        buttonExit.clicked.connect(config_ui.window.clickRestart)
        config_ui.pop_up.show()


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
        config_ui.Tile = QPixmap(config_ui.Tile).scaled(QSize(config_ui.TileSize, config_ui.TileSize), Qt.KeepAspectRatio)

    def clickExit(self):
        if config_ui.pop_up:
            config_ui.pop_up.close()
        self.close()
    def clickRestart(self):
        if config_ui.pop_up:
            config_ui.pop_up.close()
        for line in self.mapUI.nodesUI:
            for nodeUI in line:
                nodeUI.node.state = 0
                if nodeUI.mark:
                    nodeUI.mark.setParent(None)
                    nodeUI.mark = None
        config_core.state = "game"
        config_core.map.empty_nodes = config_core.map.size[0] * config_core.map.size[1]
        config_core.turn = random.randint(1, 2)
        if config_core.turn == 2:
            ai_turn()

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
        self.setPixmap(config_ui.Tile)

    def mouseReleaseEvent(self, event):
        super(NodeUI, self).mouseReleaseEvent(event)
        if config_core.state == "game":
            if config_core.turn == 1:
                set_turn(self, 1)
                if config_core.state == "game":
                    ai_turn()



class MarkUI(QLabel):
    def __init__(self, node, player):
        super().__init__(config_ui.window)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(config_ui.TileSize, config_ui.TileSize)
        self.setPixmap(config_ui.PlayerMark[player - 1])
        self.move(node.x * config_ui.TileSize, node.y * config_ui.TileSize)
        self.show()

