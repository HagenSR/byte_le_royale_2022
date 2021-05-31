
from game.common.moving.moving_object import MovingObject
from game.common.stats import GameStats
from game.common.enums import *



class DamagingObject(MovingObject):
    def __init__(self, range=0, damage=0, heading = None, speed = None, 
               health=None, coordinates=None, hitbox=None, collidable=None):
        super().__init__(heading, speed, health, coordinates, hitbox, collidable)
        self.range = range
        self.damage = damage
        self.object_type = ObjectType.damaging_object
        
    @property
    def range(self):
        return self.range

    @range.setter
    def range(self, value):
        if value >= 0 and value <= GameStats.damaging_object_stats['max_range']:
            self.range = value
            
    @property
    def damage(self):
        return self.damage
    
    @damage.setter
    def damage(self, value):
         if value >= 0 and value <= GameStats.damaging_object_stats['max_damage']:
            self.damage = value

    
    def to_json(self):
        data = super().to_json()
        data['range'] = self.range
        data['damage'] = self.damage

        return data
 
    def from_json(self, data):
        super().from_json(data)
        self.range = data['range']
        self.damage = data['damage']
   