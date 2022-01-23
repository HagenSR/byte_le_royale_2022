from game.common.hitbox import Hitbox
from game.common.moving.damaging.damaging_object import DamagingObject
from game.common.stats import GameStats
from game.common.enums import *
from game.common.items.consumable import Consumable


class Grenade(Consumable):
    def __init__(
            self, hitbox, health, fuse_time, damage):
        super().__init__(hitbox, health, consumable_enum=Consumables.grenade)
        self.fuse_time = fuse_time
        self.damage = damage
        self.object_type = ObjectType.grenade

    @property
    def fuse_time(self):
        return self.__fuse_time

    @fuse_time.setter
    def fuse_time(self, val):
        self.__fuse_time = val

    def to_json(self):
        data = super().to_json()
        data['fuse_time'] = self.fuse_time
        data['damage'] = self.damage

        return data

    def from_json(self, data):
        super().from_json(data)
        self.fuse_time = data['fuse_time']
        self.damage = data['damage']
        return self
