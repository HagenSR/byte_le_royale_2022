from game.common.enums import Upgrades
from game.common.map_object import MapObject
from game.common.items import Item


class Upgrade(Item):
    
    def __init__ (self, coordinates, hitbox, health, count, upgrade_enum = None, movement_enum = None, sight_enum = None ):
        super().__init__(coordinates, hitbox, health, count)
        self.upgrade_enum = upgrade_enum
        self.movement_enum = movement_enum
        self.sight_enum = sight_enum
        
    def to_json(self):
        data = super().to_json()
        data[upgrade_enum] = self.upgrade_enum
        data[movement_enum] = self.movement_enum
        data[sight_enum] = self.sight_enum
        return data
    
    def from_json(self, data):
        super.from_json(data)
        self.upgrade_enum = data[upgrade_enum]
        self.movement_enum = data[movement_enum]
        self.sight_enum = data[sight_enum]
        
        