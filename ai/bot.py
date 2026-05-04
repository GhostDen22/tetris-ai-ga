from ai.features import get_fake_features

class Bot:
    def __init__(self):
        self.last_features = get_fake_features()

    def update(self):
        self.last_features = get_fake_features()

    def get_features(self):
        return self.last_features