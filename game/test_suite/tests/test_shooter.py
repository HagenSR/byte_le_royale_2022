import unittest
from game.common.moving.shooter import Shooter
from game.common.items.gun import Gun
from game.common.items.upgrade import Upgrade
from game.common.items.consumable import Consumable
from game.common.enums import *


class TestShooter(unittest.TestCase):
    def setUp(self) -> None:
        self.shooter = Shooter()

    def test_inventory(self):
        self.assertTrue(self.shooter.has_empty_slot('guns'))
        self.assertTrue(self.shooter.has_empty_slot('upgrades'))
        self.assertTrue(self.shooter.has_empty_slot('consumables'))

        test_gun = Gun(GunType.shotgun, 1)
        test_upgrade = Upgrade()
        test_consumable = Consumable()

        for slot in self.shooter.inventory['guns']:
            self.shooter.append_inventory(test_gun)
        self.assertFalse(self.shooter.has_empty_slot('guns'))
        self.assertEqual(test_gun, self.shooter.remove_from_inventory(test_gun))
        self.assertTrue(self.shooter.has_empty_slot('guns'))

        for slot in self.shooter.inventory['upgrades']:
            self.shooter.append_inventory(test_upgrade)
        self.assertFalse(self.shooter.has_empty_slot('upgrades'))
        self.assertIsNotNone(self.shooter.remove_from_inventory(test_upgrade))
        self.assertTrue(self.shooter.has_empty_slot('upgrades'))

        for slot in self.shooter.inventory['consumables']:
            self.shooter.append_inventory(test_consumable)
        self.assertFalse(self.shooter.has_empty_slot('consumables'))
        self.assertEqual(test_consumable, self.shooter.remove_from_inventory(test_consumable))
        self.assertTrue(self.shooter.has_empty_slot('consumables'))

