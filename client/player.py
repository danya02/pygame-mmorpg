#!/usr/bin/python3
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.id = None
        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect()
        self.direction = 2
        self.walk_phase = 0
        self.sprites = [[pygame.image.load('sprites/spr_f_mainchara{}_{}.png'.format(j, str(i))) for i in
                         range(2 if j in 'lr' else 4)] for j in 'urdl']
        self.pressed_keys = []
        self.walking = False
        self.standalone = False

    def update(self, data = None):
        if not self.standalone:
            if data is None:
                self.update_image()
            else:
                mydata = None
                for i in data:
                    if i['id'] == self.id:
                        mydata = data.pop(data.index(i))
                        break
                self.rect.centerx = mydata['x']
                self.rect.centery = mydata['y']
                return mydata
        else:
            if pygame.K_UP in self.pressed_keys:
                self.rect.centery-=1
            if pygame.K_DOWN in self.pressed_keys:
                self.rect.centery+=1
            if pygame.K_LEFT in self.pressed_keys:
                self.rect.centerx-=1
            if pygame.K_RIGHT in self.pressed_keys:
                self.rect.centerx+=1
            self.update_image()


    def update_image(self):
        if self.walking:
            self.walk_phase += 1
        if self.walk_phase >= len(self.sprites[self.direction]):
            self.walk_phase = 0
        center = self.rect.center
        self.image = self.sprites[self.direction][self.walk_phase]
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update_walking(self):
        walk = False
        for i, j in enumerate([pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT]):
            if j in self.pressed_keys:
                self.direction = i
                walk = True
        self.walking = walk
        if not self.walking:
            self.walk_phase = 0

    def on_keypress(self, key):
        self.pressed_keys.append(key)
        self.update_walking()

    def on_keyrelease(self, key):
        try:
            while 1:
                self.pressed_keys.remove(key)
        except ValueError:
            pass
        self.update_walking()
