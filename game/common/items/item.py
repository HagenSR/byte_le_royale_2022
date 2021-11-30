from game.common.map_object import MapObject
from game.common.enums import ObjectType


class Item(MapObject):
<<<<<<< HEAD

    def __init__(self, hitbox, health=None, count=1):
        super().__init__(health, hitbox, False) # note
=======
    def __init__(self, hitbox=None, health=None):
        super().__init__(health, hitbox, True)
>>>>>>> d0ac613effa0cfa06cbda2c9a0c78285284b417d
        self.object_type = ObjectType.item

    def to_json(self):
        data = super().to_json()
        return data

    def from_json(self, data):
        super().from_json(data)
        return self
