import sys
import pygame
from src.maze import Maze
from src.astar import a_star_search
from src.maze_generator import generate_random_maze

# Window settings
CELL_SIZE = 40
MARGIN = 2

# Colors
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
GREEN = (50, 200, 100)
RED = (220, 60, 60)
BLUE = (70, 130, 255)
LIGHT_GREY = (200, 200, 200)


def mark_path_positions(path):
    return set(path) if path else set()



def draw_maze(screen, maze, path_positions):
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
            else:
                color = WHITE

            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, LIGHT_GREY, (x, y, CELL_SIZE, CELL_SIZE), 1)


def load_maze_from_args():
    if len(sys.argv) > 1 and sys.argv[1] == "--random":
        size = 10
        if len(sys.argv) > 2:
            size = int(sys.argv[2])

        grid = generate_random_maze(size)
        maze = Maze(grid)
        print(f"Generated random maze: {size}x{size}")
        return maze

    maze_file = "mazes/simple_maze.txt"
    if len(sys.argv) > 1:
        maze_file = sys.argv[1]

    maze = Maze.from_file(maze_file)
    print(f"Loaded maze: {maze_file}")
    return maze


def main():
    try:
        maze = load_maze_from_args()
        path, cost, explored = a_star_search(maze, "manhattan")

        if path:
            print(f"Path cost: {cost}")
            print(f"Nodes explored: {explored}")
        else:
            print("No path found.")
            print(f"Nodes explored: {explored}")

        path_positions = mark_path_positions(path)

        pygame.init()
        width = maze.cols * (CELL_SIZE + MARGIN) - MARGIN
        height = maze.rows * (CELL_SIZE + MARGIN) - MARGIN
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("AI Maze Solver - A* Visualizer")

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((240, 240, 240))
            draw_maze(screen, maze, path_positions)
            pygame.display.flip()

        pygame.quit()

    except FileNotFoundError:
        print("Error: Maze file not found.")
    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()