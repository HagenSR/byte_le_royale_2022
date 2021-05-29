
from game.common.moving.moving_object import MovingObject
from game.common.stats import GameStats
from game.common.enums import *



class DamagingObject(MovingObject):
    def _init_(self, range=0, damage=0, heading = None, speed = None, 
               health=None, coordinates=None, hitbox=None, collidable=None):
        super().__init__(heading, speed, health, coordinates, hitbox, collidable)
        self.__range = range
        self.__damage = damage
        
    def get_range(self):
        return self.__range
        
    def get_damage(self):
        return self.__damage
        
    def set_range(self, val):
        if val >= 0 and val <= GameStats.damaging_object_stats['max_range']:
            self.__range = val
    
    def set_damage(self, val):
         if val>= 0 and val <= GameStats.damaging_object_stats['max_damage']:
            self.__damage = val

    
    def to_json(self):
        data = super().to_json()
        data['range'] = self.range
        data['damage'] = self.damage

        return data
 
    def from_json(self, data):
        super().from_json(data)
        self.range = data['range']
        self.damage = data['damage']
   