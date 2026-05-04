from core.board import Board

class Game:
    def __init__(self):
        self.board = Board()
        self.score = 0
        self.lines = 0
        self.seed = 42

        self.board.fill_test_pattern()

    def get_board(self):
        return self.board.get_grid()

    def get_score(self):
        return self.score

    def get_lines(self):
        return self.lines

    def get_seed(self):
        return self.seed