#!/usr/bin/python3
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.Surface((1,1))
        self.rect = self.image.get_rect()