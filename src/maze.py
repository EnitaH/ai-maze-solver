class Maze:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0

        self.validate_grid()

        self.start = self.find_symbol("S")
        self.goal = self.find_symbol("G")

    @classmethod
    def from_file(cls, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            grid = [list(line.strip()) for line in file if line.strip()]
        return cls(grid)

    def validate_grid(self):
        if not self.grid:
            raise ValueError("Maze grid cannot be empty.")

        row_length = len(self.grid[0])
        for row in self.grid:
            if len(row) != row_length:
                raise ValueError("All maze rows must have the same length.")

        start_count = sum(row.count("S") for row in self.grid)
        goal_count = sum(row.count("G") for row in self.grid)

        if start_count != 1:
            raise ValueError("Maze must contain exactly one start position 'S'.")

        if goal_count != 1:
            raise ValueError("Maze must contain exactly one goal position 'G'.")

    def find_symbol(self, symbol):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == symbol:
                    return (r, c)
        return None

    def is_within_bounds(self, position):
        r, c = position
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_walkable(self, position):
        r, c = position
        return self.grid[r][c] != "#"

    def get_neighbors(self, position):
        r, c = position
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        neighbors = []
        for dr, dc in moves:
            new_pos = (r + dr, c + dc)
            
            if self.is_within_bounds(new_pos) and self.is_walkable(new_pos):
                neighbors.append(new_pos)

        return neighbors