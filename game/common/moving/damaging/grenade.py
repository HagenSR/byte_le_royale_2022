from game.common.moving.damaging.damaging_object import DamagingObject
from game.common.stats import GameStats
from game.common.enums import *


class Grenade(DamagingObject)
    def __init__(self, fuse_time = 0 range= None, damage= None, heading = None, speed = None, 
               health=None, coordinates=None, hitbox=None, collidable=None):
        super().__init__(range, damage, heading, speed, health, coordinates, hitbox, collidable)
        self.fuse_time = fuse_time
        
    @property    
    def fuse_time(self):
        return self._fuse_time
        
    @fuse_time.setter
    def fuse_time(self, val):
        if val >= fuse_time_min:
           self._fuse_time = val
        else:
            raise Exception("fuse time value outside bounds, Not set")