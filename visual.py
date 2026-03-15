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
SIDE_PANEL_WIDTH = 260
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
PANEL_BG = (225, 225, 225)
TEXT_COLOR = (40, 40, 40)


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


def draw_stats_panel(screen, maze, algorithm, heuristic, cost, explored, random_mode, rows, cols):
    maze_width = maze.cols * (CELL_SIZE + MARGIN) - MARGIN
    panel_x = maze_width + 20

    pygame.draw.rect(
        screen,
        PANEL_BG,
        (maze_width, 0, SIDE_PANEL_WIDTH, max(maze.rows * (CELL_SIZE + MARGIN), 500))
    )

    font_title = pygame.font.SysFont(None, 30)
    font_text = pygame.font.SysFont(None, 24)

    random_size_text = f"{rows}x{cols}" if random_mode else "N/A"

    lines = [
        ("Maze Solver Stats", font_title),
        ("", font_text),
        (f"Algorithm: {algorithm.upper()}", font_text),
        (f"Heuristic: {heuristic if algorithm == 'astar' else 'N/A'}", font_text),
        (f"Maze size: {maze.rows}x{maze.cols}", font_text),
        (f"Path cost: {cost if cost is not None else 'No path'}", font_text),
        (f"Nodes explored: {explored}", font_text),
        ("", font_text),
        ("Controls:", font_title),
        ("A - Switch to A*", font_text),
        ("B - Switch to BFS", font_text),
        ("R - New random maze", font_text),
        ("ESC - Quit", font_text),
        ("", font_text),
        (f"Random mode: {'Yes' if random_mode else 'No'}", font_text),
        (f"Random size: {random_size_text}", font_text),
    ]

    y = 25
    for text, font in lines:
        surface = font.render(text, True, TEXT_COLOR)
        screen.blit(surface, (panel_x, y))
        y += 35 if font == font_title else 28


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "quit"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "quit"
            if event.key == pygame.K_a:
                return "astar"
            if event.key == pygame.K_b:
                return "bfs"
            if event.key == pygame.K_r:
                return "random"

    return None


def load_initial_config():
    algorithm = "astar"
    heuristic = "manhattan"
    random_mode = False
    rows = 10
    cols = 10
    maze_file = "mazes/simple_maze.txt"

    if len(sys.argv) > 1 and sys.argv[1] == "--random":
        random_mode = True

        if len(sys.argv) > 2:
            rows = int(sys.argv[2])
            cols = rows

        if len(sys.argv) > 3:
            algorithm = sys.argv[3].lower()

    else:
        if len(sys.argv) > 1:
            maze_file = sys.argv[1]

        if len(sys.argv) > 2:
            algorithm = sys.argv[2].lower()

    return random_mode, rows, cols, maze_file, algorithm, heuristic


def build_maze(random_mode, rows, cols, maze_file):
    if random_mode:
        grid = generate_random_maze(rows, cols)
        maze = Maze(grid)
        print(f"Generated random maze: {rows}x{cols}")
        return maze

    maze = Maze.from_file(maze_file)
    print(f"Loaded maze: {maze_file}")
    return maze


def resize_window_for_maze(maze):
    maze_width = maze.cols * (CELL_SIZE + MARGIN) - MARGIN
    maze_height = maze.rows * (CELL_SIZE + MARGIN) - MARGIN
    width = maze_width + SIDE_PANEL_WIDTH
    height = max(maze_height, 500)
    return pygame.display.set_mode((width, height))


def animate_exploration(screen, maze, explored_order, algorithm, heuristic, cost, explored, random_mode, rows, cols):
    explored_positions = set()

    for position in explored_order:
        if maze.grid[position[0]][position[1]] not in ("S", "G"):
            explored_positions.add(position)

        screen.fill(BACKGROUND)
        draw_maze(screen, maze, explored_positions, set())
        draw_stats_panel(screen, maze, algorithm, heuristic, cost, explored, random_mode, rows, cols)
        pygame.display.flip()

        action = handle_events()
        if action == "quit":
            pygame.quit()
            sys.exit()

        time.sleep(EXPLORATION_DELAY)

    return explored_positions


def animate_path(screen, maze, explored_positions, path, algorithm, heuristic, cost, explored, random_mode, rows, cols):
    path_positions = set()

    if not path:
        return path_positions

    for position in path:
        if maze.grid[position[0]][position[1]] not in ("S", "G"):
            path_positions.add(position)

        screen.fill(BACKGROUND)
        draw_maze(screen, maze, explored_positions, path_positions)
        draw_stats_panel(screen, maze, algorithm, heuristic, cost, explored, random_mode, rows, cols)
        pygame.display.flip()

        action = handle_events()
        if action == "quit":
            pygame.quit()
            sys.exit()

        time.sleep(PATH_DELAY)

    return path_positions


def run_algorithm(maze, algorithm, heuristic):
    if algorithm == "bfs":
        path, cost, explored, explored_order = bfs_search(maze)
        return path, cost, explored, explored_order

    path, cost, explored, explored_order = a_star_search(maze, heuristic)
    return path, cost, explored, explored_order


def solve_and_animate(screen, maze, algorithm, heuristic, random_mode, rows, cols):
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

    screen.fill(BACKGROUND)
    draw_maze(screen, maze, set(), set())
    draw_stats_panel(screen, maze, algorithm, heuristic, cost, explored, random_mode, rows, cols)
    pygame.display.flip()
    pygame.time.wait(400)

    explored_positions = animate_exploration(
        screen, maze, explored_order, algorithm, heuristic, cost, explored, random_mode, rows, cols
    )

    final_path_positions = animate_path(
        screen, maze, explored_positions, path, algorithm, heuristic, cost, explored, random_mode, rows, cols
    )

    return cost, explored, explored_positions, final_path_positions


def main():
    try:
        random_mode, rows, cols, maze_file, algorithm, heuristic = load_initial_config()
        maze = build_maze(random_mode, rows, cols, maze_file)

        pygame.init()
        screen = resize_window_for_maze(maze)
        pygame.display.set_caption("AI Maze Solver Visualizer")

        cost, explored, explored_positions, final_path_positions = solve_and_animate(
            screen, maze, algorithm, heuristic, random_mode, rows, cols
        )

        running = True
        while running:
            action = handle_events()

            if action == "quit":
                running = False

            elif action == "astar":
                algorithm = "astar"
                maze = build_maze(random_mode, rows, cols, maze_file)
                screen = resize_window_for_maze(maze)
                cost, explored, explored_positions, final_path_positions = solve_and_animate(
                    screen, maze, algorithm, heuristic, random_mode, rows, cols
                )

            elif action == "bfs":
                algorithm = "bfs"
                maze = build_maze(random_mode, rows, cols, maze_file)
                screen = resize_window_for_maze(maze)
                cost, explored, explored_positions, final_path_positions = solve_and_animate(
                    screen, maze, algorithm, heuristic, random_mode, rows, cols
                )

            elif action == "random":
                random_mode = True
                rows = maze.rows
                cols = maze.cols
                maze = build_maze(random_mode, rows, cols, maze_file)
                screen = resize_window_for_maze(maze)
                cost, explored, explored_positions, final_path_positions = solve_and_animate(
                    screen, maze, algorithm, heuristic, random_mode, rows, cols
                )

            screen.fill(BACKGROUND)
            draw_maze(screen, maze, explored_positions, final_path_positions)
            draw_stats_panel(screen, maze, algorithm, heuristic, cost, explored, random_mode, rows, cols)
            pygame.display.flip()

        pygame.quit()

    except FileNotFoundError:
        print("Error: Maze file not found.")
    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()