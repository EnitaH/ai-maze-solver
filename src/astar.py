import heapq
from src.node import Node
from src.heuristics import manhattan_distance


def reconstruct_path(current_node):
    path = []
    while current_node is not None:
        path.append(current_node.position)
        current_node = current_node.parent
    return path[::-1]


def a_star_search(maze):
    start_node = Node(maze.start)
    goal_position = maze.goal

    open_list = []
    heapq.heappush(open_list, start_node)

    closed_set = set()
    explored_nodes = 0

    while open_list:
        current_node = heapq.heappop(open_list)
        explored_nodes += 1

        if current_node.position == goal_position:
            return reconstruct_path(current_node), current_node.g, explored_nodes

        closed_set.add(current_node.position)

        for neighbor_pos in maze.get_neighbors(current_node.position):
            if neighbor_pos in closed_set:
                continue

            neighbor_node = Node(neighbor_pos, current_node)
            neighbor_node.g = current_node.g + 1
            neighbor_node.h = manhattan_distance(neighbor_pos, goal_position)
            neighbor_node.f = neighbor_node.g + neighbor_node.h

            skip_node = False
            for open_node in open_list:
                if neighbor_node.position == open_node.position and neighbor_node.g >= open_node.g:
                    skip_node = True
                    break

            if not skip_node:
                heapq.heappush(open_list, neighbor_node)

    return None, None, explored_nodes