import math

from game.common.hitbox import Hitbox
from game.common.map_object import MapObject
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
        self.__partition_width = width / partitions_wide
        self.__partition_height = height / partitions_tall

        # create a 3d list. The first 2 dimensions handle the partitions
        # and the 3rd dimension holds the objects in those partitions
        self.__matrix = [
            [[] for _ in range(partitions_wide)]
            for _ in range(partitions_tall)
        ]

    def find_row(self, y: float):
        """Find which row of the structure the y coordinate is in"""
        return math.floor(y / self.__partition_height)

    def find_column(self, x: float):
        """Find which column of the structure the x coordinate is in"""
        return math.floor(x / self.__partition_height)

    def add_object(self, obj: MapObject):
        """add object to it's correct partition"""
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
        """Returns objects that are in the same partition as the x, y tuple"""
        return self.__matrix[self.find_row(y)][self.find_column(x)]

    def find_object_coordinates(self, x: float, y: float) -> bool:
        """Returns boolean whether there is an object at the coordinates"""

        for obj in self.__matrix[self.find_row(y)][self.find_column(x)]:
            if (obj.hitbox.topLeft[0] <= x <= obj.hitbox.bottomRight[0]
                    and obj.hitbox.topLeft[1] <= y <= obj.hitbox.bottomRight[1]):
                return True
        return False

    def find_object_hitbox(self, hitbox: Hitbox) -> bool:
        """Returns boolean whether there is an object that collides with the given hitbox"""
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
        if not isinstance(obj, MapObject):
            raise ValueError("Object must be of type MapObject")
        row = self.find_row(obj.hitbox.position[1])
        column = self.find_column(obj.hitbox.position[0])
        self.__matrix[row][column].remove(obj)

    def to_json(self):
        data = {'matrix': [
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
            for row in data['matrix']
        ]
