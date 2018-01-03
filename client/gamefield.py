#!/usr/bin/python3
import pygame


class GameField:
    def __init__(self):
        self.surface = pygame.Surface((1, 1))
        self.players = pygame.sprite.Group()

    def update(self, data):
        self.players.update(data)

    def draw(self, surface):
        surface.blit(self.surface, (0, 0))
        self.players.draw(surface)
