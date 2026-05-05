from ai.features import extract_features


class Bot:
    def __init__(self):
        self.last_features = {}

    def update(self, board_grid, lines_cleared=0):
        self.last_features = extract_features(board_grid, lines_cleared)

    def get_features(self):
        return self.last_features