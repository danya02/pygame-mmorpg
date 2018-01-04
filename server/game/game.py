from game.models import *
from game.config import *
from game.effects import *
from game.items import *
from game.entities import *
import pygame
from pygame import Rect


class Player(NPC):
    def __init__(self, x, y, hp, field, user):
        super(Player, self).__init__(Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT), field, hp)
        self.name = user.user
        self.user = user
        self.inventory = []

        self.speed_x = self.speed_y = 0
        self.direction = 0

    def action(self, act):
        if act == 'left':
            self.speed_x = -1
            self.direction = 3
        elif act == 'right':
            self.speed_x = 1
            self.direction = 1
        elif act == 'up':
            self.speed_y = -1
            self.direction = 0
        elif act == 'down':
            self.speed_y = 1
            self.direction = 2

    def drop_item(self, item):
        """
        :param item: id or class
        :return: None
        """
        if type(item) == str:
            item = self.canon_id(item)
            for i in self.inventory:
                if i.id == item:
                    break
            else:
                return
            self.drop_item(i)
            return
        super(Player, self).drop_item(item)
        self.inventory.remove(item)

    def get_item(self, item):
        if type(item) == str:
            item = self.canon_id(item)
            for entity in self.field.entities:
                if entity.id == item:
                    break
            else:
                return
            self.get_item(entity)
            return
        self.inventory.append(item)
        self.field.entities.remove(item)
        item.dropped = False


class Field:
    def __init__(self):
        self.objects = []

        self.players = []
        self.npc = []
        self.entities = []

        self.tick = 0

        self.width, self.height = FIELD_WIDTH, FIELD_HEIGHT
        self.rect = Rect(0, 0, self.width, self.height)

    def do_tick(self):
        for player in self.players:
            player.update()
        for npc in self.npc:
            npc.update()
        for entity in self.entities:
            entity.update()
        self.tick += 1

    def add_player(self, x, y, hp, user):
        player = Player(x, y, hp, self, user)
        self.players.append(player)

    # TODO: add_entity

    @staticmethod
    def add_effect(effect):
        npc = effect.npc
        for eff in npc.effects:
            if eff.id == effect.id:
                npc.effects.remove(eff)
        npc.effects.append(effect)


class Game:
    def __init__(self, channel):
        self.channel = channel
        self.field = Field()

    def add_player(self, user):
        self.field.add_player(user.player_info['x'], user.player_info['y'], user.player_info['hp'], user)

    @staticmethod
    def get_img(img):
        return {
                'src': str(pygame.image.tostring(img, 'RGBA')),
                'size': img.get_size()
        }
