from game.common.items.item import Item
from game.common.enums import ObjectType


class Consumable(Item):
    def __init__(
            self,
            hitbox=None,
            health=None,
            consumable_enum=None):
        super().__init__(hitbox, health)
        self.object_type = ObjectType.consumable
        self.consumable_type = consumable_enum

    def to_json(self):
        data = super().to_json()
        data['consumable_type'] = self.consumable_type

    def from_json(self, data):
        super().from_json(data)
        self.consumable_type = data['consumable_type']
        return self
