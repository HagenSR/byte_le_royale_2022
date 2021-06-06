from game.common.map_object import MapObject
from game.common.stats import GameStats
from game.common.enums import *
import math


# Inherits MapObject
class MovingObject(MapObject):
    def __init__(self, heading=0, speed=0, health=None, coordinates=None, hitbox=None, collidable=None):
        super().__init__(health, coordinates, hitbox, collidable)
        # Double underscore 'name mangles' the variable. The closest to private we can get in python
        self.heading = heading
        self.speed = speed
        self.object_type = ObjectType.moving_object

    @property
    def heading(self):
        return self.__heading

    @property
    def speed(self):
        return self.__speed
    
    # setter for heading. Should be degrees between 0 and 360 inclusive
    @heading.setter
    def heading(self, val):
        if 0 <= val <= (math.pi * 2):
            self.__heading = val
        else:
            raise Exception("Heading value outside bounds, Not set")
    
    # Set speed must be greater than 0
    @speed.setter
    def speed(self, val):
        if val >= 0 and val <= GameStats.moving_object_stats['max_speed']:
            self.__speed = val
        else: 
            raise Exception("Speed value outside bounds, Not set")

    # To_json creates a dictionary representation of the object.
    # super().to_json() calls MapObject.to_json(), which calls gameObject.to_json()
    # This dictionary can then easily be converted to json by the game engine
    def to_json(self):
        data = super().to_json()
        data['heading'] = self.heading
        data['speed'] = self.speed

        return data

    # Not actually necessary, but the idea is that it takes a json representation (dictionary)
    # And converts it back into an object
    def from_json(self, data):
        super().from_json(data)
        self.heading = data['heading']
        self.speed = data['speed']