import math

from game.common.door import Door
from game.common.enums import ObjectType
from game.common.hitbox import Hitbox
from game.common.items.consumable import Consumable
from game.common.items.gun import Gun
from game.common.items.item import Item
from game.common.items.money import Money
from game.common.items.upgrade import Upgrade
from game.common.map_object import MapObject
from game.common.moving.moving_object import MovingObject
from game.common.moving.shooter import Shooter
from game.common.stats import GameStats
from game.common.wall import Wall
from game.utils import collision_detection


class PartitionGrid:
    """Structure for storing objects in partitioned 2d space"""

    def __init__(
            self,
            width: int,
            height: int,
            partitions_wide: int,
            partitions_tall: int):

        if width % partitions_wide != 0 or width % partitions_tall != 0:
            raise ValueError(
                "Width and height must be evenly divisible by number of partitions")

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
        return math.floor(y / self.partition_height)

    def find_column(self, x: float):
        """Find which column of the structure the x coordinate is in"""
        return math.floor(x / self.partition_height)

    def check_overlap(self, hitbox: Hitbox):
        partitions = []
        top_left_row = self.find_row(hitbox.top_left[1])
        top_left_column = self.find_column(hitbox.top_left[0])
        top_right_row = self.find_row(hitbox.top_right[1])
        top_right_column = self.find_column(hitbox.top_right[0])
        bottom_right_row = self.find_row(hitbox.bottom_right[1])
        bottom_right_column = self.find_column(hitbox.bottom_right[0])
        bottom_left_row = self.find_row(hitbox.bottom_left[1])
        bottom_left_column = self.find_column(hitbox.bottom_left[0])
        partitions.append((top_left_row, top_left_column))
        if top_left_row != top_right_row and top_left_column != top_right_column:
            partitions.append((top_right_row, top_right_column))
        if top_right_row != bottom_right_row and top_right_column != bottom_right_column:
            partitions.append((bottom_right_row, bottom_right_column))
        if top_left_row != bottom_left_row and top_left_column != bottom_left_column:
            partitions.append((bottom_left_row, bottom_left_column))
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
            if (obj.hitbox.top_left[0] <= x <= obj.hitbox.bottom_right[0]
                    and obj.hitbox.top_left[1] <= y <= obj.hitbox.bottom_right[1]):
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
            try:
                self.__matrix[partition[0]][partition[1]].remove(obj)
            except ValueError:
                pass

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
            client.shooter.hitbox.top_left[0] +
            client.shooter.hitbox.top_right[0] /
            2,
            client.shooter.hitbox.top_left[1] +
            client.shooter.hitbox.bottom_left[1] /
            2)
        client_view_distance = client.shooter.view_distance

        # Check all partitions, if a partition isn't in view, obfuscate it
        # if it is in view, remove only objects that aren't visible

        for x in range(0, GameStats.game_board_width, self.partition_width):
            for y in range(
                    0,
                    GameStats.game_board_height,
                    self.partition_height):
                partition = self.get_partition_hitbox(x, y)
                # remove everything from a partition that isn't in view at all
                if not collision_detection.intersect_circle(
                        client_shooter_xy,
                        client_view_distance,
                        partition):
                    self.obfuscate_partition(x, y)
                else:
                    # if a partition is in view, need to check each object to
                    # see if it's in view, remove it if it isn't
                    for obj in self.get_partition_objects(x, y):
                        if not collision_detection.intersect_circle(
                                client_shooter_xy,
                                client_view_distance,
                                obj.hitbox):
                            self.remove_object(obj)

    def to_json(self):
        data = {'partition_grid': [
            [
                [obj.to_json() for obj in self.__matrix[row][column]]
                for column in range(len(self.__matrix[row]))
            ]
            for row in range(len(self.__matrix))
        ]}

        return data

    def from_json(self, data):
        self.__matrix = [
            [
                self.from_json_helper(column)
                # [obj.from_json() if "from_json" in dir(obj) else obj for obj in column]
                for column in row
            ]
            for row in data['partition_grid']
        ]
        return self

    def from_json_helper(self, data: dict):
        obj_list = list()
        for obj in data:
            if obj['object_type'] == ObjectType.consumable:
                obj_list.append(Consumable.from_json(Consumable(), obj))
            if obj['object_type'] == ObjectType.gun:
                obj_list.append(Gun.from_json(Gun(), obj))
            if obj['object_type'] == ObjectType.item:
                obj_list.append(Item.from_json(Item(), obj))
            if obj['object_type'] == ObjectType.money:
                obj_list.append(Money.from_json(Money(), obj))
            if obj['object_type'] == ObjectType.upgrade:
                obj_list.append(Upgrade.from_json(Upgrade(), obj))
            if obj['object_type'] == ObjectType.shooter:
                obj_list.append(Shooter.from_json(Shooter(), obj))
            if obj['object_type'] == ObjectType.door:
                obj_list.append(Door.from_json(Door(), obj))
            if obj['object_type'] == ObjectType.wall:
                obj_list.append(Wall.from_json(Wall(), obj))

        return obj_list
