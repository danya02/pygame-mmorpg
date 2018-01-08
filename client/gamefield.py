#!/usr/bin/python3
import random
import pygame
import entity
import inventory


class GameField:
    def __init__(self):
        self.surface = pygame.Surface((1, 1))
        self.players = pygame.sprite.Group()
        self.entities = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()
        self.players.field = self
        self.entities.field = self
        self.npcs.field = self
        self.inventory = inventory.Inventory()
        self.target = None
        self.pan = (0, 0)
        self.send_message = lambda x: None

    def load(self, data):
        if data['bg']:
            self.surface = pygame.Surface((800, 600))  # TODO: generate from data
            for i in range(800):
                for j in range(600):
                    self.surface.set_at((i, j), pygame.Color(random.randint(0, 255), random.randint(0, 255),
                                                             random.randint(0, 255), 255))

    def update(self, data):
        self.players.update(data['players'], data.get('full', False), self)
        self.entities.update(data['entities'], data.get('full', False), self)
        self.npcs.update(data['npcs'], data.get('full', False), self)
        if len(data['players']) != 0:
            for i in data['players']:
                p = entity.Player(self)  # TODO: create from data
                p.id = i['id']
                p.standalone = False
                p.original_center = (i['x'], i['y'])
                p.update(data['players'], data.get('full', False), self)
                p.update({'target':self.target})
                self.players.add(p)
        if len(data['entities']) != 0:
            for i in data['entities']:
                p = entity.Entity(self)  # TODO: create from data
                p.id = i['id']
                p.original_center = (i['x'], i['y'])
                p.update(data['players'], data.get('full', False), self)
                p.update({'target':self.target})
                self.entities.add(p)
        if len(data['npcs']) != 0:
            for i in data['npcs']:
                p = entity.NPC(self)  # TODO: create from data
                p.id = i['id']
                p.original_center = (i['x'], i['y'])
                p.update(data['npcs'], data.get('full', False), self)
                p.update({'target':self.target})
                self.npcs.add(p)

    def draw(self, surface):
        if isinstance(self.target, entity.Entity):
            self.pan = (-self.target.original_center[0], -self.target.original_center[1])
        self.target.rect.center = (400, 300)
        surface.blit(self.surface, self.pan)
        self.players.update({'target': self.target})
        self.players.draw(surface)
        self.npcs.update({'target': self.target})
        self.npcs.draw(surface)
        self.entities.update({'target': self.target})
        self.entities.draw(surface)
        self.inventory.update()
        self.inventory.draw(surface)

    def send_from_player(self, data):
        self.send_message(data)
