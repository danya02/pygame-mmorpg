#!/usr/bin/python3
import threading

import pygame


class Window(threading.Thread):
    def __init__(self):
        super().__init__()
        self.loop = True
        self.daemon = True
        self.display = pygame.display.set_mode((800, 600))
        self.on_keypress = lambda x: None
        self.on_keyrelease = lambda x: None
        self.last_pressed = pygame.key.get_pressed()
        self.gamefield = None

    def update(self):
        if self.gamefield is not None:
            self.gamefield.draw(self)
        pygame.display.flip()

    def run(self):
        while self.loop:
            for i in pygame.event.get():
                if i.type == pygame.KEYDOWN:
                    self.on_keypress(i.key)
                elif i.type == pygame.KEYUP:
                    self.on_keyrelease(i.key)