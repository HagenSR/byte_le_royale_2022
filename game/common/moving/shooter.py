from copy import deepcopy

from game.common.moving.moving_object import MovingObject
from game.common.errors.inventory_full_error import InventoryFullError
from game.common.stats import GameStats
from game.common.enums import *


class Shooter(MovingObject):
    def __init__(self, heading=0, speed=0):
        super().__init__(
            heading,
            speed,
            GameStats.player_stats['starting_health'],
            GameStats.player_stats['hitbox'],
            collidable=True
        )
        self.object_type = ObjectType.shooter
        self.money = GameStats.player_stats['starting_money']
        self.armor = None
        self.visible = []
        self.view_radius = GameStats.player_stats['view_radius']
        self.moving = False

        # use list comprehension to dynamically generate the correct types and number of slots required in the inventory
        # To add new slots, add them to stats, they will be dynamically added to the shooter object on instantiation
        # Because of the way this is set up, it is VERY important that each shooter is only instantiated once per run
        #
        # this statement grabs the slot_type as a string, the object type as a Type, and puts it into a list of tuples
        self.slot_obj_types = [
            (slot_type, slot_stats['type']) for slot_type, slot_stats in GameStats.inventory_stats.items()
        ]
        # this generates an empty inventory, with number of slots for each slot type taken from game stats
        self.__inventory = {
            slot_type:
                [None for _ in range(GameStats.inventory_stats[slot_type]['slots'])]
                for slot_type, slot_obj_type in self.slot_obj_types
        }

    @property
    def inventory(self):
        return deepcopy(self.__inventory)

    @inventory.setter
    def inventory(self, value):
        self.__inventory = value

    def has_empty_slot(self, slot_type):
        for slot in self.__inventory[slot_type]:
            if not slot:
                return True
        return False

    def append_inventory(self, value):
        if not isinstance(value, tuple(slot_type[1] for slot_type in self.slot_obj_types)):
            raise TypeError(f"Value appended must be of type "
                            f"{[obj_type[1] for obj_type in self.slot_obj_types]} "
                            f"not {type(value)}")
        for slot_type, slot_obj_type in self.slot_obj_types:
            if isinstance(value, slot_obj_type) and self.has_empty_slot(slot_type):
                self.__inventory[slot_type][self.__inventory[slot_type].index(None)] = value
                return None
        raise InventoryFullError(f"Inventory full for type {type(value)}")

    def remove_from_inventory(self, obj):
        for slot_type in self.__inventory:
            # this try except block checks to make sure you're only checking the correct slot type
            try:
                self.__inventory[slot_type][self.__inventory[slot_type].index(obj)] = None
            except ValueError:
                continue
            return obj
        return None

    # set the heading and direction in a controlled way, might need to add distance attribute later
    def move(self, heading, speed):
        super().heading = heading
        if speed < GameStats.player_stats['move_speed']:
            super().speed = speed
            self.moving = True
        raise ValueError("Speed must be less than max move speed for the player")

    def stop(self):
        super().speed = 0
        self.moving = False

    def to_json(self):
        data = super().to_json()

        data['inventory'] = self.inventory
        data['visible'] = [obj.to_json() for obj in self.visible]

        data['money'] = self.money
        data['armor'] = self.armor
        data['view_radius'] = self.view_radius
        data['moving'] = self.moving

        return data

    def from_json(self, data):
        super().from_json(data)
        self.inventory = data['inventory']
        self.money = data['money']
        self.armor = data['armor']
        self.visible = data['visible']
        self.view_radius = data['view_radius']
        self.moving = data['moving']
