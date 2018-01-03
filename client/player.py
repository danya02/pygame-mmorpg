#!/usr/bin/python3
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect()
        self.direction = 2
        self.sprites = [pygame.Surface((1, 1))] * 4

    def update(self, data):
        self.direction = 2
        center = self.rect.center
        self.image = self.sprites[self.direction]
        self.rect = self.image.get_rect()
        self.rect.center = center
