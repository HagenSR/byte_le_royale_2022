from game.common.items.item import Item
from game.common.enums import Consumables, ObjectType


class Consumable(Item):
    def __init__(self, hitbox, health, count, speed_enum = None, health_enum = None, armor_enum = None):
        super().__init__(hitbox, health, count)
        self.object_type = ObjectType.consumable
        self.speed_enum = speed_enum
        self.health_enum = health_enum
        self.armor_enum = armor_enum
        
    def to_json(self):
        data = super().to_json()
        data['speed_enum'] = self.speed_enum
        data['health_enum'] = self.health_enum
        data['armor_enum'] = self.armor_enum
        
    def from_json(self, data):
        super().from_json(data)
        self.speed_enum = data['speed_enum']
        self.health_enum = data['health_enum']
        self.armor_enum = data['armor_enum']