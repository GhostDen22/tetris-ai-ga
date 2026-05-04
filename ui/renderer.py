import pygame


class BoardRenderer:
    def __init__(self, x=60, y=90, cell_size=28):
        self.x = x
        self.y = y
        self.cell_size = cell_size

        self.empty_color = (24, 28, 36)
        self.filled_color = (61, 174, 233)
        self.grid_color = (55, 60, 72)
        self.border_color = (120, 130, 150)

    def draw(self, surface, board):
        if not board:
            return

        rows = len(board)
        cols = len(board[0]) if rows > 0 else 0

        board_width = cols * self.cell_size
        board_height = rows * self.cell_size

        pygame.draw.rect(
            surface,
            self.border_color,
            (
                self.x - 2,
                self.y - 2,
                board_width + 4,
                board_height + 4,
            ),
            2,
            border_radius=4,
        )

        for row_index, row in enumerate(board):
            for col_index, cell in enumerate(row):
                rect = pygame.Rect(
                    self.x + col_index * self.cell_size,
                    self.y + row_index * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )

                color = self.filled_color if cell else self.empty_color

                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, self.grid_color, rect, 1)