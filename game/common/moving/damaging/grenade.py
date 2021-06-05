from game.common.moving.damaging.damaging_object import DamagingObject
from game.common.stats import GameStats
from game.common.enums import *


class Grenade(DamagingObject):
    def __init__(self, fuse_time = GameStats.grenade_stats['min_fuse_time'], range= None, damage= None, 
        heading = None, speed = None, health=None, coordinates=None, hitbox=None, collidable=None):
        super().__init__(range, damage, heading, speed, health, coordinates, hitbox, collidable)
        self.__fuse_time = fuse_time
        self.object_type = ObjectType.grenade
        
    @property    
    def fuse_time(self):
        return self.__fuse_time
        
    @fuse_time.setter
    def fuse_time(self, val):
        if val >= GameStats.grenade_stats['min_fuse_time'] and val <= GameStats.grenade_stats['max_fuse_time']:
           self.__fuse_time = val
        else:
            raise Exception("fuse time value outside bounds, Not set")
    
  
    def to_json(self):
        data = super().to_json()
        data['fuse_time'] = self.fuse_time

        return data

    def from_json(self, data):
        super().from_json(data)
        self.fuse_time = data['fuse_time']
