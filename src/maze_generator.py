import random


def generate_random_maze(rows=10, cols=10, wall_probability=0.3):
    # Start with all open cells
    grid = [["." for _ in range(cols)] for _ in range(rows)]

    # Set start and goal
    grid[0][0] = "S"
    grid[rows - 1][cols - 1] = "G"

    # Create a guaranteed path from S to G
    row, col = 0, 0
    path_cells = {(row, col)}

    while row < rows - 1 or col < cols - 1:
        if row == rows - 1:
            col += 1
        elif col == cols - 1:
            row += 1
        else:
            if random.choice([True, False]):
                row += 1
            else:
                col += 1

        path_cells.add((row, col))

    # Add random walls everywhere except the guaranteed path
    for r in range(rows):
        for c in range(cols):
            if (r, c) not in path_cells and (r, c) != (0, 0) and (r, c) != (rows - 1, cols - 1):
                if random.random() < wall_probability:
                    grid[r][c] = "#"

    return grid