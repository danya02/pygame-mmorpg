from .models import Entity
from .effects import *


class Ball(Entity):
    id = '150'

    def __init__(self, field, rect):
        super(Ball, self).__init__(field, rect)

        self.damage_value = 20
        self.effect = None

        self.speed = 5

    def action(self, lst):
        target = lst[0]
        if target.type == 'npc':
            target.hp -= self.damage_value
            if self.effect:
                self.field.add_effect(FireEffect(target, 5))


class FireBall(Ball):
    id = '150:1'

    def __init__(self, field, rect):
        super(FireBall, self).__init__(field, rect)
