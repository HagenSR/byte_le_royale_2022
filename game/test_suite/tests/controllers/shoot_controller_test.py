from game.common.hitbox import Hitbox
from game.common.wall import Wall
import math
import unittest
from game.common.enums import *
from game.common.stats import GameStats
from game.controllers.shoot_controller import ShootController
from game.common.game_board import GameBoard
from game.common.wall import Wall
from game.common.moving.shooter import Shooter
from game.common.player import Player
from game.common.door import Door
from game.common.items.gun import Gun


class TestShootController(unittest.TestCase):

    def setUp(self):
        self.shoot_controller = ShootController()
        self.game_board = GameBoard()
        shooter = Shooter(heading=(0), speed=0,
                          hitbox=Hitbox(10, 10, (0, 0)))
        self.gun = Gun(GunType.sniper, level=1, hitbox=Hitbox(2, 2, (0, 0)))
        shooter.append_inventory(self.gun)
        self.player = Player(shooter=shooter)
        self.player.action._chosen_action = ActionType.shoot
        self.game_board.partition.add_object(shooter)

    def test_health_removal_wall(self):
        wall = Wall(Hitbox(30, 30, (20, 0)), destructible=True)
        self.game_board.partition.add_object(wall)
        self.shoot_controller.handle_action(self.player, self.game_board)
        self.assertEqual(
            round(
                wall.health), round(
                (GameStats.default_wall_health - self.gun.damage)))
        self.game_board.partition.remove_object(wall)

    def test_wall_removal(self):
        wall = Wall(Hitbox(30, 30, (20, 0)), destructible=True)
        self.game_board.partition.add_object(wall)
        for i in range(20):
            self.shoot_controller.handle_action(self.player, self.game_board)
        object_list = self.game_board.partition.get_partition_objects(
            20, 0)
        self.assertNotIn(wall, object_list)

    def test_health_removal_door(self):
        door = Door(Hitbox(30, 30, (20, 0)))
        self.game_board.partition.add_object(door)
        self.shoot_controller.handle_action(self.player, self.game_board)
        self.assertEqual(
            round(
                door.health), round(
                (GameStats.default_door_health - self.gun.damage)))
        self.game_board.partition.remove_object(door)

    def test_door_removal(self):
        door = Door(Hitbox(30, 30, (20, 0)))
        self.game_board.partition.add_object(door)
        for i in range(20):
            self.shoot_controller.handle_action(self.player, self.game_board)
        object_list = self.game_board.partition.get_partition_objects(
            20, 0)
        self.assertNotIn(door, object_list)

    def test_health_removal_shooter(self):
        shooter = Shooter(heading=(math.pi / 2), speed=0,
                          hitbox=Hitbox(30, 30, (20, 0)))
        self.game_board.partition.add_object(shooter)
        self.shoot_controller.handle_action(self.player, self.game_board)
        self.assertEqual(
            round(
                shooter.health), round(
                (GameStats.player_stats['starting_health'] - self.gun.damage)))
        self.game_board.partition.remove_object(shooter)

    def test_shooter_removal(self):
        shooter = Shooter(heading=(math.pi / 2), speed=0,
                          hitbox=Hitbox(30, 30, (20, 0)))
        self.game_board.partition.add_object(shooter)
        for i in range(20):
            self.shoot_controller.handle_action(self.player, self.game_board)
        self.assertLessEqual(shooter.health, 0)

    def test_shot_pattern_spread(self):
        self.game_board = GameBoard()
        shooter = Shooter(heading=(0), speed=0,
                          hitbox=Hitbox(10, 10, (0, 0)))
        gun = Gun(GunType.shotgun, level=1, hitbox=Hitbox(2, 2, (0, 0)))
        shooter.append_inventory(gun)
        self.player = Player(shooter=shooter)
        self.player.action._chosen_action = ActionType.shoot
        wall = Wall(Hitbox(30, 30, (2, 0)), destructible=True)
        self.game_board.partition.add_object(wall)
        self.shoot_controller.handle_action(self.player, self.game_board)
        wall = self.game_board.partition.get_partition_objects(2, 0)[0]
        self.assertAlmostEqual(
            wall.health,
            (GameStats.default_wall_health -
             4 *
             round(
                 gun.damage /
                 GameStats.shot_pattern_multi_pellet_count)),
            4)
        self.game_board.partition.remove_object(wall)
        self.assertEqual(len(self.game_board.ray_list), 9)
