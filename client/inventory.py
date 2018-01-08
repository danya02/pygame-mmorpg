#!/usr/bin/python3
import pygame
import connection


class Inventory:
    def __init__(self):
        self.items = []
        self.rects = []
        for i in range(10):
            self.rects.append(pygame.Rect((150 + (50 * i), 550, 50, 50)))
        self.selected = 0

    def update(self):
        for i in self.items:
            i.inventory = self
        self.selected = min(len(self.items) - 1, self.selected)
        for i, j in zip(self.items, self.rects):
            i.rect.center = j.center

    def draw(self, surface):
        for i in self.rects:
            surface.fill(pygame.Color('black'), i)
        for i in self.rects:
            pygame.draw.rect(surface, pygame.Color('white'), i, 1)
        pygame.draw.rect(surface, pygame.Color('red'), self.rects[self.selected], 4)
        for i in self.items:
            surface.blit(i.image, i.rect)


class Item(pygame.sprite.Sprite):
    def __init__(self, item_id):
        super().__init__()
        self.id = item_id
        self.image = pygame.image.load('sprites/null_item.png')
        self.rect = self.image.get_rect()
        self.inventory = None
        self.get_image()

    def get_image(self):
        try:
            self.image = pygame.image.load('sprites/{}.png'.format(self.id))
        except pygame.error:
            connection.client.get_image(self.id+'.png', self.set_image)
            pass

    def set_image(self, data):
        self.image = pygame.image.fromstring(eval(data['src']), tuple(data['size']), "RGBA")
        self.rect = self.image.get_rect()
        self.inventory.update()


def get_item(item_id: str) -> Item:
    return Item(item_id)
