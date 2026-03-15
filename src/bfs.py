from collections import deque
from src.node import Node


def reconstruct_path(current_node):
    path = []
    while current_node is not None:
        path.append(current_node.position)
        current_node = current_node.parent
    return path[::-1]


def bfs_search(maze):
    start_node = Node(maze.start)

    queue = deque([start_node])
    visited = {maze.start}

    explored_nodes = 0

    while queue:
        current_node = queue.popleft()
        explored_nodes += 1

        if current_node.position == maze.goal:
            path = reconstruct_path(current_node)
            return path, len(path) - 1, explored_nodes

        for neighbor in maze.get_neighbors(current_node.position):

            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(Node(neighbor, current_node))

    return None, None, explored_nodes