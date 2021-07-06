
from game.common.moving.moving_object import MovingObject
from game.common.stats import GameStats
from game.common.enums import *


class DamagingObject(MovingObject):
    def __init__(self, range=0, damage=0, heading=None, speed=None,
                 health=None, hitbox=None, collidable=None):
        super().__init__(heading, speed, health, hitbox, collidable)
        self.range = range
        self.damage = damage
        self.object_type = ObjectType.damaging_object

    @property
    def range(self):
        return self.__range

    @range.setter
    def range(self, value):
        if value >= 0 and value <= GameStats.damaging_object_stats['max_range']:
            self.__range = value
        else:
            raise Exception("Range value outside bounds, Not set")

    @property
    def damage(self):
        return self.__damage

    @damage.setter
    def damage(self, value):
        if value >= 0 and value <= GameStats.damaging_object_stats['max_damage']:
            self.__damage = value
        else:
            raise Exception("Damage value outside bounds, Not set")

    def to_json(self):
        data = super().to_json()
        data['range'] = self.range
        data['damage'] = self.damage

        return data

    def from_json(self, data):
        super().from_json(data)
        self.range = data['range']
        self.damage = data['damage']
