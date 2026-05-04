class Board:
    WIDTH = 10
    HEIGHT = 20

    def __init__(self):
        self.grid = [[0 for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]

    def get_grid(self):
        return self.grid

    def fill_test_pattern(self):
        # tylko do testów UI
        for y in range(self.HEIGHT - 5, self.HEIGHT):
            for x in range(self.WIDTH):
                if (x + y) % 2 == 0:
                    self.grid[y][x] = 1