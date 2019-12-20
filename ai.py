import core, config_core
import ui, config_ui
import random

max_inf = 12 * 12
sign = {1:-2, 2:1}
max_deep = 3

def g(map):
    value = 0
    for line in map.nodes:
        for node in line:
            if node.state != 0:
                for dir in ((0, 1), (1, 0), (1, 1), (-1, 1)):
                    count = 1
                    cur_pos = [node.x, node.y]
                    while True:
                        cur_pos[0] += dir[0]
                        cur_pos[1] += dir[1]
                        if map.get_node(cur_pos[0], cur_pos[1]).state != node.state:
                            break
                        count += 1
                    cur_pos = [node.x, node.y]
                    while True:
                        cur_pos[0] -= dir[0]
                        cur_pos[1] -= dir[1]
                        if map.get_node(cur_pos[0], cur_pos[1]).state != node.state:
                            break
                        count += 1
                    if count == 5:
                        value += sign[node.state] * max_inf
                    if count < 5:
                        value += sign[node.state] * count * count
    return value

def get_turn(map, deep = 1, player = 2, alpha = -max_inf, beta = max_inf):
    childs = {}
    for line in map.nodes:
        for node in line:
            if node.state == 0:
                node.state = player
                res = map.get_line(node, player)
                if deep == max_deep or res:
                    value = g(map)
                else:
                    value = get_turn(map, deep + 1 , player % 2 + 1, alpha, beta)
                if childs.get(value) is None:
                    childs[value] = []
                childs[value].append(node)
                node.state = 0
                if childs.keys():
                    if player == 1:
                        beta = min(beta, min(childs.keys()))
                    else:
                        alpha = max(alpha, max(childs.keys()))
                if beta < alpha:
                    break
    if childs != {}:
        if deep == 1:
            return random.choice(childs[max(childs.keys())])
        else:
            if player == 1:
                return min(childs.keys())
            else:
                return max(childs.keys())
    else:
        return 0
