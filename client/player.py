#!/usr/bin/python3
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((1,1))
        self.rect = self.image.get_rect()