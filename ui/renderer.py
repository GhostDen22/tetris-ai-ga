import pygame


class BoardRenderer:
    def __init__(self, x=25, y=50, cell_size=28):
        self.x = x
        self.y = y
        self.cell_size = cell_size

        self.header_height = 70
        self.padding = 16

        self.card_color = (20, 24, 32)
        self.card_border_color = (72, 84, 105)

        self.empty_color = (25, 30, 39)
        self.grid_color = (55, 64, 78)
        self.board_border_color = (126, 144, 170)

        self.tetromino_colors = [
            (58, 175, 235),
            (118, 214, 255),
            (90, 200, 140),
            (245, 200, 80),
            (245, 135, 95),
            (180, 135, 245),
            (235, 95, 135),
        ]

        self.font_title = pygame.font.SysFont("arial", 24, bold=True)
        self.font_small = pygame.font.SysFont("arial", 14)

    def draw_text(self, surface, text, x, y, font, color):
        rendered = font.render(str(text), True, color)
        surface.blit(rendered, (x, y))

    def get_cell_color(self, cell):
        if cell in (0, None, False):
            return self.empty_color

        if isinstance(cell, int):
            return self.tetromino_colors[cell % len(self.tetromino_colors)]

        return self.tetromino_colors[0]

    def draw(self, surface, board):
        if not board:
            return

        rows = len(board)
        cols = len(board[0]) if rows > 0 else 0

        board_width = cols * self.cell_size
        board_height = rows * self.cell_size

        card_width = board_width + self.padding * 2
        card_height = board_height + self.header_height + self.padding * 2

        pygame.draw.rect(
            surface,
            self.card_color,
            (self.x, self.y, card_width, card_height),
            border_radius=16,
        )

        pygame.draw.rect(
            surface,
            self.card_border_color,
            (self.x, self.y, card_width, card_height),
            2,
            border_radius=16,
        )

        self.draw_text(
            surface,
            "Board",
            self.x + 16,
            self.y + 14,
            self.font_title,
            (245, 247, 250),
        )

        self.draw_text(
            surface,
            "Backend state from game.get_board()",
            self.x + 16,
            self.y + 42,
            self.font_small,
            (150, 160, 175),
        )

        board_x = self.x + self.padding
        board_y = self.y + self.header_height

        pygame.draw.rect(
            surface,
            self.board_border_color,
            (
                board_x - 2,
                board_y - 2,
                board_width + 4,
                board_height + 4,
            ),
            2,
            border_radius=6,
        )

        for row_index, row in enumerate(board):
            for col_index, cell in enumerate(row):
                rect = pygame.Rect(
                    board_x + col_index * self.cell_size,
                    board_y + row_index * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )

                pygame.draw.rect(surface, self.get_cell_color(cell), rect)
                pygame.draw.rect(surface, self.grid_color, rect, 1)