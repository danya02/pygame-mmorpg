import random


class Generator:
    def __init__(self, width, height):
        self.seed = random.randint(0, 100000000000000)
        self.width, self.height = width, height

        random.seed(self.seed)
