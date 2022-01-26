from game.common.hitbox import Hitbox
from game.common.moving.damaging.damaging_object import DamagingObject
from game.common.stats import GameStats
from game.common.enums import *


class Bullet(DamagingObject):
    def __init__(self, termination=None, object_hit=None, range=None,
                 damage=None, heading=None, speed=None, health=None,
                 hitbox=Hitbox(1, 1, (250, 250), 0), collidable=None):
        super().__init__(range, damage, heading, speed, health, hitbox, collidable)
        # termination will be an xy tuple
        self.termination = termination
        self.object_hit = object_hit
        self.object_type = ObjectType.bullet

    @property
    def termination(self):
        return self.__termination

    @termination.setter
    def termination(self, vals):
        if vals[0] < 0 or vals[0] > GameStats.game_board_width:
            raise ValueError("x coordinate outside bounds, Not set")
        elif vals[1] < 0 or vals[1] > GameStats.game_board_height:
            raise ValueError("y coordinate outside bounds, Not set")
        else:
            self.__termination = vals

    def to_json(self):
        data = super().to_json()
        data['termination'] = self.termination
        data['object_hit'] = self.object_hit

        return data

    def from_json(self, data):
        super().from_json(data)
        self.termination = data['termination']
        self.object_hit = data['object_hit']
