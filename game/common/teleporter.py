from game.common.map_object import MapObject
from game.common.enums import ObjectType


class Teleporter(MapObject):

    def __init__(self, hitbox=None, turn_cooldown=5, health=10):
        super().__init__(health=health, hitbox=hitbox, collidable=False)
        self.turn_cooldown = turn_cooldown
        self.usable = True
        self.object_type = ObjectType.teleporter

    def to_json(self):
        data = super().to_json()
        data['turn_cooldown'] = self.turn_cooldown
        data['usable'] = self.usable
        return data

    def from_json(self, data):
        super().from_json(data)
        self.turn_cooldown = data['turn_cooldown']
        self.usable = data['usable']
        return self
