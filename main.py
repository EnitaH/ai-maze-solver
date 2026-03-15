import sys
from src.maze import Maze
from src.astar import a_star_search


def print_maze(grid):
    for row in grid:
        print("".join(row))


def mark_path(grid, path):
    new_grid = [row[:] for row in grid]

    for row, col in path:
        if new_grid[row][col] not in ("S", "G"):
            new_grid[row][col] = "*"

    return new_grid


def main():
    maze_file = "mazes/simple_maze.txt"
    heuristic = "manhattan"

    if len(sys.argv) > 1:
        maze_file = sys.argv[1]

    if len(sys.argv) > 2:
        heuristic = sys.argv[2].lower()

    maze = Maze.from_file(maze_file)

    print(f"Loaded maze: {maze_file}")
    print(f"Heuristic: {heuristic}")
    print("\nOriginal Maze:")
    print_maze(maze.grid)

    path, cost, explored = a_star_search(maze, heuristic)

    if path:
        solved_grid = mark_path(maze.grid, path)
        print("\nSolved Maze:")
        print_maze(solved_grid)
        print(f"\nPath cost: {cost}")
        print(f"Nodes explored: {explored}")
    else:
        print("\nNo path found.")
        print(f"Nodes explored: {explored}")


if __name__ == "__main__":
    main()