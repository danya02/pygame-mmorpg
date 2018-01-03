from game.models import NPC
from game.config import *
from pygame import Rect


class Player(NPC):
    def __init__(self, x, y, hp, field, user):
        super(Player, self).__init__(Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT), field, '0', hp)
        self.name = user.user
        self.user = user

        self.speed_x = self.speed_y = 0
        self.direction = 0

    def action(self, act):
        if act == 'left':
            self.speed_x = -1
            self.direction = 2
        elif act == 'right':
            self.speed_x = 1
            self.direction = 0
        elif act == 'up':
            self.speed_y = -1
            self.direction = -1
        elif act == 'down':
            self.speed_y = 1
            self.direction = 1


class Field:
    def __init__(self):
        self.objects = []

        self.players = []
        self.npc = []
        self.entities = []

        self.width, self.height = FIELD_WIDTH, FIELD_HEIGHT
        self.rect = Rect(0, 0, self.width, self.height)

    def tick(self):
        for player in self.players:
            player.update()
        for npc in self.npc:
            npc.update()
        for entity in self.entities:
            entity.update()

    def add_player(self, x, y, hp, user):
        player = Player(x, y, hp, self, user)
        self.objects.append(player)
        self.players.append(player)


class Game:
    def __init__(self, channel):
        self.channel = channel
        self.field = Field()

    def add_player(self, user):
        self.field.add_player(user.player_info['x'], user.player_info['y'], user.player_info['hp'], user)
