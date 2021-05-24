from game.common.map_object import MapObject
from game.common.enums import *

class MovingObject(MapObject):
    def __init__(self, heading=None, speed=None):
        super().__init__()
        self.heading = heading
        self.speed = speed


    def to_json(self):
        data = super().to_json()
        data['heading'] = self.heading
        data['speed'] = self.speed

        return data

    def from_json(self, data):
        super().from_json()
        self.heading = data['heading']
        self.speed = data['speed']