import math

from game.common.game_object import GameObject
from game.common.enums import *
import game.common.stats as stats

import math


class Hitbox(GameObject):
    def __init__(self, width, height, xy_tuple, rotation=0):
        super().__init__()
        self.object_type = ObjectType.hitbox
        # Set width, height, rotation like this due to deadlock from both position and rotation needing eachother
        # to check if corners are out of bounds
        self.__width = width
        self.__height = height
        # (x,y) tuple, where [0] is the x position and y is [1] of the top left corner
        self.__rotation = rotation
        self.position = xy_tuple
        self.update_corners()


        #self.position = xy_tuple
        # added rotation to allow for diagonal hitboxes while keeping backwards
        # compatibility

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
    def rotation(self):
        return self.__rotation

    @property
    def topLeft(self):
        return self.__top_left

    @property
    def topRight(self):
        return self.__top_right

    @property
    def bottomLeft(self):
        return self.__bottom_left

    @property
    def bottomRight(self):
        return self.__bottom_right

    @property
    def middle(self):
        return (self.position[0] + (self.width / 2),
                self.position[1] + (self.height / 2)
                )

    # set height between 0 and max
    @height.setter
    def height(self, val):
        if val > 0:
            self.__height = val
            self.update_corners()
        else:
            raise ValueError(
                "Tried to set an invalid height for hitbox: {0}".format(val))

    # Set width for hitbox between 0 and max
    @width.setter
    def width(self, val):
        if val > 0:
            self.__width = val
            self.update_corners()
        else:
            raise ValueError(
                "Tried to set an invalid width for hitbox: {0}".format(val))

    # set x between 0 and max game board width
    @position.setter
    def position(self, xy_tuple):
        self.__position = xy_tuple
        self.update_corners()
        self.check_corner_outside()

    # set rotation
    @rotation.setter
    def rotation(self, rotation):
        self.__rotation = rotation
        self.update_corners()
        self.check_corner_outside()

    def update_corners(self):
        self.__top_left = self.rotate(self.middle, self.position, self.rotation)
        self.__top_right = self.rotate(
            self.middle,
            (self.position[0] +
             self.width,
             self.position[1]),
            self.rotation)
        self.__bottom_left = self.rotate(
            self.middle,
            (self.position[0],
             self.position[1] +
             self.height),
            self.rotation)
        self.__bottom_right = self.rotate(
            self.middle,
            (self.position[0] +
             self.width,
             self.position[1] +
             self.height),
            self.rotation)

    def check_corner_outside(self):
        '''
        Returns True if one of the corners of a hitbox is outside the gamemap
        '''
        if stats.GameStats.game_board_width < self.topLeft[0] or self.topLeft[
                0] < 0 or stats.GameStats.game_board_height < self.topLeft[1] or self.topLeft[1] < 0:
            raise ValueError(
                "Tried to set an invalid xy position tuple for hitbox: {0}, top left is out of bounds at {1}".format(
                    self.position, self.topLeft))
        elif stats.GameStats.game_board_width < self.topRight[0] or self.topRight[0] < 0 or stats.GameStats.game_board_height < self.topRight[1] or self.topRight[1] < 0:
            raise ValueError(
                "Tried to set an invalid xy position tuple for hitbox: {0}, top right is out of bounds at {1}".format(
                    self.position, self.topRight))
        elif stats.GameStats.game_board_width < self.bottomLeft[0] or self.bottomLeft[0] < 0 or stats.GameStats.game_board_height < self.bottomLeft[1] or self.bottomLeft[1] < 0:
            raise ValueError(
                "Tried to set an invalid xy position tuple for hitbox: {0}, bottom left is out of bounds at {1}".format(
                    self.position, self.bottomLeft))
        elif stats.GameStats.game_board_width < self.bottomRight[0] or self.bottomRight[0] < 0 or stats.GameStats.game_board_height < self.bottomRight[1] or self.bottomRight[1] < 0:
            raise ValueError(
                "Tried to set an invalid xy position tuple for hitbox: {0}, bottom right is out of bounds at {1}".format(
                    self.position, self.bottomRight))

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

    def rotate(self, origin, point, ngle):
        """
        Rotate a point counterclockwise by a given angle around a given origin.

        The angle should be given in degrees, then is converted to rads.
        """

        angle = math.radians(ngle)
        ox, oy = origin
        px, py = point
        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)

        return qx, qy

    def __str__(self):
        return f"""
             Height: {self.height}
             Width: {self.width}
             X: {self.position[0]}
             Y: {self.position[1]}
             """
