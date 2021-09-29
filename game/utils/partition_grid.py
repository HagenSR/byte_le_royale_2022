import math
from copy import deepcopy, copy

from game.common import game_board
from game.common.hitbox import Hitbox
from game.common.items.item import Item
from game.common.map_object import MapObject
from game.common.moving.moving_object import MovingObject
from game.common.stats import GameStats
from game.utils import collision_detection
from game.utils.collision_detection import arc_intersect_rect


class PartitionGrid:
    """Structure for storing objects in partitioned 2d space"""
    def __init__(
            self,
            width: int,
            height: int,
            partitions_wide: int,
            partitions_tall: int):

        if width % partitions_wide != 0 or width % partitions_tall != 0:
            raise ValueError("Width and height must be evenly divisible by number of partitions")

        # define the length and width of each square partition
        self.partition_width = width // partitions_wide
        self.partition_height = height // partitions_tall

        # create a 3d list. The first 2 dimensions handle the partitions
        # and the 3rd dimension holds the objects in those partitions
        # each list in the 3rd dimension can be considered to be a partition
        self.__matrix = [
            [[] for _ in range(partitions_wide)]
            for _ in range(partitions_tall)
        ]

    def find_row(self, y: float):
        """Find which row of the structure the y coordinate is in"""
        return math.floor(y / self.partition_height) - 1

    def find_column(self, x: float):
        """Find which column of the structure the x coordinate is in"""
        return math.floor(x / self.partition_height) - 1

    def check_overlap(self, hitbox: Hitbox):
        partitions = []
        topLeft_row = self.find_row(hitbox.topLeft[1])
        topLeft_column = self.find_column(hitbox.topLeft[0])
        topRight_row = self.find_row(hitbox.topRight[1])
        topRight_column = self.find_column(hitbox.topRight[0])
        bottomRight_row = self.find_row(hitbox.bottomRight[1])
        bottomRight_column = self.find_column(hitbox.bottomRight[0])
        bottomLeft_row = self.find_row(hitbox.bottomLeft[1])
        bottomLeft_column = self.find_column(hitbox.bottomLeft[0])
        partitions.append((topLeft_row, topLeft_column))
        if topLeft_row != topRight_row and topLeft_column != topRight_column:
            partitions.append((topRight_row, topRight_column))
        if topRight_row != bottomRight_row and topRight_column != bottomRight_column:
            partitions.append((bottomRight_row, bottomRight_column))
        if topLeft_row != bottomLeft_row and topLeft_column != bottomLeft_column:
            partitions.append((bottomLeft_row, bottomLeft_column))
        return partitions

    def add_object(self, obj: MapObject):
        """add object to it's correct partition"""
        if not isinstance(obj, MapObject):
            raise ValueError("Object must be of type MapObject")
        for partition in self.check_overlap(obj.hitbox):
            self.__matrix[partition[0]][partition[1]].append(obj)

    def add_object_list(self, object_list: 'list[MapObject]'):
        """add a list of objects to their correct partition"""
        for obj in object_list:
            self.add_object(obj)

    def get_partition_objects(self, x: float, y: float):
        """Returns objects that are in the same partition as the x, y coordinates"""
        return self.__matrix[self.find_row(y)][self.find_column(x)]

    def get_partition_hitbox(self, x: float, y: float):
        """Returns hitbox of a partition at the x, y coordinates"""
        return Hitbox(
            self.partition_width,
            self.partition_height,
            (self.find_column(x) *
             self.partition_width,
             self.find_row(y) *
             self.partition_height))

    def get_partition_objects_by_index(self, x: int, y: int):
        """Returns objects that are in the partition at indices [y][x]"""
        return self.__matrix[y][x]

    def find_object_coordinates(self, x: float, y: float) -> bool:
        """Returns the object if there is an object at the coordinates, or false otherwise"""
        for obj in self.__matrix[self.find_row(y)][self.find_column(x)]:
            if (obj.hitbox.topLeft[0] <= x <= obj.hitbox.bottomRight[0]
                    and obj.hitbox.topLeft[1] <= y <= obj.hitbox.bottomRight[1]):
                return obj
        return False

    def find_object_hitbox(self, hitbox: Hitbox) -> bool:
        """Returns the object if there is an object that collides with the given hitbox, or false otherwise"""
        if not isinstance(hitbox, Hitbox):
            raise ValueError("Hitbox to check must be of type Hitbox")
        for partition in self.check_overlap(hitbox):
            for obj in self.__matrix[partition[0]][partition[1]]:
                if collision_detection.check_collision(obj.hitbox, hitbox):
                    return obj
        return False

    def find_object_object(self, given_obj: MapObject) -> bool:
        """Returns object if there is an object that collides with the given object, false otherwise"""
        if not isinstance(given_obj, MapObject):
            raise ValueError("Object must be of type MapObject")
        for partition in self.check_overlap(given_obj.hitbox):
            for obj in self.__matrix[partition[0]][partition[1]]:
                if collision_detection.check_collision(
                        given_obj.hitbox, obj.hitbox):
                    return obj
        return False

    def remove_object(self, obj: MapObject) -> None:
        """Remove a given object from the structure"""
        if not isinstance(obj, MapObject):
            raise ValueError("Object must be of type MapObject")
        for partition in self.check_overlap(obj.hitbox):
            self.__matrix[partition[0]][partition[1]].remove(obj)

    def get_partitions_wide(self):
        return len(self.__matrix)

    def get_partitions_tall(self):
        return len(self.__matrix[0])

    def obfuscate_partition(self, x, y):
        """Remove all moving and item objects in the partition that contains the x, y coordinates"""
        for obj in self.__matrix[self.find_row(y)][self.find_column(x)]:
            if isinstance(obj, MovingObject) or isinstance(obj, Item):
                self.remove_object(obj)

    def obfuscate(self, client):
        # get center of client hitbox for origin of view arc
        client_shooter_xy = (
            client.shooter.hitbox.topLeft[0] +
            client.shooter.hitbox.topRight[0] /
            2,
            client.shooter.hitbox.topLeft[1] +
            client.shooter.hitbox.bottomLeft[1] /
            2)
        client_heading = client.shooter.heading
        client_view_distance = client.shooter.view_distance
        client_field_of_view = client.shooter.field_of_view

        # Check all partitions, if a partition isn't in view, obfuscate it
        # if it is in view, remove only objects that aren't visible
        for x, y in range(
                0, GameStats.game_board_width, self.partition_width), range(
            0, GameStats.game_board_height, self.partition_height):
            partition = self.get_partition_hitbox(x, y)
            # remove everything from a partition that isn't in view at all
            if not arc_intersect_rect(
                    partition,
                    client_heading,
                    client_field_of_view,
                    client_view_distance,
                    client_shooter_xy):
                self.obfuscate_partition(x, y)
            else:
                # if a partition is in view, need to check each object to
                # see if it's in view, remove it if it isn't
                for obj in self.get_partition_objects(x, y):
                    if not arc_intersect_rect(
                            obj.hitbox,
                            client_heading,
                            client_field_of_view,
                            client_view_distance,
                            client_shooter_xy):
                        self.remove_object(obj)

    def to_json(self):
        data = {'partition_grid': [
            [
                [obj.to_json() if "to_json" in dir(obj) else obj for obj in self.__matrix[row][column]]
                for column in range(len(self.__matrix[row]))
            ]
            for row in range(len(self.__matrix))
        ]}

        return data

    def from_json(self, data):
        self.__matrix = [
            [
                [obj.from_json() if "from_json" in dir(obj) else obj for obj in column]
                for column in row
            ]
            for row in data['partition_grid']
        ]
