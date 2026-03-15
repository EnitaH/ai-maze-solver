import heapq
from src.node import Node
from src.heuristics import manhattan_distance, euclidean_distance


def reconstruct_path(current_node):
    path = []
    while current_node is not None:
        path.append(current_node.position)
        current_node = current_node.parent
    return path[::-1]


def a_star_search(maze, heuristic_name="manhattan"):
    
    goal_position = maze.goal

    if heuristic_name == "euclidean":
        heuristic_function = euclidean_distance
    else:
        heuristic_function = manhattan_distance

    start_node = Node(maze.start)
    start_node.g = 0
    start_node.h = heuristic_function(maze.start, goal_position)
    start_node.f = start_node.g + start_node.h

    open_list = []
    heapq.heappush(open_list, start_node)

    closed_set = set()
    best_g = {maze.start: 0}
    explored_nodes = 0

    while open_list:
        current_node = heapq.heappop(open_list)

        if current_node.position in closed_set:
            continue

        explored_nodes += 1

        if current_node.position == goal_position:
            return reconstruct_path(current_node), current_node.g, explored_nodes

        closed_set.add(current_node.position)

        for neighbor_pos in maze.get_neighbors(current_node.position):
            if neighbor_pos in closed_set:
                continue

            tentative_g = current_node.g + 1

            if neighbor_pos not in best_g or tentative_g < best_g[neighbor_pos]:
                best_g[neighbor_pos] = tentative_g

                neighbor_node = Node(neighbor_pos, current_node)
                neighbor_node.g = tentative_g
                neighbor_node.h = heuristic_function(neighbor_pos, goal_position)
                neighbor_node.f = neighbor_node.g + neighbor_node.h



                heapq.heappush(open_list, neighbor_node)

    return None, None, explored_nodes