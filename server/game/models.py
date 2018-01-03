

class Object:
    def __init__(self, rect, field, obj_id):
        self.rect = rect
        self.field = field
        self.collide = True

        if obj_id.count(':') > 0:
            ent_id, sub_id = list(map(int, obj_id.split()))
            self.id = ent_id
            self.sub_id = sub_id
        else:
            self.id = obj_id

        self.speed_x, self.speed_y = 0, 0

    def update(self):
        if not (self.speed_x or self.speed_y):
            return

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


class Entities(Object):
    def __init__(self, rect, ent_id, field):
        super(Entities, self).__init__(rect, field, ent_id)


class NPC(Object):
    def __init__(self, rect, field, npc_id, hp):
        super(NPC, self).__init__(rect, field, npc_id)
        self.hp = hp
