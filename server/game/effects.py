from game.models import Effect


class PoisonEffect(Effect):
    def __init__(self, player):
        super(PoisonEffect, self).__init__(player)
