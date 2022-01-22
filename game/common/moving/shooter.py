from copy import deepcopy

from game.common.items.gun import Gun
from game.common.items.upgrade import Upgrade
from game.common.items.consumable import Consumable
from game.common.hitbox import Hitbox
import game.common.items.gun
import game.common.items.upgrade
import game.common.items.consumable
from game.common.items.item import Item
from game.common.moving.damaging.grenade import Grenade
from game.common.items.money import Money
from game.common.moving.moving_object import MovingObject
from game.common.items.gun import Gun
from game.common.errors.inventory_full_error import InventoryFullError
from game.common.stats import GameStats
from game.common.enums import *
from game.utils import helpers


class Shooter(MovingObject):
    """The main player within the game logic"""

    def __init__(
            self,
            heading=0,
            speed=0,
            hitbox=Hitbox(10, 10, (250, 250), 0)):
        super().__init__(
            heading,
            speed,
            GameStats.player_stats['starting_health'],
            hitbox,
            collidable=True
        )
        self.object_type = ObjectType.shooter

        self.field_of_view = GameStats.player_stats['field_of_view']
        self.view_distance = GameStats.player_stats['view_distance']
        self.max_speed = GameStats.player_stats['max_distance_per_turn']

        self.money = GameStats.player_stats['starting_money']
        self.armor = None
        self.shield = False

        # use list comprehension to dynamically generate the correct types and number of slots required in the inventory
        # To add new slots, add them to stats, they will be dynamically added to the shooter object on instantiation
        # Because of the way this is set up, it is VERY important that each shooter is only instantiated once per run
        #
        # this statement grabs the slot_type as a string, the object type as a
        # Type, and puts it into a list of tuples
        self.slot_obj_types = [
            ('guns', game.common.items.gun.Gun),
            ('upgrades', game.common.items.upgrade.Upgrade),
            ('consumables', game.common.items.consumable.Consumable)]

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

        # how far shooter can throw grenade
        self.grenade_distance = 50

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
        """Add object to inventory. Not allowed for client use! Will be disqualified if called in contestant's code"""
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

    def remove_grenade(self):
        for obj in self.__inventory['consumables']:
            if isinstance(obj, Grenade):
                self.__inventory['consumables'][self.__inventory['consumables'].index(obj)] = None
                return obj
        return None

    @property
    def grenade_distance(self):
        return self.__grenade_distance

    @grenade_distance.setter
    def grenade_distance(self, val):
        if 0 <= val <= 200:
            self.__grenade_distance = val
        else:
            raise Exception("Tried to set a grenade distance greater than the max of 200 or below 0")

    def remove_from_inventory(self, obj):
        """Remove object from inventory"""
        for slot_type in self.__inventory:
            # this try except block checks to make sure you're only checking
            # the correct slot type
            try:
                self.__inventory[slot_type][self.__inventory[slot_type].index(obj)] = None
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

    def to_json(self):
        data = super().to_json()
        data['inventory'] = {
            'inventory': {
                slot_type:
                    [obj.to_json() if obj else None for obj in self.__inventory[slot_type]]
                for slot_type in self.__inventory
            }
        }
        data['money'] = self.money
        data['armor'] = self.armor
        data['view_distance'] = self.view_distance
        data['grenade_distance'] = self.grenade_distance

        return data

    def from_json(self, data):
        super().from_json(data)
        self.__inventory = {
            slot_type:
                self.from_json_helper(data['inventory'][slot_type])
            for slot_type in data['inventory']
        }
        self.money = data['money']
        self.armor = data['armor']
        self.view_distance = data['view_distance']
        self.grenade_distance = data['grenade_distance']
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

        return obj_list
