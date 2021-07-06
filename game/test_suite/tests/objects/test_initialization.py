# This is a quick example test file to show you the basics.
# Always remember to add the proper details to the __init__.py file in the 'tests' folder
# to insure your tests are run.

from game.common.hitbox import Hitbox
from game.common.map_object import MapObject
import unittest
from game.common.items.gun import Gun
from game.common.items.item import Item
from game.common.moving.moving_object import MovingObject
from game.common.moving.damaging.damaging_object import DamagingObject
from game.common.moving.damaging.grenade import Grenade
from game.common.moving.damaging.bullet import Bullet
from game.common.moving.shooter import Shooter
from game.common.action import Action
from game.common.game_board import GameBoard
from game.common.game_board import GameObject
from game.common.player import Player
from game.common.wall import Wall
from game.common.items.consumable import Consumable
from game.common.items.upgrade import Upgrade
from game.common.door import Door
from game.common.stats import GameStats
from game.common.enums import ObjectType, GunLevel, GunType


class TestInit(
        unittest.TestCase):  # Your test class is a subclass of unittest.Testcase, this is important

    # This method is used to set up anything you wish to test prior to every
    # test method below.
    def setUp(self):
        self.gun = Gun(
            gun_type=GunType.assault_rifle,
            level=GunLevel.level_one)
        self.item = Item(hitbox=Hitbox(10, 10, (10, 10)))
        self.damaging = DamagingObject(hitbox=Hitbox(
            10, 10, (10, 10)), heading=1, speed=10)
        self.movObj = MovingObject(1, 10)
        self.shooter = Shooter()
        self.action = Action()
        self.gameBoard = GameBoard()
        self.gameObj = GameObject()
        self.map = MapObject()
        self.player = Player()
        self.wall = Wall(hitbox=Hitbox(10, 10, (10, 10)))
        self.bltObj = Bullet((25, 25), False, range=5, damage=5)
        self.grnObj = Grenade(heading=1, speed=1, range=10, damage=10)
        self.consumable = Consumable(hitbox=Hitbox(
            10, 10, (10, 10)), health=10, count=1)
        self.upgrade = Upgrade(
            hitbox=Hitbox(
                10, 10, (10, 10)), health=10, count=1)
        self.door = Door(hitbox=Hitbox(10, 10, (10, 10)))

    def testObjectInit(self):
        self.assertEqual(self.gun.object_type, ObjectType.gun)
        self.assertEqual(self.item.object_type, ObjectType.item)
        self.assertEqual(self.grnObj.object_type, ObjectType.grenade)
        self.assertEqual(self.damaging.object_type, ObjectType.damaging_object)
        self.assertEqual(self.movObj.object_type, ObjectType.moving_object)
        self.assertEqual(self.shooter.object_type, ObjectType.shooter)
        self.assertEqual(self.action.object_type, ObjectType.action)
        self.assertEqual(self.gameBoard.object_type, ObjectType.game_board)
        self.assertEqual(self.gameObj.object_type, 0)
        self.assertEqual(self.map.object_type, ObjectType.map_object)
        self.assertEqual(self.player.object_type, ObjectType.player)
        self.assertEqual(self.wall.object_type, ObjectType.wall)
        self.assertEqual(self.consumable.object_type, ObjectType.consumable)
        self.assertEqual(self.upgrade.object_type, ObjectType.upgrade)

    # This is just the very basics of how to set up a test file
    # For more info: https://docs.python.org/3/library/unittest.html
if __name__ == '__main__':
    unittest.main
