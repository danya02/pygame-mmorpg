from game.models import Effect


class PoisonEffect(Effect):
    id = '100'

    def __init__(self, player, ticks, delay=1):
        super(PoisonEffect, self).__init__(player, ticks, delay)

        self.damage_value = 1

    def action(self):
        self.player.hp -= self.damage_value


class ExtraPoisonEffect(PoisonEffect):
    id = '100:1'

    def __init__(self, player, ticks, delay=1):
        super(ExtraPoisonEffect, self).__init__(player, ticks, delay)

        self.damage_value = 5


class HealingEffect(Effect):
    id = '101'

    def __init__(self, player, ticks, delay=1):
        super(HealingEffect, self).__init__(player, ticks, delay)

        self.healing_value = 1

    def action(self):
        self.player.hp += self.healing_value
