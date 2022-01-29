from game.common.game_object import GameObject
from game.common.enums import *
from game.common.stats import GameStats

import math


def rotate(origin, point, angle_deg):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in degrees, then is converted to rads.
    """

    angle_rad = math.radians(angle_deg)
    ox, oy = origin
    px, py = point
    qx = ox + math.cos(angle_rad) * (px - ox) - math.sin(angle_rad) * (py - oy)
    qy = oy + math.sin(angle_rad) * (px - ox) + math.cos(angle_rad) * (py - oy)

    return qx, qy


class Hitbox(GameObject):
    def __init__(self, width, height, xy_tuple, rotation=0):
        super().__init__()
        self.object_type = ObjectType.hitbox
        # Set width, height, rotation like this due to deadlock from both position and rotation needing each other
        # to check if corners are out of bounds
        self.__width = width
        self.__height = height
        # (x,y) tuple, where [0] is the x position and y is [1] of the top left corner
        self.position = xy_tuple
        self.update_corners()

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
        return 0

    @property
    def top_left(self):
        return self.__top_left

    @property
    def top_right(self):
        return self.__top_right

    @property
    def bottom_left(self):
        return self.__bottom_left

    @property
    def bottom_right(self):
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
        corners = [
            rotate(self.middle, self.position, self.rotation),
            rotate(
                self.middle, (self.position[0] + self.width, self.position[1]), self.rotation),
            rotate(
                self.middle, (self.position[0], self.position[1] + self.height), self.rotation),
            rotate(self.middle, (self.position[0] + self.width,
                                 self.position[1] + self.height), self.rotation)
        ]

        # this is so each corner is guaranteed to be in its spot
        corners = sorted(corners, key=lambda coord: coord[0] + coord[1])
        self.__top_left = corners[0]
        self.__top_right = max([corners[1], corners[2]],
                               key=lambda coord: coord[0])
        self.__bottom_left = max(
            [corners[1], corners[2]], key=lambda coord: coord[1])
        self.__bottom_right = corners[3]

    def check_corner_outside(self):
        '''
        Returns True if one of the corners of a hitbox is outside the gamemap
        '''
        if GameStats.game_board_width < self.top_left[0] or self.top_left[
                0] < 0 or GameStats.game_board_height < self.top_left[1] or self.top_left[1] < 0:
            raise ValueError(
                "Tried to set an invalid xy position tuple for hitbox: {0}, top left is out of bounds at {1}".format(
                    self.position, self.top_left))
        elif GameStats.game_board_width < self.top_right[0] or self.top_right[0] < 0 or GameStats.game_board_height < self.top_right[1] or self.top_right[1] < 0:
            raise ValueError(
                "Tried to set an invalid xy position tuple for hitbox: {0}, top right is out of bounds at {1}".format(
                    self.position, self.top_right))
        elif GameStats.game_board_width < self.bottom_left[0] or self.bottom_left[0] < 0 or GameStats.game_board_height < self.bottom_left[1] or self.bottom_left[1] < 0:
            raise ValueError(
                "Tried to set an invalid xy position tuple for hitbox: {0}, bottom left is out of bounds at {1}".format(
                    self.position, self.bottom_left))
        elif GameStats.game_board_width < self.bottom_right[0] or self.bottom_right[0] < 0 or GameStats.game_board_height < self.bottom_right[1] or self.bottom_right[1] < 0:
            raise ValueError(
                "Tried to set an invalid xy position tuple for hitbox: {0}, bottom right is out of bounds at {1}".format(
                    self.position, self.bottom_right))

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
