from game.common.hitbox import Hitbox
import unittest
from game.common.moving.shooter import Shooter
from game.common.items.gun import Gun
from game.common.items.upgrade import Upgrade
from game.common.items.consumable import Consumable
from game.common.items.item import Item
from game.common.enums import *
from game.common.errors.inventory_full_error import InventoryFullError


class TestShooterObject(unittest.TestCase):
    def setUp(self) -> None:
        self.shooter = Shooter()

    def test_inventory_guns(self):
        self.assertTrue(self.shooter.has_empty_slot('guns'))

        test_gun = Gun(GunType.shotgun, 1)

        for slot in self.shooter.inventory['guns']:
            self.shooter.append_inventory(test_gun)
        self.assertFalse(self.shooter.has_empty_slot('guns'))
        self.assertEqual(
            test_gun,
            self.shooter.remove_from_inventory(test_gun))
        self.assertTrue(self.shooter.has_empty_slot('guns'))

    def test_inventory_upgrades(self):
        self.assertTrue(self.shooter.has_empty_slot('upgrades'))

        test_upgrade = Upgrade(None, None, None)

        for slot in self.shooter.inventory['upgrades']:
            self.shooter.append_inventory(test_upgrade)
        self.assertFalse(self.shooter.has_empty_slot('upgrades'))
        self.assertIsNotNone(self.shooter.remove_from_inventory(test_upgrade))
        self.assertTrue(self.shooter.has_empty_slot('upgrades'))

    def test_inventory_consumables(self):
        self.assertTrue(self.shooter.has_empty_slot('consumables'))

        test_consumable = Consumable(Hitbox(10, 10, (10, 10)), 20, 1, None, None, None)

        for slot in self.shooter.inventory['consumables']:
            self.shooter.append_inventory(test_consumable)
        self.assertFalse(self.shooter.has_empty_slot('consumables'))
        self.assertEqual(
            test_consumable,
            self.shooter.remove_from_inventory(test_consumable))
        self.assertTrue(self.shooter.has_empty_slot('consumables'))

    def test__append_inventory__wrong_inventory_type_raises_TypeError(self):
        self.assertRaises(TypeError, self.shooter.append_inventory, (Item(None, None)))

    def test__append_inventory__correct_type_inventory_full__raises_InventoryFullError(
            self):
        test_gun = Gun(GunType.shotgun, 1)
        for slot in self.shooter.inventory['guns']:
            self.shooter.append_inventory(test_gun)
        self.assertRaises(InventoryFullError, self.shooter.append_inventory, (test_gun))
