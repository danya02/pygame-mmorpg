from .models import Entity
from .effects import *


class Ball(Entity):
    id = '150'
    speed = 5

    def __init__(self, field, rect, owner):
        super(Ball, self).__init__(field, rect)

        self.damage_value = 20
        self.effect = None
        self.owner = owner

    def collide_action(self, lst):
        target = lst[0]
        if (target.type == 'npc') and (target != self.owner):
            target.hp -= self.damage_value
            if self.effect:
                self.field.add_effect(FireEffect(target, 5))


class FireBall(Ball):
    id = '150:1'

    def __init__(self, field, rect, owner):
        super(FireBall, self).__init__(field, rect, owner)
