import unittest
import math
import json

from game.utils.ray_utils import *
from game.common.game_board import GameBoard
from game.common.player import Player
from game.common.moving.shooter import Shooter
from game.common.items.gun import Gun
from game.common.hitbox import Hitbox
from game.common.map_object import MapObject


class TestRayCollision(unittest.TestCase):
    def setUp(self):
        self.gameboard = GameBoard(100, 100)
        self.player = Player()
        self.shooter = Shooter()

    def test_calculate_slope(self):
        player = Player()
        player.shooter = Shooter()
        player.shooter.heading = (3 * math.pi) / 4
        expected_slope = -1
        test_slope = calculate_slope(player.shooter.heading)
        self.assertAlmostEqual(expected_slope, test_slope, 2)

    def test_determine_collision_quadrant1(self):
        player = Player()
        player.shooter = Shooter()
        player.shooter.heading = (math.pi / 4)
        player.shooter.hitbox = Hitbox(10, 10, (19, 101))
        gun = Gun(GunType.handgun, 1)
        player.shooter.append_inventory(gun)
        gameboard = GameBoard()
        obj_list = [
            MapObject(hitbox=Hitbox(5, 5, (20, 100))),
            MapObject(hitbox=Hitbox(5, 5, (100, 20))),
            MapObject(hitbox=Hitbox(5, 5, (200, 100))),
            MapObject(hitbox=Hitbox(5, 5, (100, 200))),
            MapObject(hitbox=Hitbox(5, 5, (20, 200))),
            MapObject(hitbox=Hitbox(5, 5, (200, 20))),
        ]
        gameboard.partition.add_object_list(obj_list)
        gameboard.partition.add_object(player.shooter)
        ray = get_gun_ray_collision(player, gameboard)
        self.assertEqual(ray.collision, obj_list[0])

    def test_determine_collision_quadrant2(self):
        player = Player()
        player.shooter = Shooter()
        player.shooter.heading = (3 * (math.pi / 4))
        player.shooter.hitbox = Hitbox(10, 10, (21, 101))
        gun = Gun(GunType.handgun, 1)
        player.shooter.append_inventory(gun)
        gameboard = GameBoard()
        obj_list = [
            MapObject(hitbox=Hitbox(5, 5, (20, 100))),
            MapObject(hitbox=Hitbox(5, 5, (100, 20))),
            MapObject(hitbox=Hitbox(5, 5, (200, 100))),
            MapObject(hitbox=Hitbox(5, 5, (100, 200))),
            MapObject(hitbox=Hitbox(5, 5, (20, 200))),
            MapObject(hitbox=Hitbox(5, 5, (200, 20))),
        ]
        gameboard.partition.add_object_list(obj_list)
        gameboard.partition.add_object(player.shooter)
        ray = get_gun_ray_collision(player, gameboard)
        self.assertEqual(ray.collision, obj_list[0])

    def test_determine_collision_quadrant3(self):
        player = Player()
        player.shooter = Shooter()
        player.shooter.heading = (5 * math.pi) / 4
        player.shooter.hitbox = Hitbox(10, 10, (21, 99))
        gun = Gun(GunType.handgun, 1)
        player.shooter.append_inventory(gun)
        gameboard = GameBoard()
        obj_list = [
            MapObject(hitbox=Hitbox(5, 5, (20, 100))),
            MapObject(hitbox=Hitbox(5, 5, (100, 20))),
            MapObject(hitbox=Hitbox(5, 5, (200, 100))),
            MapObject(hitbox=Hitbox(5, 5, (100, 200))),
            MapObject(hitbox=Hitbox(5, 5, (20, 200))),
            MapObject(hitbox=Hitbox(5, 5, (200, 20))),
        ]
        gameboard.partition.add_object_list(obj_list)
        gameboard.partition.add_object(player.shooter)
        ray = get_gun_ray_collision(player, gameboard)
        self.assertEqual(ray.collision, obj_list[0])

    def test_determine_collision_quadrant4(self):
        player = Player()
        player.shooter = Shooter()
        player.shooter.heading = (7 * (math.pi / 4))
        player.shooter.hitbox = Hitbox(10, 10, (19, 99))
        gun = Gun(GunType.handgun, 1)
        player.shooter.append_inventory(gun)
        gameboard = GameBoard()
        obj_list = [
            MapObject(hitbox=Hitbox(5, 5, (20, 100))),
            MapObject(hitbox=Hitbox(5, 5, (100, 20))),
            MapObject(hitbox=Hitbox(5, 5, (200, 100))),
            MapObject(hitbox=Hitbox(5, 5, (100, 200))),
            MapObject(hitbox=Hitbox(5, 5, (20, 200))),
            MapObject(hitbox=Hitbox(5, 5, (200, 20))),
        ]
        gameboard.partition.add_object_list(obj_list)
        gameboard.partition.add_object(player.shooter)
        ray = get_gun_ray_collision(player, gameboard)
        self.assertEqual(ray.collision, obj_list[0])

    def test_miss_collision(self):
        player = Player()
        player.shooter = Shooter()
        player.shooter.heading = 7 * math.pi / 4
        player.shooter.hitbox = Hitbox(10, 10, (0, 2))
        gun = Gun(GunType.handgun, 1)
        player.shooter.append_inventory(gun)
        gameboard = GameBoard()
        obj_list = [
            MapObject(hitbox=Hitbox(5, 5, (20, 100))),
            MapObject(hitbox=Hitbox(5, 5, (100, 20))),
            MapObject(hitbox=Hitbox(5, 5, (200, 100))),
            MapObject(hitbox=Hitbox(5, 5, (100, 200))),
            MapObject(hitbox=Hitbox(5, 5, (20, 200))),
            MapObject(hitbox=Hitbox(5, 5, (200, 20))),
        ]
        gameboard.partition.add_object_list(obj_list)
        gameboard.partition.add_object(player.shooter)
        ray = get_gun_ray_collision(player, gameboard)
        self.assertAlmostEqual(ray.endpoint[0], 26.87, 2)
        self.assertAlmostEqual(ray.endpoint[1], 28.87, 2)

    def test_miss_collision2(self):
        player = Player()
        player.shooter = Shooter()
        player.shooter.heading = math.pi / 4
        player.shooter.hitbox = Hitbox(10, 10, (0, 2))
        gun = Gun(GunType.handgun, 1)
        player.shooter.append_inventory(gun)
        gameboard = GameBoard()
        obj_list = [
            MapObject(hitbox=Hitbox(5, 5, (20, 100))),
            MapObject(hitbox=Hitbox(5, 5, (100, 20))),
            MapObject(hitbox=Hitbox(5, 5, (200, 100))),
            MapObject(hitbox=Hitbox(5, 5, (100, 200))),
            MapObject(hitbox=Hitbox(5, 5, (20, 200))),
            MapObject(hitbox=Hitbox(5, 5, (200, 20))),
        ]
        gameboard.partition.add_object_list(obj_list)
        gameboard.partition.add_object(player.shooter)
        ray = get_gun_ray_collision(player, gameboard)
        self.assertAlmostEqual(ray.endpoint[0], 2, 2)
        self.assertEqual(ray.endpoint[1], 0)

    def test_miss_collision3(self):
        player = Player()
        player.shooter = Shooter()
        player.shooter.heading = (math.pi / 4)
        player.shooter.hitbox = Hitbox(10, 10, (0, 2))
        gun = Gun(GunType.handgun, 1)
        player.shooter.append_inventory(gun)
        gameboard = GameBoard()
        obj_list = [
            MapObject(hitbox=Hitbox(5, 5, (20, 100))),
            MapObject(hitbox=Hitbox(5, 5, (100, 20))),
            MapObject(hitbox=Hitbox(5, 5, (200, 100))),
            MapObject(hitbox=Hitbox(5, 5, (100, 200))),
            MapObject(hitbox=Hitbox(5, 5, (20, 200))),
            MapObject(hitbox=Hitbox(5, 5, (200, 20))),
        ]
        gameboard.partition.add_object_list(obj_list)
        gameboard.partition.add_object(player.shooter)
        ray = get_gun_ray_collision(player, gameboard)
        self.assertAlmostEqual(ray.endpoint[0], 2, 2)
        self.assertEqual(ray.endpoint[1], 0, 2)

    def test_vertical_slope1(self):
        player = Player()
        player.shooter = Shooter()
        player.shooter.heading = (3 * math.pi) / 2
        player.shooter.hitbox = Hitbox(10, 10, (0, 2))
        gun = Gun(GunType.handgun, 1)
        player.shooter.append_inventory(gun)
        gameboard = GameBoard()
        obj_list = [
            MapObject(hitbox=Hitbox(5, 5, (20, 100))),
            MapObject(hitbox=Hitbox(5, 5, (100, 20))),
            MapObject(hitbox=Hitbox(5, 5, (200, 100))),
            MapObject(hitbox=Hitbox(5, 5, (100, 200))),
            MapObject(hitbox=Hitbox(5, 5, (20, 200))),
            MapObject(hitbox=Hitbox(5, 5, (200, 20))),
        ]
        gameboard.partition.add_object_list(obj_list)
        gameboard.partition.add_object(player.shooter)
        ray = get_gun_ray_collision(player, gameboard)
        self.assertEqual(ray.endpoint[0], 0)
        self.assertEqual(ray.endpoint[1], 40)

    def test_vertical_slope2(self):
        player = Player()
        player.shooter = Shooter()
        player.shooter.heading = math.pi / 2
        player.shooter.hitbox = Hitbox(10, 10, (0, 50))
        gun = Gun(GunType.handgun, 1)
        player.shooter.append_inventory(gun)
        gameboard = GameBoard()
        obj_list = [
            MapObject(hitbox=Hitbox(5, 5, (20, 100))),
            MapObject(hitbox=Hitbox(5, 5, (100, 20))),
            MapObject(hitbox=Hitbox(5, 5, (200, 100))),
            MapObject(hitbox=Hitbox(5, 5, (100, 200))),
            MapObject(hitbox=Hitbox(5, 5, (20, 200))),
            MapObject(hitbox=Hitbox(5, 5, (200, 20))),
        ]
        gameboard.partition.add_object_list(obj_list)
        gameboard.partition.add_object(player.shooter)
        ray = get_gun_ray_collision(player, gameboard)
        self.assertEqual(ray.endpoint[0], 0)
        self.assertEqual(ray.endpoint[1], 12)

    def test_vertical_slope3(self):
        player = Player()
        player.shooter = Shooter()
        player.shooter.heading = math.pi / 2
        player.shooter.hitbox = Hitbox(10, 10, (20, 120))
        gun = Gun(GunType.handgun, 1)
        player.shooter.append_inventory(gun)
        gameboard = GameBoard()
        obj_list = [
            MapObject(hitbox=Hitbox(5, 5, (20, 100))),
            MapObject(hitbox=Hitbox(5, 5, (100, 20))),
            MapObject(hitbox=Hitbox(5, 5, (200, 100))),
            MapObject(hitbox=Hitbox(5, 5, (100, 200))),
            MapObject(hitbox=Hitbox(5, 5, (20, 200))),
            MapObject(hitbox=Hitbox(5, 5, (200, 20))),
        ]
        gameboard.partition.add_object_list(obj_list)
        gameboard.partition.add_object(player.shooter)
        ray = get_gun_ray_collision(player, gameboard)
        self.assertEqual(ray.collision, obj_list[0])
        self.assertEqual(ray.endpoint[0], 20)
        self.assertEqual(ray.endpoint[1], 105)

    def test_horizontal_slope1(self):
        player = Player()
        player.shooter = Shooter()
        player.shooter.heading = (0)
        player.shooter.hitbox = Hitbox(10, 10, (15, 100))
        gun = Gun(GunType.handgun, 1)
        player.shooter.append_inventory(gun)
        gameboard = GameBoard()
        obj_list = [
            MapObject(hitbox=Hitbox(5, 5, (20, 100))),
            MapObject(hitbox=Hitbox(5, 5, (100, 20))),
            MapObject(hitbox=Hitbox(5, 5, (200, 100))),
            MapObject(hitbox=Hitbox(5, 5, (100, 200))),
            MapObject(hitbox=Hitbox(5, 5, (20, 200))),
            MapObject(hitbox=Hitbox(5, 5, (200, 20))),
        ]
        gameboard.partition.add_object_list(obj_list)
        gameboard.partition.add_object(player.shooter)
        ray = get_gun_ray_collision(player, gameboard)
        self.assertEqual(ray.endpoint[0], 20)
        self.assertEqual(ray.endpoint[1], 100)
        self.assertEqual(ray.collision, obj_list[0])

    def test_horizontal_slope2(self):
        player = Player()
        player.shooter = Shooter()
        player.shooter.heading = (0)
        player.shooter.hitbox = Hitbox(10, 10, (15, 100))
        gun = Gun(1, 1)
        player.shooter.append_inventory(gun)
        gameboard = GameBoard()
        obj_list = [
            MapObject(hitbox=Hitbox(5, 5, (20, 102))),
            MapObject(hitbox=Hitbox(5, 5, (100, 20))),
            MapObject(hitbox=Hitbox(5, 5, (200, 100))),
            MapObject(hitbox=Hitbox(5, 5, (100, 200))),
            MapObject(hitbox=Hitbox(5, 5, (20, 200))),
            MapObject(hitbox=Hitbox(5, 5, (200, 20))),
        ]
        gameboard.partition.add_object_list(obj_list)
        gameboard.partition.add_object(player.shooter)
        ray = get_gun_ray_collision(player, gameboard)
        self.assertEqual(ray.endpoint[0], 20)
        self.assertEqual(ray.endpoint[1], 100)
        self.assertEqual(ray.collision, obj_list[0])


if __name__ == '__main__':
    unittest.main
