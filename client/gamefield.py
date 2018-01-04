#!/usr/bin/python3
import pygame


class GameField:
    def __init__(self):
        self.surface = pygame.Surface((1, 1))
        self.players = pygame.sprite.Group()
        self.entities = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()
        self.send_message = lambda x: None

    def load(self, data):
        pass  # TODO: create players, bg, &c.

    def update(self, data):
        self.players.update(data['players'])
        self.entities.update(data['entities'])
        self.npcs.update(data['npcs'])
        if len(data['players']) != 0:
            pass  # TODO: create classes.
        if len(data['entities']) != 0:
            pass  # TODO: create classes.
        if len(data['npcs']) != 0:
            pass  # TODO: create classes.

    def draw(self, surface):
        surface.blit(self.surface, (0, 0))
        self.players.draw(surface)

    def send_from_player(self, data):
        self.send_message(data)
