import sys
import time
import pygame
from src.maze import Maze
from src.astar import a_star_search
from src.bfs import bfs_search
from src.maze_generator import generate_random_maze

# Window settings
CELL_SIZE = 40
MARGIN = 2
EXPLORATION_DELAY = 0.03
PATH_DELAY = 0.08

# Colors
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
GREEN = (50, 200, 100)
RED = (220, 60, 60)
BLUE = (70, 130, 255)
YELLOW = (255, 215, 0)
LIGHT_GREY = (200, 200, 200)
BACKGROUND = (240, 240, 240)


def draw_maze(screen, maze, explored_positions, path_positions):
    for row in range(maze.rows):
        for col in range(maze.cols):
            cell = maze.grid[row][col]

            x = col * (CELL_SIZE + MARGIN)
            y = row * (CELL_SIZE + MARGIN)

            if cell == "#":
                color = BLACK
            elif cell == "S":
                color = GREEN
            elif cell == "G":
                color = RED
            elif (row, col) in path_positions:
                color = BLUE
            elif (row, col) in explored_positions:
                color = YELLOW
            else:
                color = WHITE

            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, LIGHT_GREY, (x, y, CELL_SIZE, CELL_SIZE), 1)


def handle_quit_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def load_maze_and_algorithm():
    algorithm = "astar"
    heuristic = "manhattan"

    if len(sys.argv) > 1 and sys.argv[1] == "--random":
        size = 10
        if len(sys.argv) > 2:
            size = int(sys.argv[2])
        if len(sys.argv) > 3:
            algorithm = sys.argv[3].lower()

        grid = generate_random_maze(size)
        maze = Maze(grid)
        print(f"Generated random maze: {size}x{size}")
        return maze, algorithm, heuristic

    maze_file = "mazes/simple_maze.txt"
    if len(sys.argv) > 1:
        maze_file = sys.argv[1]
    if len(sys.argv) > 2:
        algorithm = sys.argv[2].lower()

    maze = Maze.from_file(maze_file)
    print(f"Loaded maze: {maze_file}")
    return maze, algorithm, heuristic


def animate_exploration(screen, maze, explored_order):
    explored_positions = set()

    for position in explored_order:
        if maze.grid[position[0]][position[1]] not in ("S", "G"):
            explored_positions.add(position)

        screen.fill(BACKGROUND)
        draw_maze(screen, maze, explored_positions, set())
        pygame.display.flip()

        handle_quit_events()
        time.sleep(EXPLORATION_DELAY)

    return explored_positions


def animate_path(screen, maze, explored_positions, path):
    path_positions = set()

    if not path:
        return path_positions

    for position in path:
        if maze.grid[position[0]][position[1]] not in ("S", "G"):
            path_positions.add(position)

        screen.fill(BACKGROUND)
        draw_maze(screen, maze, explored_positions, path_positions)
        pygame.display.flip()

        handle_quit_events()
        time.sleep(PATH_DELAY)

    return path_positions

def run_algorithm(maze, algorithm, heuristic):
    if algorithm == "bfs":
        path, cost, explored, explored_order = bfs_search(maze)
        return path, cost, explored, explored_order

    path, cost, explored, explored_order = a_star_search(maze, heuristic)
    return path, cost, explored, explored_order

def main():
    try:
        maze, algorithm, heuristic = load_maze_and_algorithm()

        path, cost, explored, explored_order = run_algorithm(maze, algorithm, heuristic)

        print(f"Algorithm: {algorithm.upper()}")
        if algorithm == "astar":
            print(f"Heuristic: {heuristic}")

        if path:
            print(f"Path cost: {cost}")
            print(f"Nodes explored: {explored}")
        else:
            print("No path found.")
            print(f"Nodes explored: {explored}")

        pygame.init()
        width = maze.cols * (CELL_SIZE + MARGIN) - MARGIN
        height = maze.rows * (CELL_SIZE + MARGIN) - MARGIN
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(f"AI Maze Solver - {algorithm.upper()} Visualizer")

        screen.fill(BACKGROUND)
        draw_maze(screen, maze, set(), set())
        pygame.display.flip()
        pygame.time.wait(400)

        explored_positions = animate_exploration(screen, maze, explored_order)
        final_path_positions = animate_path(screen, maze, explored_positions, path)

        running = True
        while running:
            handle_quit_events()

            screen.fill(BACKGROUND)
            draw_maze(screen, maze, explored_positions, final_path_positions)
            pygame.display.flip()

        pygame.quit()

    except FileNotFoundError:
        print("Error: Maze file not found.")
    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()