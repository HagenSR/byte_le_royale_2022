from game.common.map_object import MapObject
from game.common.enums import ObjectType


class Teleporter(MapObject):

    def __init__(self, hitbox=None, cooldown=20, health=10):
        super().__init__(health=health, hitbox=hitbox, collidable=False)
        # cooldown is in terms of seconds
        self.cooldown = cooldown
        self.object_type = ObjectType.teleporter

    def to_json(self):
        data = super().to_json()
        data['cooldown'] = self.cooldown
        return data

    def from_json(self, data):
        super().from_json(data)
        self.cooldown = data['cooldown']
        return self
