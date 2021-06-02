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

        self.shooter.append_inventory(test_gun)
        self.shooter.append_inventory(test_gun)
        self.assertFalse(self.shooter.has_empty_slot('guns'))
        self.assertEqual(test_gun, self.shooter.remove_from_inventory(test_gun))
        self.assertTrue(self.shooter.has_empty_slot('guns'))

