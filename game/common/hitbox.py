from game.common.game_object import GameObject
from game.common.enums import *
import game.common.stats as stats


class Hitbox(GameObject):
    def __init__(self, width, height, xy_tuple):
        super().__init__()
        self.object_type = ObjectType.hitbox
        self.width = width
        self.height = height
        # (x,y) tuple, where [0] is the x position and y is [1] of the top left corner
        # It is coerced here to be the middle
        self.position = (xy_tuple[0] + (self.width / 2), xy_tuple[1] + (self.height / 2))

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
        return (self.position[0] - (self.width/2), self.position[1] + (self.height/2))

    @property
    def topRight(self):
        return (self.position[0] + (self.width/2), self.position[1] + (self.height/2))

    @property
    def bottomLeft(self):
        return (self.position[0] - (self.width/2), self.position[1] - (self.height/2))

    @property
    def bottomRight(self):
        return (self.position[0] + (self.width/2), self.position[1] - (self.height/2))

    @property
    def middle(self):
        return self.position

    # set height between 0 and max
    @height.setter
    def height(self, val):
        if val > 0:
            self.__height = val
        else:
            raise ValueError("Tried to set an invalid height for hitbox")

    # Set width for hitbox between 0 and max
    @width.setter
    def width(self, val):
        if val > 0:
            self.__width = val
        else:
            raise ValueError("Tried to set an invalid width for hitbox")

    # set x between 0 and max game board width
    @position.setter
    def position(self, val):
        if (0 <= val[0] <= stats.GameStats.game_board_width) and (
                0 <= val[1] <= stats.GameStats.game_board_height):
            self.__position = val
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
