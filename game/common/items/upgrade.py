from game.common.enums import ObjectType, Upgrades
from game.common.map_object import MapObject
from game.common.items.item import Item


class Upgrade(Item):

    def __init__(
            self,
            hitbox,
            health,
            upgrade_enum=None,
            movement_enum=None,
            sight_enum=None):
        super().__init__(hitbox, health)
        self.object_type = ObjectType.upgrade
        self.upgrade_enum = upgrade_enum
        self.movement_enum = movement_enum
        self.sight_enum = sight_enum

    def to_json(self):
        data = super().to_json()
        data['upgrade_enum'] = self.upgrade_enum
        data['movement_enum'] = self.movement_enum
        data['sight_enum'] = self.sight_enum
        return data

    def from_json(self, data):
        super().from_json(data)
        self.upgrade_enum = data['upgrade_enum']
        self.movement_enum = data['movement_enum']
        self.sight_enum = data['sight_enum']
        return self
