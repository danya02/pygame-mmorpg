from pygame import Rect


class Object:
    id = '0'
    type = 'object'

    def __init__(self, rect, field):
        self.rect = rect
        self.field = field
        self.collide = True

        self.direction = 0
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
        objects = self.field.objects + self.field.players + self.field.npc + self.field.entities
        objects.remove(self)
        if self.field.rect.contains(rect) \
                and((rect.collidelist((list(map(lambda x: x.rect,
                                                filter(lambda x: x.collide, objects)))))) or not self.collide):
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


class Entity(Object):
    id = '150'
    type = 'entity'

    def __init__(self, rect, field):
        super(Entity, self).__init__(rect, field)
        self.collide = False
        self.touchable = True

    def update(self):
        super(Entity, self).update()
        if self.touchable:
            objects = self.field.objects + self.field.players + self.field.npc + self.field.entities
            objects.remove(self)
            self.action([objects[i] for i in self.rect.collidelistall(list(map(lambda x: x.rect,
                                                                               filter(lambda x: x.collide, objects))))])

    def action(self, *_):
        pass


class Item(Entity):
    id = '50'
    type = 'item'

    def __init__(self, rect, field):
        super(Item, self).__init__(rect, field)
        self.dropped = False
        self.name = None

        self.action_delay = 15
        self.last_action_tick = 0

    def action(self, player):
        if self.field.tick - self.last_action_tick < self.action_delay:
            return
        self.last_action_tick = self.field.tick

        # Override your action


class Weapon(Item):
    def __init__(self, field):
        self.width = 10
        self.height = 15

        super(Weapon, self).__init__(Rect(0, 0, self.width, self.height), field)
        self.damage_value = 0
        self.damage_radius = 20

    def damage(self, npc):
        npc.hp -= self.damage_value


class Effect:
    id = '100'
    type = 'effect'

    def __init__(self, npc, ticks, delay):
        self.npc = npc
        self.ticks = ticks
        self.delay = delay

    def update(self):
        if self.ticks == 0:
            self.npc.effects.remove(self)
            return
        if not self.ticks % self.delay:
            self.action()
        self.ticks -= 1

    def action(self):
        pass


class NPC(Object):
    type = 'NPC'

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
