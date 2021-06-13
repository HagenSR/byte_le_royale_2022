from game.common.moving.damaging.damaging_object import DamagingObject
from game.common.stats import GameStats
from game.common.enums import *

class Bullet(DamagingObject):
    def __init__(self, termination = {'x': 0, 'y': 0}, object_hit = None, range= None, 
        damage= None, heading = None, speed = None, health=None, coordinates=None,
        hitbox=None, collidable=None):
        super().__init__(range, damage, heading, speed, health, coordinates, hitbox, collidable)
        self.termination = termination
        self.object_hit = object_hit
        self.object_type = ObjectType.bullet

    @property
    def termination(self):
        return self.__termination
    

    @termination.setter
    def termination(self, x_value, y_value):
        if x_value >= 0 and x_value <= GameStats.game_board_width:
            self.__termination['x'] = x_value
        else:
            raise Exception("x coordinate value outside bounds, Not set")
        if y_value >= 0 and y_value <= GameStats.game_board_height:
            self.__termination['y'] = y_value
        else:
            raise Exception("y coordinate value outside bounds, Not set")


    @property
    def object_hit(self):
        return self.__object_hit
        
    def to_json(self):
        data = super().to_json()
        data['termination'] = self.termination
        data['object_hit'] = self.object_hit

        return data

    def from_json(self, data):
        super().from_json(data)
        self.termination = data['termination']
        self.object_hit = data['object_hit']
    
