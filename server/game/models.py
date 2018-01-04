

class Object:
    def __init__(self, rect, field):
        self.rect = rect
        self.field = field
        self.collide = True
        self.id = '0'

        self.speed_x, self.speed_y = 0, 0
        self.moving = False

    def update(self):
        if not (self.speed_x or self.speed_y):
            return

        self.moving = True

        move_x = self.rect.move(self.speed_x, 0)
        if not self.check_collide(move_x):
            self.rect = move_x

        move_y = self.rect.move(0, self.speed_y)
        if not self.check_collide(move_y):
            self.rect = move_y

    def check_collide(self, rect):
        if self.field.rect.contains(rect) \
                or (rect.collidelist(list(filter(lambda x: x.collide, self.field.objects))) == -1):
            return False
        return True

    @staticmethod
    def canon_id(i):
        if type(i) == int:
            return str(i)
        if i.count(':') != -1:
            main_id, sub_id = i.split(':')
            if sub_id == 0:
                return main_id
        return i


class Entities(Object):
    def __init__(self, rect, field):
        super(Entities, self).__init__(rect, field)
        self.collide = False
        self.touchable = True


class Item(Entities):
    def __init__(self, rect, field):
        super(Item, self).__init__(rect, field)
        self.dropped = False
        self.name = None


class Weapon(Item):
    def __init__(self, rect, field):
        super(Weapon, self).__init__(rect, field)
        self.damage_value = 0

    def damage(self, npc):
        npc.hp -= self.damage_value


class Effect:
    def __init__(self, player):
        self.player = player
        self.id = '0'

    def update(self):
        pass


class NPC(Object):
    def __init__(self, rect, field, hp):
        super(NPC, self).__init__(rect, field)
        self.hp = hp
        self.effects = []

    def drop_item(self, item):
        if type(item) == list:
            for i in item:
                self.drop_item(i)
        else:
            item.dropped = True
            self.field.entities.append(item)
            item.rect.x, item.rect.y = self.rect.x, self.rect.y

    def update(self):
        super(NPC, self).update()
        for effect in self.effects:
            effect.update()
