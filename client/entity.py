#!/usr/bin/python3
import pygame
import math
import main
import effects


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        """
        This class describes an Entity. An Entity is an object that has sprites, and can be moved by the server.
        """
        super().__init__()
        self.id = None
        self.image = pygame.Surface((1, 1))
        self.original_image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect()
        self.original_center = (0, 0)
        self.pan = (0, 0)
        self.direction = 2
        self.walk_phase = 0
        self.sprites = [[pygame.Surface((1, 1))]] * 4
        self.pressed_keys = []
        self.effects = [effects.Effect(self)]
        self.walking = False
        self.walk_tick_delay = 1
        self.walk_tick_phase = 0
        self.standalone = False

    def update(self, data=None, full: bool = False):
        """
        Update this with given data. If no data, update the sprite instead.
        :param data: data to find me in and to update from.
        :param full: is the update a full one?
        :return: my part of data, or None if there is no such.
        """
        if data is None:
            self.update_image()
        elif 'target' in data and data['target'] is not self and data['target'] is not None:
            self.pan = (self.original_center[0]-data['target'].original_center[0], self.original_center[1]-data['target'].original_center[1])
            self.update_image()
        else:
            for i in data:
                if i['id'] == self.id:
                    mydata = data.pop(data.index(i))
                    break
            else:
                self.kill()
                return None
            deltax = mydata['x'] - self.original_center[0]
            deltay = mydata['y'] - self.original_center[1]
            if deltax > 0:
                self.direction = 1
            if deltax < 0:
                self.direction = 3
            if deltay > 0:
                self.direction = 2
            if deltay < 0:
                self.direction = 0
            self.walking = abs(deltax) + abs(deltay) > 0
            self.original_center = mydata['x'], mydata['y']
            return mydata

    def update_image(self, target=True):
        for i in self.effects:
            i.target = self
            if not i.running:
                i.start()
        if target:
            self.rect.centerx = self.original_center[0] + self.pan[0]
            self.rect.centery = self.original_center[1] + self.pan[1]
        if self.walking:
            self.walk_tick_phase += 1
        if self.walk_tick_phase >= self.walk_tick_delay:
            self.walk_tick_phase = 0
            self.walk_phase += 1
        if self.walk_phase >= len(self.sprites[self.direction]):
            self.walk_phase = 0
        target = self.rect.center
        self.original_image = self.sprites[self.direction][self.walk_phase]
        self.rect = self.image.get_rect()
        self.rect.center = target

    def update_walking(self) -> bool:
        """
        Am I walking?
        :return: if I am walking.
        """
        walk = False
        for i, j in enumerate([pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT]):
            if j in self.pressed_keys:
                self.direction = i
                walk = True
        self.walking = walk
        if not self.walking:
            self.walk_phase = 0
        return self.walking


class NPC(Entity):
    def __init__(self):
        """
        This class describes an NPC. An NPC is an Entity that is a character not controlled by humans.
        """
        super().__init__()
        self.walk_tick_delay = 150
        zoom = lambda img, factor: pygame.transform.scale(img, (
            int(img.get_width() * factor), int(img.get_height() * factor)))
        self.sprites = [[zoom(pygame.image.load('sprites/spr_chara{}_{}.png'.format(j, str(i))), 2) for i in
                         range(2 if j in 'lr' else 4)] for j in 'urdl']


class Object(Entity):
    pass


class Projectile(Entity):
    pass


class Player(Entity):
    def __init__(self):
        """
        This class describes a Player. A Player is a character that a human controls.
        That includes the player at this computer.
        """
        super().__init__()
        self.hp = 100
        self.walk_tick_delay = 150
        zoom = lambda img, factor: pygame.transform.scale(img, (
            int(img.get_width() * factor), int(img.get_height() * factor)))
        self.sprites = [[zoom(pygame.image.load('sprites/spr_f_mainchara{}_{}.png'.format(j, str(i))), 2) for i in
                         range(2 if j in 'lr' else 4)] for j in 'urdl']
        self.transmit = False

    def load(self, data):
        self.original_center = data['player_info']['x'], data['player_info']['y']
        self.id = data['user_id']
        self.hp = data['player_info']['hp']
        self.direction = data['player_info']['direction']
        self.effects = [effects.get_effect(i) for i in ['player_info']['effects']]



    def update(self, data=None, full=False):
        """
        Update this with given data. If no data, update the sprite instead.
        If I am a standalone Player, ignore data and move myself instead.
        :param data: data to find me in and to update from.
        :param full: is the update a full one?
        :return: my part of data, or None if there is no such.
        """
        if not self.standalone:
            super().update(data, full)
        else:
            if pygame.K_UP in self.pressed_keys:
                self.original_center = (self.original_center[0], self.original_center[1] - 1)
            if pygame.K_DOWN in self.pressed_keys:
                self.original_center = (self.original_center[0], self.original_center[1] + 1)
            if pygame.K_LEFT in self.pressed_keys:
                self.original_center = (self.original_center[0] - 1, self.original_center[1])
            if pygame.K_RIGHT in self.pressed_keys:
                self.original_center = (self.original_center[0] + 1, self.original_center[1])
            self.rect.center = (400, 300)
            self.update_image(False)
        if self.transmit:
            if pygame.K_UP in self.pressed_keys:
                main.client.action(action_type='up')
            if pygame.K_DOWN in self.pressed_keys:
                main.client.action(action_type='down')
            if pygame.K_LEFT in self.pressed_keys:
                main.client.action(action_type='left')
            if pygame.K_RIGHT in self.pressed_keys:
                main.client.action(action_type='right')

    def on_keypress(self, key) -> None:
        """
        Do this when the key is pressed.
        :param key: the key that was pressed's ID.
        """
        self.pressed_keys.append(key)
        self.update_walking()

    def on_keyrelease(self, key) -> None:
        """
        Do this when the key is released.
        :param key: the key that was released's ID.
        """
        try:
            while 1:
                self.pressed_keys.remove(key)
        except ValueError:
            pass
        self.update_walking()

    def on_click(self, pos, button):
        if button == 3:
            y = abs(pos[1]-300)
            dist = math.sqrt((400-pos[0])**2+(300-pos[1])**2)
            cosa = y/dist
            angle = math.acos(cosa) * 180 / math.pi
            if self.transmit:
                main.client.action('action', angle)

    def on_unclick(self, pos, button):
        pass