import random


def generate_random_maze(size=10, wall_probability=0.3):
    grid = []

    for row in range(size):
        current_row = []

        for col in range(size):

            if (row, col) == (0, 0):
                current_row.append("S")

            elif (row, col) == (size - 1, size - 1):
                current_row.append("G")

            else:
                if random.random() < wall_probability:
                    current_row.append("#")
                else:
                    current_row.append(".")

        grid.append(current_row)

    # ensure start neighbors are open
    if size > 1:
        grid[0][1] = "."
        grid[1][0] = "."

    # ensure goal neighbors are open
    if size > 1:
        grid[size-1][size-2] = "."
        grid[size-2][size-1] = "."

    return grid