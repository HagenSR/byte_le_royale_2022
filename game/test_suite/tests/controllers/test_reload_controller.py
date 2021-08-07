import unittest

from game.common.action import Action
from game.common.enums import ActionType, GunType, GunLevel
from game.common.hitbox import Hitbox
from game.common.items.gun import Gun
from game.common.map_object import MapObject
from game.common.moving.shooter import Shooter
from game.common.player import Player
from game.controllers.reload_controller import ReloadController
from game.utils.partition_grid import PartitionGrid


class TestReloadController(unittest.TestCase):
    def setUp(self):
        act = Action()
        act.set_action(ActionType.reload)
        self.myPlayer = Player(action=act, shooter=Shooter(0, 0, Hitbox(10, 10, (10, 10))))
        self.myPlayer.shooter.append_inventory(Gun(GunType.shotgun, GunLevel.level_two, hitbox=Hitbox(10,10, (10,10))))
        self.reloadController = ReloadController()

    def test_reload_when_empty(self):
        self.myPlayer.shooter.primary_gun.mag_ammo = 0
        ReloadController.handle_actions(self.myPlayer)
        self.assertEqual(self.myPlayer.shooter.primary_gun.mag_ammo, self.myPlayer.shooter.primary_gun.mag_size)

    def test_reload_when_full(self):
        self.myPlayer.shooter.primary_gun.mag_ammo = self.myPlayer.shooter.primary_gun.mag_size
        ReloadController.handle_actions(self.myPlayer)
        self.assertEqual(self.myPlayer.shooter.primary_gun.mag_ammo, self.myPlayer.shooter.primary_gun.mag_size)

    def test_reload_when_partially_full(self):
        self.myPlayer.shooter.primary_gun.mag_ammo = self.myPlayer.shooter.primary_gun.mag_size - 1
        ReloadController.handle_actions(self.myPlayer)
        self.assertEqual(self.myPlayer.shooter.primary_gun.mag_ammo, self.myPlayer.shooter.primary_gun.mag_size)

