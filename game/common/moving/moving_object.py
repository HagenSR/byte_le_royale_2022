from game.common.map_object import MapObject
from game.common.enums import *

# Inherits MapObject
class MovingObject(MapObject):
    def __init__(self, heading=0, speed=0):
        super().__init__()
        self.__heading = heading
        self.__speed = speed

    def get_heading(self):
        return self.__heading

    def get_speed(self):
        return self.__speed

    def set_heading(self, val):
        if val >= 0 and val <= 360:
            self.__heading = val
        
    def set_speed(self, val):
        if val >= 0:
            self.__speed = val

    def to_json(self):
        data = super().to_json()
        data['heading'] = self.heading
        data['speed'] = self.speed

        return data

    def from_json(self, data):
        super().from_json(data)
        self.heading = data['heading']
        self.speed = data['speed']