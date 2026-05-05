from core.piece import Piece
from ai.features import extract_features


class Bot:
    DEFAULT_WEIGHTS = {
        "holes": -4.0,
        "aggregate_height": -0.5,
        "max_height": -0.8,
        "bumpiness": -0.7,
        "lines_cleared": 3.0,
    }

    def __init__(self, weights=None):
        self.weights = weights or self.DEFAULT_WEIGHTS
        self.last_features = {}
        self.last_move = None
        self.last_score = 0

    def evaluate_board(self, features):
        score = 0

        for name, value in features.items():
            weight = self.weights.get(name, 0)
            score += weight * value

        return score

    def find_best_move(self, board, piece):
        best_move = None
        best_features = None
        best_score = None

        for rotation_index in range(piece.get_rotation_count()):
            rotated_piece = Piece(piece.name, rotation_index)

            for x in range(-2, board.WIDTH + 2):
                simulated_board, lines_cleared = board.simulate_place(rotated_piece, x)

                if simulated_board is None:
                    continue

                features = extract_features(simulated_board.get_grid(), lines_cleared)
                score = self.evaluate_board(features)

                if best_score is None or score > best_score:
                    best_score = score
                    best_features = features
                    best_move = {
                        "piece": piece.name,
                        "rotation_index": rotation_index,
                        "x": x,
                    }

        self.last_move = best_move
        self.last_features = best_features or {}
        self.last_score = best_score if best_score is not None else 0

        return best_move

    def get_features(self):
        return self.last_features

    def get_last_move(self):
        return self.last_move

    def get_last_score(self):
        return self.last_score