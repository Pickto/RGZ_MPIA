import config_core

def set_turn(node, player):
    node.set_state(player)
    res = config_core.map.get_line(node, player)
    if res:
        config_core.state = f"win{player}"
        return
    config_core.turn = (player + 1) % 3


class Map:
    def __init__(self, size = (10,13)):
        self.size = size
        self.empty = Node(None, None, -1)
        self.nodes = []
        for i in range(size[1]):
            self.nodes.append([])
            for j in range(size[0]):
                self.nodes[i].append(Node(j, i))
        self.empty_nodes = size[0] * size[1]

    def get_node(self, x, y):
        if x < 0 or y < 0 or x > self.size[0] or y > self.size[1]:
            return self.empty
        return self.nodes[y][x]

    def get_line(self, node, state):
        for dir in ((0, 1), (1, 0), (1, 1)):
            count = 0
            cur_pos = [node.x, node.y]
            while True:
                cur_pos[0] += dir[0]
                cur_pos[1] += dir[1]
                if self.get_node(cur_pos[0], cur_pos[1]).state != state:
                    break
                count += 1
            cur_pos = [node.x, node.y]
            while True:
                cur_pos[0] -= dir[0]
                cur_pos[1] -= dir[1]
                if self.get_node(cur_pos[0], cur_pos[1]).state != state:
                    break
                count += 1
            if count == 4:
                return True
        return False


class Node:
    def __init__(self, x, y, state=0):
        self.state = state
        self.x = x
        self.y = y

    def set_state(self, state):
        if self.state == 0:
            self.state = state

