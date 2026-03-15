import sys
from src.maze import Maze
from src.astar import a_star_search
from src.maze_generator import generate_random_maze
from src.bfs import bfs_search


def print_maze(grid):
    for row in grid:
        print(" ".join(row))


def mark_path(grid, path):
    new_grid = [row[:] for row in grid]

    for row, col in path:
        if new_grid[row][col] not in ("S", "G"):
            new_grid[row][col] = "*"

    return new_grid


def run_solver(maze, heuristic):
    print(f"\n=== Algorithm: A* ({heuristic.capitalize()}) ===")

    print("\nOriginal Maze:")
    print_maze(maze.grid)

    path, cost, explored, _ = a_star_search(maze, heuristic)

    if path:
        solved_grid = mark_path(maze.grid, path)
        print("\nSolved Maze:")
        print_maze(solved_grid)
        print(f"\nPath cost: {cost}")
        print(f"Nodes explored: {explored}")
    else:
        print("\nNo path found.")
        print(f"Nodes explored: {explored}")


def run_bfs(maze):
    print("\n=== Algorithm: BFS ===")

    print("\nOriginal Maze:")
    print_maze(maze.grid)

    path, cost, explored = bfs_search(maze)

    if path:
        solved_grid = mark_path(maze.grid, path)
        print("\nSolved Maze:")
        print_maze(solved_grid)
        print(f"\nPath cost: {cost}")
        print(f"Nodes explored: {explored}")
    else:
        print("\nNo path found.")
        print(f"Nodes explored: {explored}")


def main():
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "--random":
            size = 10

            if len(sys.argv) > 2:
                size = int(sys.argv[2])

            grid = generate_random_maze(size)
            maze = Maze(grid)

            print(f"Generated random maze: {size}x{size}")

        else:
            maze_file = "mazes/simple_maze.txt"

            if len(sys.argv) > 1:
                maze_file = sys.argv[1]

            maze = Maze.from_file(maze_file)
            print(f"Loaded maze: {maze_file}")

        run_solver(maze, "manhattan")
        run_solver(maze, "euclidean")
        run_bfs(maze)


    except FileNotFoundError:
        print(f"Error: File '{maze_file}' not found.")
    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()