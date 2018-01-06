#!/usr/bin/python3
import pygame
import threading
import random


class Effect(threading.Thread):
    def __init__(self, target):
        super().__init__()
        self.target = target
        self.do_effect = True

    def run(self):
        pass


class Poison(Effect):
    def __init__(self, target):
        super().__init__(target)

    def run(self):
        if self.target.image.get_at((0, 0)) != pygame.Color(0, 255, 0, 127):
            self.target.image.set_at((0, 0), pygame.Color(0, 255, 0, 127))
            for i in range(self.target.image.get_width()):
                for j in range(self.target.image.get_height()):
                    color = self.target.image.get_at((i, j))
                    color.g = min(color.g + 64, 255)
                    self.target.image.set_at((i, j), color)


class Fire(Effect):
    def __init__(self, target):
        super().__init__(target)

    def run(self):
        if self.target.image.get_at((0, 0)) != pygame.Color(255, 0, 0, 255):
            self.target.image.set_at((0, 0), pygame.Color(255, 0, 0, 255))
            for i in range(self.target.image.get_width()):
                for j in range(self.target.image.get_height()):
                    if random.randint(0, 1000)>750:
                        self.target.image.set_at((i, j), pygame.Color('red'))
