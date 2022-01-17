from game.common.hitbox import Hitbox
from game.common.moving.damaging.damaging_object import DamagingObject
from game.common.stats import GameStats
from game.common.enums import *


class Grenade(DamagingObject):
    def __init__(
            self,
            fuse_time=GameStats.grenade_stats['min_fuse_time'],
            range=None,
            damage=None,
            heading=None,
            speed=None,
            health=None,
            hitbox=Hitbox(5, 5, (250, 250), 0),
            collidable=False):
        super().__init__(range, damage, heading, speed, health, hitbox, collidable)
        self.fuse_time = fuse_time
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

    @DamagingObject.range.setter
    def range(self, val):
        if 0 <= val <= 200:
            self.range = val
        else:
            raise Exception("Tried to set a grenade distance greater than the max of 200")

    def to_json(self):
        data = super().to_json()
        data['fuse_time'] = self.fuse_time

        return data

    def from_json(self, data):
        super().from_json(data)
        self.fuse_time = data['fuse_time']
        return self
