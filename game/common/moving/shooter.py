from game.common.moving.moving_object import MovingObject
from game.common.items.gun import Gun
from game.common.items.upgrade import Upgrade
from game.common.items.consumable import Consumable
from game.common.items.item import Item
from game.common.errors.inventory_full_error import InventoryFullError
from game.common.stats import GameStats
from game.common.enums import *


class Shooter(MovingObject):
    def __init__(self, heading=0, speed=0, coordinates=GameStats.player_stats['starting_coordinates']):
        super().__init__(
            heading,
            speed,
            GameStats.player_stats['starting_health'],
            coordinates,
            GameStats.player_stats['hitbox'],
            collidable=True
        )
        self.object_type = ObjectType.shooter
        self.money = GameStats.player_stats['starting_money']
        self.armor = None
        self.visible = []
        self.view_radius = GameStats.player_stats['view_radius']
        self.moving = False

        self.__inventory = {
            'guns':
                [None] * GameStats.inventory_stats['guns'],
            'upgrades':
                [None] * GameStats.inventory_stats['upgrades'],
            'consumables':
                [None] * GameStats.inventory_stats['consumables']
        }

    @property
    def inventory(self):
        return self.__inventory

    @inventory.setter
    def inventory(self, value):
        self.__inventory = value

    def has_empty_slot(self, slot_type):
        for slot in self.__inventory[slot_type]:
            if not slot:
                return True
        return False

    def append_inventory(self, value):
        if not isinstance(value, (Gun, Upgrade, Consumable)):
            raise TypeError(f"Value appended must be of type Gun, Upgrade, or Consumable, not {type(value)}")
        if isinstance(value, Gun) and self.has_empty_slot('guns'):
            self.__inventory['guns'].replace(None, value, 1)
            return None
        if isinstance(value, Upgrade) and self.has_empty_slot('upgrades'):
            self.__inventory['upgrades'].replace(None, value, 1)
            return None
        if isinstance(value, Consumable) and self.has_empty_slot('consumables'):
            self.__inventory['consumables'].replace(None, value, 1)
            return None
        raise InventoryFullError(f"Inventory full for type {type(value)}")

    def remove_from_inventory(self, obj):
        for slot_type in self.__inventory:
            self.__inventory[slot_type].replace(obj, None, 1)
            return obj
        return None

    # set the heading and direction in a controlled way, might need to add distance attribute later
    def move(self, heading):
        super().heading = heading
        super().speed = GameStats.player_stats['move_speed']
        self.moving = True

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
