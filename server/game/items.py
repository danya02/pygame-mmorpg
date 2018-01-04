from game.models import Weapon
from pygame import Rect


class Sword(Weapon):
    def __init__(self, field):
        self.width = 10
        self.height = 15
        super(Sword, self).__init__(Rect(0, 0, self.width, self.height), field)

        self.damage_value = 10
        self.id = '50'


class UltimateSword(Sword):
    def __init__(self, field):
        super(UltimateSword, self).__init__(field)

        self.damage_value = 50
        self.id = '50:1'


class PoisonSword(Sword):
    def __init__(self, field):
        super(PoisonSword, self).__init__(field)

        self.damage_value = 20
        self.id = '50:2'

    def damage(self, npc):
        super(PoisonSword, self).damage(npc)
