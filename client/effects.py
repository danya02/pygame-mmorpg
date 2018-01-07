#!/usr/bin/python3
import pygame
import threading
import random
import time
import math


class Effect(threading.Thread):
    def __init__(self, target=None):
        super().__init__()
        self.target = target
        self.do_effect = True
        self.running = False
        self.delay = 0.01

    def run(self):
        self.running = True
        while self.running:
            if self.target is not None:
                time.sleep(self.delay)
                self.target.image = self.target.original_image.copy()


class Poison(Effect):
    def __init__(self, target=None):
        super().__init__(target)

    def run(self):
        self.running = True
        while self.running:
            if self.target is not None:
                time.sleep(self.delay)
                self.target.image = self.target.original_image.copy()
                if self.do_effect:
                    for i in range(self.target.image.get_width()):
                        for j in range(self.target.image.get_height()):
                            color = self.target.image.get_at((i, j))
                            color.g = min(color.g + 96, 255)
                            self.target.image.set_at((i, j), color)


class Fire(Effect):
    def __init__(self, target=None):
        super().__init__(target)

    def run(self):
        self.running = True
        while self.running:
            if self.target is not None:
                time.sleep(self.delay)
                self.target.image = self.target.original_image.copy()
                if self.do_effect:
                    for i in range(self.target.image.get_width()):
                        for j in range(self.target.image.get_height()):
                            if random.random() > 1 - (j / self.target.image.get_height()) * abs(
                                    math.sin(time.time())) and self.target.image.get_at((i, j)).a != 0:
                                self.target.image.set_at((i, j), pygame.Color('orange' if random.randint(0, 1) else 'red'))


def get_effect(effect_id: str) -> Effect:
    return Effect()
