from game.common.hitbox import Hitbox
from game.common.game_object import GameObject
from game.common.enums import ObjectType, Upgrades
from game.common.items.upgrade import Upgrade
from game.common.stats import GameStats
from game.common.moving.shooter import Shooter
from game.common.wall import Wall
from game.common.items.item import Item
from game.common.ray import Ray
from copy import deepcopy
import math

from game.utils.partition_grid import PartitionGrid


class GameBoard(GameObject):
    # the width and height parameters have default values to allow them to be
    # set for unit testing purposes
    def __init__(self, width=GameStats.game_board_width,
                 height=GameStats.game_board_height):
        super().__init__()
        self.object_type = ObjectType.game_board

        # pull width and height values from GameStats
        self.width = width
        self.height = height

        self.partition = PartitionGrid(
            width, height, int(width / 25), int(height / 25))
        self.ray_list = []

        # this calculates starting radius to totally encompass the map at start
        # with delay
        self.circle_radius = math.sqrt(
            (self.width / 2) ** 2 + (self.height / 2) ** 2) + GameStats.circle_delay

    @property
    def circle_radius(self):
        return self.__circle_radius

    # setter for circle radius. must be greater than or equal to zero
    @circle_radius.setter
    def circle_radius(self, val):
        if val > 0:
            self.__circle_radius = val
        else:
            self.__circle_radius = 0

    def obfuscate(self):
        super().obfuscate()

    def to_json(self):
        data = super().to_json()

        data['width'] = self.width
        data['height'] = self.height

        data['partition'] = self.partition.to_json()
        data['ray_list'] = [ray.to_json() for ray in self.ray_list]

        data['circle_radius'] = self.circle_radius

        return data

    def from_json(self, data):
        super().from_json(data)

        self.width = data['width']
        self.height = data['height']

        self.partition.from_json(data['partition'])
        r = Ray()
        self.ray_list = [r.from_json(ray) for ray in data['ray_list']]

        self.circle_radius = data['circle_radius']

        return self
