#!/usr/bin/python3
import pygame
import threading
import random
import time


class Effect(threading.Thread):
    def __init__(self, target):
        super().__init__()
        self.target = target
        self.do_effect = True
        self.running = False
        self.delay = 0.01

    def run(self):
        self.running = True
        while self.running:
            time.sleep(self.delay)
            self.target.image = self.target.original_image


class Poison(Effect):
    def __init__(self, target):
        super().__init__(target)

    def run(self):
        self.running = True
        while self.running:
            time.sleep(self.delay)
            self.target.image = self.target.original_image.copy()
            if self.do_effect:
                for i in range(self.target.image.get_width()):
                    for j in range(self.target.image.get_height()):
                        color = self.target.image.get_at((i, j))
                        color.g = min(color.g + 96, 255)
                        self.target.image.set_at((i, j), color)


class Fire(Effect):
    def __init__(self, target):
        super().__init__(target)

    def run(self):
        self.running = True
        while self.running:
            time.sleep(self.delay)
            self.target.image = self.target.original_image.copy()
            if self.do_effect:
                for i in range(self.target.image.get_width()):
                    for j in range(self.target.image.get_height()):
                        if random.randint(0, 1000) > 800 and self.target.image.get_at((i, j)).a != 0:
                            self.target.image.set_at((i, j), pygame.Color('red'))
