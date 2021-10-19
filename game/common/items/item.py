from game.common.map_object import MapObject
from game.common.enums import ObjectType


class Item(MapObject):
    def __init__(self, hitbox, health=None, count=1):
        super().__init__(health, hitbox, False)
        self.object_type = ObjectType.item
        self.count = count

    def to_json(self):
        data = super().to_json()
        data['count'] = self.count
        return data

    def from_json(self, data):
        super().from_json(data)
        self.count = data['count']
        return self
