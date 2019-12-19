import config_core

def set_turn(node, player):
    node.set_state(player)
    config_core.map.empty_nodes -= 1
    res = config_core.map.get_line(node, player)
    if res:
        config_core.state = f"win{player}"
        return
    if config_core.map.empty_nodes == 0:
        config_core.state = "draw"
        return
    config_core.turn = player % 2 + 1


class Map:
    def __init__(self):
        self.size = (config_core.size_x, config_core.size_y)
        self.empty = Node(None, None, -1)
        self.nodes = []
        for i in range(self.size[1]):
            self.nodes.append([])
            for j in range(self.size[0]):
                self.nodes[i].append(Node(j, i))
        self.empty_nodes = self.size[0] * self.size[1]

    def get_node(self, x, y):
        if x < 0 or y < 0 or x >= self.size[0] or y >= self.size[1]:
            return self.empty
        return self.nodes[y][x]

    def get_line(self, node, state):
        for dir in ((0, 1), (1, 0), (1, 1), (-1, 1)):
            count = 1
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
            if count == 5:
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

