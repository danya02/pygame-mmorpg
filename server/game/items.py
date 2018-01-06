from .models import *
from .effects import *
from .entities import *


class Sword(Weapon):
    id = '50'

    def __init__(self, field):
        super(Sword, self).__init__(field)

        self.damage_value = 10


class UltimateSword(Sword):
    id = '50:1'

    def __init__(self, field):
        super(UltimateSword, self).__init__(field)

        self.damage_value = 50


class PoisonSword(Sword):
    id = '50:2'

    def __init__(self, field):
        super(PoisonSword, self).__init__(field)

        self.damage_value = 20

    def damage(self, npc):
        super(PoisonSword, self).damage(npc)
        self.field.add_effect(PoisonEffect(npc, 5))


class HealingSword(Sword):
    id = '50:3'

    def __init__(self, field):
        super(HealingSword, self).__init__(field)

        self.damage_value = -1
        self.action_delay = 5

    def damage(self, npc):
        super(HealingSword, self).damage(npc)
        self.field.add_effect(HealingEffect(npc, 5))

    def action(self, player):
        super(HealingSword, self).action(player)
        player.hp += 1


class FireStaff(Weapon):
    id = '51'

    def __init__(self, field):
        super(FireStaff, self).__init__(field)

        self.damage_value = 5

    def action(self, player):
        super(FireStaff, self).action(player)
        self.field.spawn_entity(FireBall(self.field, self.rect), player.rect.x, player.rect.y, player.speed_x)  # TODO: Speed
