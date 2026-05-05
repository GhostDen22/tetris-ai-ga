class Board:
    WIDTH = 10
    HEIGHT = 20

    def __init__(self):
        self.grid = [[0 for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]

    def get_grid(self):
        return self.grid

    def can_place(self, piece, piece_x, piece_y):
        for block_x, block_y in piece.get_blocks():
            x = piece_x + block_x
            y = piece_y + block_y

            if x < 0 or x >= self.WIDTH:
                return False

            if y < 0 or y >= self.HEIGHT:
                return False

            if self.grid[y][x] != 0:
                return False

        return True

    def place_piece(self, piece, piece_x, piece_y):
        for block_x, block_y in piece.get_blocks():
            x = piece_x + block_x
            y = piece_y + block_y

            if 0 <= x < self.WIDTH and 0 <= y < self.HEIGHT:
                self.grid[y][x] = 1

    def clear_lines(self):
        new_grid = []
        cleared = 0

        for row in self.grid:
            if all(cell != 0 for cell in row):
                cleared += 1
            else:
                new_grid.append(row)

        while len(new_grid) < self.HEIGHT:
            new_grid.insert(0, [0 for _ in range(self.WIDTH)])

        self.grid = new_grid
        return cleared

    def get_grid_with_piece(self, piece, piece_x, piece_y):
        visible_grid = [row[:] for row in self.grid]

        for block_x, block_y in piece.get_blocks():
            x = piece_x + block_x
            y = piece_y + block_y

            if 0 <= x < self.WIDTH and 0 <= y < self.HEIGHT:
                visible_grid[y][x] = 1

        return visible_grid