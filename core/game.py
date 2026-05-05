import random

from core.board import Board
from core.piece import Piece


class Game:
    def __init__(self, seed=42):
        self.board = Board()
        self.score = 0
        self.lines = 0
        self.seed = seed
        self.random = random.Random(seed)

        self.current_piece = None
        self.current_x = 0
        self.current_y = 0
        self.game_over = False

        self.spawn_piece()

    def spawn_piece(self):
        piece_name = self.random.choice(["I", "O", "T", "S", "Z", "J", "L"])

        self.current_piece = Piece(piece_name)
        self.current_x = 3
        self.current_y = 0

        if not self.board.can_place(self.current_piece, self.current_x, self.current_y):
            self.game_over = True

    def step(self):
        if self.game_over:
            return

        if self.board.can_place(self.current_piece, self.current_x, self.current_y + 1):
            self.current_y += 1
        else:
            self.lock_piece()

    def lock_piece(self):
        self.board.place_piece(self.current_piece, self.current_x, self.current_y)

        cleared = self.board.clear_lines()

        if cleared > 0:
            self.lines += cleared
            self.score += cleared * 100

        self.spawn_piece()

    def get_board(self):
        if self.current_piece is None:
            return self.board.get_grid()

        return self.board.get_grid_with_piece(
            self.current_piece,
            self.current_x,
            self.current_y
        )

    def get_score(self):
        return self.score

    def get_lines(self):
        return self.lines

    def get_seed(self):
        return self.seed

    def is_game_over(self):
        return self.game_over