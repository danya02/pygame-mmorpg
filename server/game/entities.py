from game.models import Entities


class FireBall(Entities):
    def __init__(self, field, rect):
        super(FireBall, self).__init__(field, rect)