import math
from copy import deepcopy

from game.common.hitbox import Hitbox
from game.common.items.item import Item
from game.common.map_object import MapObject
from game.common.moving.moving_object import MovingObject
from game.utils import collision_detection


class PartitionGrid:
    """Structure for storing objects in partitioned 2d space"""

    def __init__(
            self,
            width: int,
            height: int,
            partitions_wide: int,
            partitions_tall: int):
        # define the length and width of each square partition
        self.partition_width = width / partitions_wide
        self.partition_height = height / partitions_tall

        # create a 3d list. The first 2 dimensions handle the partitions
        # and the 3rd dimension holds the objects in those partitions
        # each list in the 3rd dimension can be considered to be a partition
        self.__matrix = [
            [[] for _ in range(partitions_wide)]
            for _ in range(partitions_tall)
        ]

    def find_row(self, y: float):
        """Find which row of the structure the y coordinate is in"""
        return math.floor(y / self.partition_height)

    def find_column(self, x: float):
        """Find which column of the structure the x coordinate is in"""
        return math.floor(x / self.partition_height)

    def add_object(self, obj: MapObject):
        """add object to it's correct partition"""
        # TODO fix bug where object only gets added to the partition of it's topleft corner, even if it overlaps
        if not isinstance(obj, MapObject):
            raise ValueError("Object must be of type MapObject")
        row = self.find_row(obj.hitbox.position[1])
        column = self.find_column(obj.hitbox.position[0])
        self.__matrix[row][column].append(obj)

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
            (self.find_column(x) * self.partition_width, self.find_row(y) * self.partition_height)
        )

    def find_object_coordinates(self, x: float, y: float) -> bool:
        """Returns boolean whether there is an object at the coordinates"""
        for obj in self.__matrix[self.find_row(y)][self.find_column(x)]:
            if (obj.hitbox.topLeft[0] <= x <= obj.hitbox.bottomRight[0]
                    and obj.hitbox.topLeft[1] <= y <= obj.hitbox.bottomRight[1]):
                return True
        return False

    def find_object_hitbox(self, hitbox: Hitbox) -> bool:
        """Returns boolean whether there is an object that collides with the given hitbox"""
        # TODO account for objects being in multiple partitions after add object fix
        if not isinstance(hitbox, Hitbox):
            raise ValueError("Hitbox to check must be of type Hitbox")
        row = self.find_row(hitbox.position[1])
        column = self.find_column(hitbox.position[0])
        for obj in self.__matrix[row][column]:
            if collision_detection.check_collision(obj.hitbox, hitbox):
                return True
        return False

    def find_object_object(self, given_obj: MapObject) -> bool:
        """Returns boolean whether there is an object that collides with the given object"""
        # TODO account for objects being in multiple partitions after add object fix
        if not isinstance(given_obj, MapObject):
            raise ValueError("Object must be of type MapObject")
        row = self.find_row(given_obj.hitbox.position[1])
        column = self.find_column(given_obj.hitbox.position[0])
        for obj in self.__matrix[row][column]:
            if collision_detection.check_collision(
                    given_obj.hitbox, obj.hitbox):
                return True
        return False

    def remove_object(self, obj: MapObject) -> None:
        """Remove a given object from the structure"""
        # TODO account for objects being in multiple partitions after add object fix
        if not isinstance(obj, MapObject):
            raise ValueError("Object must be of type MapObject")
        row = self.find_row(obj.hitbox.position[1])
        column = self.find_column(obj.hitbox.position[0])
        self.__matrix[row][column].remove(obj)

    def get_partitions_wide(self):
        return len(self.__matrix)

    def get_partitions_tall(self):
        return len(self.__matrix[0])

    def obfuscate_partition(self, x, y):
        """Remove all moving and item objects in the partition that contains the x, y coordinates"""
        for obj in self.__matrix[self.find_row(y)][self.find_column(x)]:
            if isinstance(obj, MovingObject) or isinstance(obj, Item):
                self.remove_object(obj)

    def to_json(self):
        # TODO account for objects being in multiple partitions after add object fix
        data = {'matrix': [
            [
                [obj.to_json() if "to_json" in dir(obj) else obj for obj in self.__matrix[row][column]]
                for column in range(len(self.__matrix[row]))
            ]
            for row in range(len(self.__matrix))
        ]}

        return data

    def from_json(self, data):
        # TODO account for objects being in multiple partitions after add object fix
        self.__matrix = [
            [
                [obj.from_json() if "from_json" in dir(obj) else obj for obj in column]
                for column in row
            ]
            for row in data['matrix']
        ]
