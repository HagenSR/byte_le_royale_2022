
from game.common.moving_object import MovingObject
from game.common.enums import *


class DamagingObject(MovingObject)
    def _init_(self, range=0, damage=0, heading = None, speed = None, 
               health=None, coordinates=None, hitbox=None, collidable=None)):
        super().__init__(heading, speed, health, coordinates, hitbox, collidable)
            self.__range = range
            self.__damage = damage
        
    def get_range(self):
        return self.__range
        
    def get__damage(self):
        return self.__damage
        
    def set_range(self, val):
        if val >= 0:
            self.__range = val
    
    def set_damage(self, val):
         if val>= 0:
            self.__damage = val

    # To_json creates a dictionary representation of the object.
    # super().to_json() calls MapObject.to_json(), which calls gameObject.to_json()
    # This dictionary can then easily be converted to json by the game engine
    def to_json(self):
        data = super().to_json()
        data['range'] = self.range
        data['damage'] = self.damage

        return data

    # Not actually necessary, but the idea is that it takes a json representation (dictionary)
    # And converts it back into an object
    def from_json(self, data):
        super().from_json(data)
        self.range = data['range']
        self.damage = data['damage']