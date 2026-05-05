class Piece:
    SHAPES = {
        "I": [(0, 1), (1, 1), (2, 1), (3, 1)],
        "O": [(0, 0), (1, 0), (0, 1), (1, 1)],
        "T": [(1, 0), (0, 1), (1, 1), (2, 1)],
        "S": [(1, 0), (2, 0), (0, 1), (1, 1)],
        "Z": [(0, 0), (1, 0), (1, 1), (2, 1)],
        "J": [(0, 0), (0, 1), (1, 1), (2, 1)],
        "L": [(2, 0), (0, 1), (1, 1), (2, 1)],
    }

    def __init__(self, name):
        if name not in self.SHAPES:
            raise ValueError(f"Unknown piece: {name}")

        self.name = name
        self.blocks = self.SHAPES[name]

    def get_blocks(self):
        return self.blocks