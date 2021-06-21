from game.common.enums import ObjectType
from game.common.map_object import MapObject
from game.common.stats import GameStats


class Wall(MapObject):
    def __init__(self, coordinates, hitbox, health = GameStats.default_wall_health, destructible = False, collidable = True):
        super().__init__(health, coordinates, hitbox, collidable )
        self.object_type = ObjectType.wall
        self.destructible = destructible
        
    def to_json(self):
        data = super().to_json()
        data['destructible'] = self.destructible
        return data
    
    def from_json(self, data):
        super().from_json(data)
        self.destructible = data['destructible']