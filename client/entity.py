#!/usr/bin/python3
import traceback

import pygame
import math

import inventory
import connection
import effects


class Entity(pygame.sprite.Sprite):
    def __init__(self, field):
        """
        This class describes an Entity. An Entity is an object that has sprites, and can be moved by the server.
        """
        super().__init__()
        self.field = field
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
        self.can_walk = False
        self.walk_tick_delay = 1
        self.walk_tick_phase = 0
        self.standalone = False
        self.target = None

    def update_target(self):
        if self.target is not None:
            self.pan = (400 - self.target.original_center[0], 300 - self.target.original_center[1])
        self.update_image()

    def update(self, data=None, full: bool = False, field=None):
        """
        Update this with given data. If no data, update the sprite instead.
        :param data: data to find me in and to update from.
        :param full: is the update a full one?
        :return: my part of data, or None if there is no such.
        """
        if field is not None:
            self.field = field
        if data is None:
            self.update_image()
        elif 'target' in data and data['target'] is not self and data['target'] is not None and not self.standalone:
            self.target = data['target']
            self.update_target()
            return None
        else:
            if 'target' in data:
                self.update_target()
                return None
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
            if self.can_walk:
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
        if self.can_walk:
            if self.walking:
                self.walk_tick_phase += 1
            if self.walk_tick_phase >= self.walk_tick_delay:
                self.walk_tick_phase = 0
                self.walk_phase += 1
            if self.walk_phase >= len(self.sprites[self.direction]):
                self.walk_phase = 0
        target = self.rect.center
        if self.can_walk:
            self.original_image = self.sprites[self.direction][self.walk_phase]
        else:
            self.original_image = self.sprites[0]
        self.rect = self.original_image.get_rect()
        self.rect.center = target

    def update_walking(self) -> bool:
        """
        Am I walking?
        :return: if I am walking.
        """
        if self.can_walk:
            walk = False
            for i, j in enumerate([pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT]):
                if j in self.pressed_keys:
                    self.direction = i
                    walk = True
            self.walking = walk
            if not self.walking:
                self.walk_phase = 0
            return self.walking

    def get_image(self):
        try:
            self.image = pygame.image.load('sprites/{}.png'.format(self.id))
        except pygame.error:
            connection.client.get_image(self.id+'.png', self.set_image)
            pass

    def set_image(self, data):
        self.image = pygame.image.fromstring(eval(data['src']), tuple(data['size']), "RGBA")
        center = self.rect.center
        try:
            self.rect = self.original_image.get_rect()
        except AttributeError:
            self.rect = self.original_image[0].get_rect()
        self.rect.center = center

    def get_image(self):
        try:
            self.image = pygame.image.load('sprites/{}.png'.format(self.id))
        except pygame.error:
            connection.client.get_image(self.id+'.png', self.set_image)
            pass

    def set_image(self, data):
        self.image = pygame.image.fromstring(eval(data['src']), tuple(data['size']))
        self.rect = self.image.get_rect()


class NPC(Entity):
    def __init__(self, field):
        """
        This class describes an NPC. An NPC is an Entity that is a character not controlled by humans.
        """
        super().__init__(field)
        self.can_walk = True
        self.walk_tick_delay = 15
        zoom = lambda img, factor: pygame.transform.scale(img, (
            int(img.get_width() * factor), int(img.get_height() * factor)))
        self.sprites = [[zoom(pygame.image.load('sprites/spr_chara{}_{}.png'.format(j, str(i))), 2) for i in
                         range(2 if j in 'lr' else 4)] for j in 'urdl']


class Object(Entity):
    pass


class Projectile(Entity):
    pass


class Player(Entity):
    def __init__(self, field):
        """
        This class describes a Player. A Player is a character that a human controls.
        That includes the player at this computer.
        """
        super().__init__(field)
        self.can_walk = True
        self.hp = 100
        self.walk_tick_delay = 15
        zoom = lambda img, factor: pygame.transform.scale(img, (
            int(img.get_width() * factor), int(img.get_height() * factor)))
        self.sprites = [[zoom(pygame.image.load('sprites/spr_f_mainchara{}_{}.png'.format(j, str(i))), 2) for i in
                         range(2 if j in 'lr' else 4)] for j in 'urdl']
        self.transmit = False
        self.is_target = None

    def load(self, data: dict) -> None:
        """
        Initialize self with data from login process.
        :param data: the dict that was parsed from json.
        """
        try:
            self.original_center = data['player_info']['x'], data['player_info']['y']
            self.id = data['user_id']
            self.hp = data['player_info']['hp']
            self.direction = data['player_info']['direction']
            self.effects = [effects.get_effect(i) for i in data['player_info']['effects']]
            self.field.inventory.items = [inventory.get_item(i, self.field.inventory) for i in data['player_info']['inventory']]
        except:
            traceback.print_exc()

    def update(self, data=None, full=False, field=None):
        """
        Update this with given data. If no data, update the sprite instead.
        If I am a standalone Player, ignore data and move myself instead.
        :param data: data to find me in and to update from.
        :param full: is the update a full one?
        :param field: the GameField that this is a part of.
        :return: my part of data, or None if there is no such.
        """
        if field is not None:
            self.field = field
        super().update(data, full)
        if self.standalone:
            self.rect.center = (400, 300)
        self.update_image(False)
        if self.transmit and self.standalone:
            if pygame.K_UP in self.pressed_keys:
                connection.client.action('up')
            if pygame.K_DOWN in self.pressed_keys:
                connection.client.action('down')
            if pygame.K_LEFT in self.pressed_keys:
                connection.client.action('left')
            if pygame.K_RIGHT in self.pressed_keys:
                connection.client.action('right')

    def on_keypress(self, key) -> None:
        """
        Do this when the key is pressed.
        :param key: the key that was pressed's ID.
        """
        self.pressed_keys.append(key)
        if key in [eval('pygame.K_{}'.format(str(i))) for i in range(10)]:
            dict = eval('{' + ', '.join(['pygame.K_{}: {}'.format(str(i), str(i - 1)) for i in range(10)]) + '}')
            dict.update({pygame.K_0: 9})
            self.field.inventory.selected = dict[key]
            if self.transmit:
                connection.client.action('active_item_change', dict[key])
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
            y = abs(pos[1] - 300)
            dist = math.sqrt((400 - pos[0]) ** 2 + (300 - pos[1]) ** 2)
            cosa = y / dist
            angle = math.acos(cosa) * 180 / math.pi
            if self.transmit:
                connection.client.action('action', angle)
<<<<<<< HEAD
        elif button==1:
=======
        elif button == 1:
>>>>>>> 4391304502c1d672696e03ff136d683556e65a8b
            connection.client.action('hit')

    def on_unclick(self, pos, button):
        pass
