#!/usr/bin/python3
import pygame


class Inventory:
    def __init__(self):
        self.items = []
        self.rects = []
        for i in range(10):
            self.rects.append(pygame.Rect((150 + (50 * i), 550, 50, 50)))
        self.selected = 0

    def update(self):
        self.selected = min(len(self.items)-1, self.selected)
        for i, j in zip(self.items, self.rects):
            i.rect = j

    def draw(self, surface):
        for i in self.rects:
            surface.fill(pygame.Color('black'), i)
        for i in self.rects:
            pygame.draw.rect(surface, pygame.Color('white'), i, 1)
        pygame.draw.rect(surface, pygame.Color('red'), self.rects[self.selected], 4)
        for i in self.items:
            surface.blit(i.image, i.rect)


class Item(pygame.sprite.Sprite):
    pass
