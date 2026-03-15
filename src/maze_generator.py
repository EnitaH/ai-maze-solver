import random


def generate_random_maze(size=10, wall_probability=0.3):
    # Start with all open cells
    grid = [["." for _ in range(size)] for _ in range(size)]

    # Set start and goal
    grid[0][0] = "S"
    grid[size - 1][size - 1] = "G"

    # Create a guaranteed path from S to G
    row, col = 0, 0
    path_cells = {(row, col)}

    while row < size - 1 or col < size - 1:
        if row == size - 1:
            col += 1
        elif col == size - 1:
            row += 1
        else:
            if random.choice([True, False]):
                row += 1
            else:
                col += 1

        path_cells.add((row, col))

    # Add random walls everywhere except the guaranteed path, start, and goal
    for r in range(size):
        for c in range(size):
            if (r, c) not in path_cells and (r, c) != (0, 0) and (r, c) != (size - 1, size - 1):
                if random.random() < wall_probability:
                    grid[r][c] = "#"

    return grid