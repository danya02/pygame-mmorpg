from game.config import *
import game.items
import game.entities
import game.objects
import game.effects
import game.models

import threading
import time
import pygame
from pygame import Rect


class Player(game.models.NPC):
    def __init__(self, x, y, hp, inventory, active_item, direction, field, user):
        super(Player, self).__init__(Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT), field, hp)
        self.name = user.user
        self.id = user.user_id
        self.user = user
        self.inventory = inventory
        self.active_item = active_item

        self.speed_x = self.speed_y = 0
        self.direction = direction

    def action(self, act, data):
        if act == 'left':
            self.speed_x = -PLAYER_SPEED
            self.direction = 3
        elif act == 'right':
            self.speed_x = PLAYER_SPEED
            self.direction = 1
        elif act == 'up':
            self.speed_y = -PLAYER_SPEED
            self.direction = 0
        elif act == 'down':
            self.speed_y = PLAYER_SPEED
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

    def update(self):
        super(Player, self).update()
        self.speed_x = 0
        self.speed_y = 0


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

    def add_player(self, x, y, hp, inventory, active_item, direction, user):
        player = Player(x, y, hp, inventory, direction, active_item, self, user)
        self.players.append(player)
        return player

    def spawn_entity(self, entity, x, y, speed_x, speed_y):
        entity.rect.x = x
        entity.rect.y = y
        entity.speed_x = speed_x,
        entity.speed_y = speed_y
        self.entities.append(entity)

    @staticmethod
    def add_effect(effect):
        npc = effect.npc
        for eff in npc.effects:
            if eff.id == effect.id:
                npc.effects.remove(eff)
        npc.effects.append(effect)

    @staticmethod
    def get_attr(obj, attr='id'):
        try:
            return getattr(obj, attr)
        except AttributeError:
            return False

    def get_object_by_id(self, item_id):
        if type(item_id) == list:
            return [self.get_object_by_id(i) for i in item_id]
        all_objects = list(filter(lambda x: self.get_attr(x),
                                  map(lambda x: getattr(game.objects, x), dir(game.objects))))
        ids = list(map(lambda x: x.id, all_objects))
        return all_objects[ids.index(item_id)]


class Game(threading.Thread):
    def __init__(self, channel):
        threading.Thread.__init__(self, target=self.run)
        self.channel = channel
        self.field = Field()

    def add_player(self, user):
        inventory = self.field.get_object_by_id(user.player_info['inventory'])
        active_item = self.field.get_object_by_id(user.player_info['active_item'])
        return self.field.add_player(user.player_info['x'], user.player_info['y'],
                                     user.player_info['hp'], inventory,
                                     active_item, user.player_info['direction'], user)

    def delete_player(self, user):
        self.field.players.remove(user.me)
        self.channel.send({'type': 'player_left', 'data': ''})

    @staticmethod
    def get_img(img):
        return {
                'src': str(pygame.image.tostring(img, 'RGBA')),
                'size': img.get_size()
        }

    def run(self):
        while True:
            self.field.do_tick()
            data = {
                'players': [
                    {
                        'x': player.rect.x,
                        'y': player.rect.y,
                        'hp': player.hp,
                        'user_info': player.user.get_information(),
                        'effects': [
                            {
                                'id': effect.id,
                                'ticks': effect.ticks
                            } for effect in player.effects
                        ]
                    } for player in self.field.players
                ],
                'objects': [
                    {
                        'x': obj.rect.x,
                        'y': obj.rect.y,
                        'id': obj.id
                    } for obj in self.field.objects
                ],
                'entities': [
                    {
                        'x': entity.rect.x,
                        'y': entity.rect.y,
                        'id': entity.id
                    } for entity in self.field.entities
                ],
                'npcs': [
                    {
                        'x': npc.rect.x,
                        'y': npc.rect.y,
                        'hp': npc.hp,
                        'effects': [
                            {
                                'id': effect.id,
                                'ticks': effect.ticks
                            } for effect in npc.effects
                        ]
                    } for npc in self.field.npc
                ]
            }
            self.channel.send({'type': 'tick', 'data': data})
            time.sleep(TICK)
