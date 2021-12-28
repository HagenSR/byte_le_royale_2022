from game.common.map_object import MapObject
from game.common.stats import GameStats
from game.common.enums import *
import math


# Inherits MapObject
class MovingObject(MapObject):
    def __init__(
            self,
            heading=0,
            speed=0,
            health=None,
            hitbox=Hitbox(10, 10, (250, 250), 0),
            collidable=True):
        super().__init__(health, hitbox, collidable)
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
    def heading(self, heading):
        if not 0 <= heading <= 360:
            raise ValueError("Heading must be between 0 and 360")
        self.__heading = heading
        self.hitbox.rotation = heading

    # Set speed must be greater than 0
    @speed.setter
    def speed(self, val):
        if not 0 <= val <= self.max_speed:
            raise Exception("Speed value outside bounds, Not set")
        self.__speed = val

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
        return self
