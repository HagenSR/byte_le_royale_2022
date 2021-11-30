import unittest

from game.common.action import Action
from game.common.enums import ActionType, Consumables
from game.common.game_board import GameBoard
from game.common.hitbox import Hitbox
from game.common.items.consumable import Consumable
from game.common.moving.shooter import Shooter
from game.common.player import Player
from game.common.stats import GameStats
from game.controllers.movement_controller import MovementController
from game.utils.calculate_new_location import calculate_location
from game.common.wall import Wall


class TestMovementController(unittest.TestCase):

    def setUp(self):
        act = Action()
        act.set_action(ActionType.move)
        self.myPlayer = Player(
            action=act, shooter=Shooter(
                0, 0, Hitbox(
                    10, 10, (10, 10), 0)))
        self.movementController = MovementController()
        self.world_data = {'game_board': GameBoard()}

    def test_updated_location(self):
        print("testing location")
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.myPlayer.shooter.speed = 10
        self.myPlayer.shooter.heading = 0.34
        location = self.myPlayer.shooter.hitbox.position
        speed = self.myPlayer.shooter.speed
        angle = self.myPlayer.shooter.heading
        target_location = calculate_location(location, speed, angle)
        self.movementController.handle_actions(self.myPlayer, self.world_data)
        x_val = self.myPlayer.shooter.hitbox.position[0]
        y_val = self.myPlayer.shooter.hitbox.position[1]
        self.assertTrue(target_location, self.myPlayer.shooter.hitbox.position)

    def test_player_removed(self):
        print("testing removed")
        self.myPlayer.shooter.hitbox.position = (10, 10)
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.myPlayer.shooter.speed = 10
        self.myPlayer.shooter.heading = 0.34
        location = self.myPlayer.shooter.hitbox.position
        speed = self.myPlayer.shooter.speed
        angle = self.myPlayer.shooter.heading
        self.movementController.handle_actions(self.myPlayer, self.world_data)
        self.assertFalse(
            self.world_data["game_board"].partition.find_object_coordinates(
                10, 10))

    # def test_edge_of_map_invalid(self):
    #     print("testing edge of map")
    #     self.myPlayer.shooter.hitbox.position = (500, 500)
    #     self.world_data["game_board"].partition.add_object(
    #         self.myPlayer.shooter)
    #     self.myPlayer.shooter.speed = 50
    #     self.myPlayer.shooter.heading = 0.34
    #     self.assertRaises(
    #         ValueError,
    #         self.movementController.handle_actions,
    #         self.myPlayer,
    #         self.world_data)

    def test_max_distance_error(self):
        self.myPlayer.shooter.hitbox.position = (10, 10)
        self.myPlayer.shooter.speed = GameStats.player_stats["max_distance_per_turn"] + 1
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.assertRaises(Exception, self.movementController.handle_actions,
                          self.myPlayer,
                          self.world_data)

    def test_walk_over_item(self):
        print("testing walk over item")
        self.myPlayer.shooter.hitbox.position = (50, 50)
        an_item = Consumable(
            hitbox=Hitbox(
                10,
                10,
                (55,
                 50),
                0),
            health=None,
            count=None,
            consumable_enum=Consumables.speed_boost)
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.world_data["game_board"].partition.add_object(an_item)
        self.myPlayer.shooter.speed = 50
        self.myPlayer.shooter.heading = 0
        location = self.myPlayer.shooter.hitbox.position
        speed = self.myPlayer.shooter.speed
        angle = self.myPlayer.shooter.heading
        target_location = calculate_location(location, speed, angle)
        self.movementController.handle_actions(self.myPlayer, self.world_data)
        self.assertTrue(target_location, self.myPlayer.shooter.hitbox.position)

    def test_object_in_path_head_on(self):
        print("testing object path")
        self.myPlayer.shooter.hitbox.position = (50, 50)
        wall_object = Wall(health=21, hitbox=Hitbox(10, 10, (70, 50), 0))
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.world_data["game_board"].partition.add_object(wall_object)
        # self.myPlayer.shooter.speed = 50
        # self.myPlayer.shooter.heading = 0
        self.myPlayer.shooter.move(0, 50)
        self.movementController.handle_actions(self.myPlayer, self.world_data)
        self.assertFalse(self.movementController.space_free)

    # player moves straight line past object that is also level to x axis, no
    # collision should occur
    def test_passing_object_no_angle_pass(self):
        print("testing object no angle pass")
        self.myPlayer.shooter.hitbox.position = (50, 50)
        # self.myPlayer.shooter.heading = 90
        # self.myPlayer.shooter.hitbox.rotation = 90
        # self.myPlayer.shooter.speed = 50
        self.myPlayer.shooter.move(90, 50)
        print(self.myPlayer.shooter.heading)
        print(self.myPlayer.shooter.hitbox.rotation)
        # print(self.myPlayer.shooter.hitbox.topRight)
        # self.myPlayer.shooter.hitbox.rotation = 90
        wall_object = Wall(health=21, hitbox=Hitbox(5, 5, (70, 70), 0))
        # print(wall_object.hitbox.topRight)
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.world_data["game_board"].partition.add_object(wall_object)

        # self.myPlayer.shooter.heading = 90

        self.movementController.handle_actions(self.myPlayer, self.world_data)
        self.assertTrue(self.movementController.space_free)

    # player attempts to brush by object that is level to x axis, will be
    # stopped by object
    def test_passing_object_no_angle_fail(self):
        print("testing object no angle pass")
        self.myPlayer.shooter.hitbox.position = (50, 50)
        wall_object = Wall(health=21, hitbox=Hitbox(5, 5, (50, 70), 0))
        self.myPlayer.shooter.move(90, 50)
        # self.myPlayer.shooter.hitbox.rotation = 0
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.world_data["game_board"].partition.add_object(wall_object)
        # self.myPlayer.shooter.speed = 50
        # self.myPlayer.shooter.heading = .5
        print(self.myPlayer.shooter.heading)
        print(self.myPlayer.shooter.hitbox.rotation)
        self.movementController.handle_actions(self.myPlayer, self.world_data)
        self.assertFalse(self.movementController.space_free)

    # player moves straight line past object that is at an angle, they should
    # not collide.
    def test_passing_object_angle_pass(self):
        print("testing object angle pass")
        self.myPlayer.shooter.hitbox.position = (50, 50)
        self.myPlayer.shooter.move(90, 50)
        wall_object = Wall(health=21, hitbox=Hitbox(5, 5, (60, 70), 290))
        print(wall_object.hitbox.top_left)
        print(wall_object.hitbox.top_right)
        print(wall_object.hitbox.bottom_left)
        print(wall_object.hitbox.bottom_right)
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.world_data["game_board"].partition.add_object(wall_object)
        self.movementController.handle_actions(self.myPlayer, self.world_data)
        self.assertTrue(self.movementController.space_free)

    # player moves straight line past object that is at an angle, they should
    # be stopped from colliding
    def test_passing_object_angle_fail(self):
        print("testing object no angle pass")
        self.myPlayer.shooter.hitbox.position = (50, 50)
        self.myPlayer.shooter.move(90, 50)
        wall_object = Wall(health=21, hitbox=Hitbox(10, 10, (60, 50), 70))
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.world_data["game_board"].partition.add_object(wall_object)
        self.movementController.handle_actions(self.myPlayer, self.world_data)
        self.assertFalse(self.movementController.space_free)

    # player attempts to collide with object at an angle. They will stop before collision.
    # def player_angle_object_collide(self):

    # both player and object are at an angle, the player will top before colliding.
    # def both_angle_collision(self):

    def setPosition(self, new_pos):
        self.myPlayer.shooter.hitbox.position = new_pos

    def setHeading(self, new_hd):
        self.myPlayer.shooter.speed = new_hd

    def setSpeed(self, new_spd):
        self.myPlayer.shooter.heading = new_spd


if __name__ == '__main__':
    unittest.main
