import math

from game.common.game_object import GameObject
from game.common.enums import *
import game.common.stats as stats


class Hitbox(GameObject):
    def __init__(self, width, height, xy_tuple, rotation=0):
        super().__init__()
        self.object_type = ObjectType.hitbox
        self.width = width
        self.height = height
        # (x,y) tuple, where [0] is the x position and y is [1] of the top left corner
        self.position = xy_tuple
        # added rotation to allow for diagonal hitboxes while keeping backwards
        # compatibility
        self.rotation = math.radians(rotation)

        self.__calculate_positions()

    # method to be called anytime positions should change
    def __calculate_positions(self):
        # use backing variables so the equations don't get calculated everytime
        # the property gets called
        self.__topRight = (self.position[0] +
                           (self.width *
                            math.cos(self.rotation)), self.position[1] +
                           (self.width *
                            math.sin(self.rotation)))
        self.__bottomLeft = (self.position[0] +
                             (self.height *
                              math.sin(self.rotation)), self.position[1] +
                             (self.height *
                              math.cos(self.rotation)))
        self.__bottomRight = (self.__bottomLeft[0] + (self.width * math.cos(
            self.rotation)), self.__bottomLeft[1] + (self.width * math.sin(self.rotation)))

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def position(self):
        return self.__position

    @property
    def topLeft(self):
        return self.position

    @property
    def topRight(self):
        return self.__topRight

    @property
    def bottomLeft(self):
        return self.__bottomLeft

    @property
    def bottomRight(self):
        return self.__bottomRight

    @property
    def middle(self):
        return (
            self.position[0] +
            self.width /
            2,
            self.position[1] +
            self.height /
            2)

    # set height between 0 and max
    @height.setter
    def height(self, val):
        if val > 0:
            self.__height = val
            self.__calculate_positions()
        else:
            raise ValueError("Tried to set an invalid height for hitbox")

    # Set width for hitbox between 0 and max
    @width.setter
    def width(self, val):
        if val > 0:
            self.__width = val
            self.__calculate_positions()
        else:
            raise ValueError("Tried to set an invalid width for hitbox")

    # set x between 0 and max game board width
    @position.setter
    def position(self, val):
        if (0 <= val[0] <= stats.GameStats.game_board_width) and (
                0 <= val[1] <= stats.GameStats.game_board_height):
            self.__position = val
            self.__calculate_positions()
        else:
            raise ValueError(
                "Tried to set an invalid xy position tuple for hitbox")

    def to_json(self):
        data = super().to_json()
        data['width'] = self.width
        data['height'] = self.height
        data['position'] = self.position
        return data

    def from_json(self, data):
        super().from_json(data)
        self.width = data['width']
        self.height = data['height']
        self.position = data['position']

    def __str__(self):
        return f"""
             Height: {self.height}
             Width: {self.width}
             X: {self.position[0]}
             Y: {self.position[1]}
             """
