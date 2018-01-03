#!/usr/bin/python3
import threading

import pygame


class Window(threading.Thread):
    def __init__(self):
        self.display = pygame.display.set_mode((800, 600))
        self.on_keypress = lambda x: None
        self.on_keyrelease = lambda x: None
        self.last_pressed = pygame.key.get_pressed()
        self.draw = lambda x: None

    def update(self):
        self.draw(self)
        pygame.display.flip()

    def run(self):
        keys = pygame.key.get_pressed()
        for key, before, after in zip(range(len(keys)), self.last_pressed, keys):
            if before and not after:
                self.on_keyrelease(key)
            elif not before and after:
                self.on_keypress(key)
