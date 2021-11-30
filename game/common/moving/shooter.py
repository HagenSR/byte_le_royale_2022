from copy import deepcopy

from game.common.moving.moving_object import MovingObject
from game.common.items.gun import Gun
from game.common.errors.inventory_full_error import InventoryFullError
from game.common.stats import GameStats
from game.common.enums import *
import math


class Shooter(MovingObject):
    """The main player within the game logic"""

    def __init__(
            self,
            heading=0,
            speed=0,
            hitbox=None):
        super().__init__(
            heading,
            speed,
            GameStats.player_stats['starting_health'],
            hitbox,
            collidable=True
        )
        self.heading = math.radians(heading)
        self.object_type = ObjectType.shooter
        self.money = GameStats.player_stats['starting_money']
        self.armor = None
        self.visible = []
        self.field_of_view = GameStats.player_stats['field_of_view']
        self.view_distance = GameStats.player_stats['view_distance']
        self.moving = False

        # use list comprehension to dynamically generate the correct types and number of slots required in the inventory
        # To add new slots, add them to stats, they will be dynamically added to the shooter object on instantiation
        # Because of the way this is set up, it is VERY important that each shooter is only instantiated once per run
        #
        # this statement grabs the slot_type as a string, the object type as a
        # Type, and puts it into a list of tuples
        self.slot_obj_types = [
            (slot_type,
             slot_stats['type']) for slot_type,
            slot_stats in GameStats.inventory_stats.items()]
        # this generates an empty inventory, with number of slots for each slot
        # type taken from game stats
        self.__inventory = {
            slot_type: [
                None for _ in range(
                    GameStats.inventory_stats[slot_type]['slots'])] for slot_type,
            slot_obj_type in self.slot_obj_types}

        # set initial primary gun to be none
        self.__primary_pointer = 0
        self.__primary = self.__inventory['guns'][self.__primary_pointer]

    @property
    def inventory(self):
        return deepcopy(self.__inventory)

    def has_empty_slot(self, slot_type):
        """check if there's an empty slot of a particular type in the inventory"""
        for slot in self.__inventory[slot_type]:
            if not slot:
                return True
        return False

    def append_inventory(self, value):
        """Add object to inventory"""
        if not isinstance(
            value, tuple(
                slot_type[1] for slot_type in self.slot_obj_types)):
            raise TypeError(
                f"Value appended must be of type "
                f"{[obj_type[1] for obj_type in self.slot_obj_types]} "
                f"not {type(value)}")
        for slot_type, slot_obj_type in self.slot_obj_types:
            if isinstance(
                    value,
                    slot_obj_type) and self.has_empty_slot(slot_type):
                self.__inventory[slot_type][self.__inventory[slot_type].index(
                    None)] = value
                return None
        raise InventoryFullError(f"Inventory full for type {type(value)}")

    def remove_from_inventory(self, obj):
        """Remove object from inventory"""
        for slot_type in self.__inventory:
            # this try except block checks to make sure you're only checking
            # the correct slot type
            try:
                self.__inventory[slot_type][self.__inventory[slot_type].index(
                    obj)] = None
            except ValueError:
                continue
            # if a gun is removed and it's the primary one, cycle to the next
            # one
            if isinstance(obj, Gun) and obj == self.primary_gun:
                self.cycle_primary()
            return obj
        return None

    @property
    def primary_gun(self):
        """Gun currently equipped"""
        return self.__inventory['guns'][self.__primary_pointer]

    def cycle_primary(self):
        """Cycle primary gun to the next one in the inventory"""

        def cycle():
            if self.__primary_pointer >= len(self.__inventory['guns']):
                self.__primary_pointer = 0
                return self.primary_gun
            self.__primary_pointer += 1

        # cycle to the next gun
        cycle()
        # if the next gun is None, cycle until you find one that isn't
        if self.primary_gun is None:
            # use a for loop here because you don't want infinite loop
            # scenarios if they're all None
            for gun in self.__inventory['guns']:
                if gun is None:
                    cycle()
                else:
                    break
        return self.primary_gun

    # set the heading and direction in a controlled way, might need to add
    # distance attribute later
    def move(self, heading, speed):
        """Set heading and speed to handle moving"""
        self.heading = math.radians(heading)
        self.hitbox.rotation = heading
        # if speed < GameStats.player_stats['move_speed']:
        self.speed = speed
        self.moving = True
        # raise ValueError(
        #  "Speed must be less than max move speed for the player")

   # def stop(self):
        # """Define stop movement"""
        # super().speed = 0
        # self.moving = False

    def to_json(self):
        data = super().to_json()

        data['inventory'] = self.inventory
        data['visible'] = [obj.to_json() for obj in self.visible]

        data['money'] = self.money
        data['armor'] = self.armor
        data['view_distance'] = self.view_distance
        data['moving'] = self.moving

        return data

    def from_json(self, data):
        super().from_json(data)
        self.inventory = data['inventory']
        self.money = data['money']
        self.armor = data['armor']
        self.visible = data['visible']
        self.view_distance = data['view_distance']
        self.moving = data['moving']
        return self
