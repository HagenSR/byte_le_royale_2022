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
        self.myPlayer = Player(
            shooter=Shooter(
                0, 0, Hitbox(
                    10, 10, (10, 10), 0)))
        self.myPlayer.action._chosen_action = ActionType.move
        self.movementController = MovementController()
        self.world_data = {'game_board': GameBoard()}

    def test_updated_location(self):
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.myPlayer.action.set_move(1, 10)
        location = self.myPlayer.shooter.hitbox.position
        speed = self.myPlayer.shooter.speed
        angle = self.myPlayer.shooter.heading
        target_location = calculate_location(location, speed, angle)
        self.movementController.handle_actions(self.myPlayer, self.world_data["game_board"])
        self.assertTrue(target_location, self.myPlayer.shooter.hitbox.position)

    def test_player_removed(self):
        self.myPlayer.shooter.hitbox.position = (10, 10)
        self.world_data["game_board"].partition.add_object(self.myPlayer.shooter)
        self.myPlayer.action.set_move(1, 10)
        self.movementController.handle_actions(self.myPlayer, self.world_data["game_board"])
        self.assertFalse(
            self.world_data["game_board"].partition.find_object_coordinates(
                10, 10))

    def test_walk_over_item(self):
        self.myPlayer.shooter.hitbox.position = (50, 50)
        an_item = Consumable(
            hitbox=Hitbox(
                10,
                10,
                (55,
                 50),
                0),
            health=None,
            consumable_enum=Consumables.speed_boost)
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.world_data["game_board"].partition.add_object(an_item)
        self.myPlayer.action.set_move(0, 50)
        location = self.myPlayer.shooter.hitbox.position
        speed = self.myPlayer.shooter.speed
        angle = self.myPlayer.shooter.heading
        target_location = calculate_location(location, speed, angle)
        self.movementController.handle_actions(self.myPlayer, self.world_data["game_board"])
        self.assertTrue(target_location, self.myPlayer.shooter.hitbox.position)

    def test_object_in_path_head_on(self):
        self.myPlayer.shooter.hitbox.position = (50, 50)
        wall_object = Wall(health=21, hitbox=Hitbox(10, 10, (70, 50), 0))
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.world_data["game_board"].partition.add_object(wall_object)
        self.myPlayer.action.set_move(0, 50)
        self.movementController.handle_actions(self.myPlayer, self.world_data["game_board"])
        self.assertFalse(self.movementController.space_free)

    # player moves straight line past object that is also level to x axis, no
    # collision should occur
    def test_passing_object_no_angle_pass(self):
        self.myPlayer.shooter.hitbox.position = (50, 50)
        self.myPlayer.action.set_move(90, 50)
        wall_object = Wall(health=21, hitbox=Hitbox(5, 5, (70, 70), 0))
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.world_data["game_board"].partition.add_object(wall_object)
        self.movementController.handle_actions(self.myPlayer, self.world_data["game_board"])
        self.assertTrue(self.movementController.space_free)

    # player attempts to brush by object that is level to x axis, will be
    # stopped by object
    def test_passing_object_no_angle_fail(self):
        self.myPlayer.shooter.hitbox.position = (50, 50)
        wall_object = Wall(health=21, hitbox=Hitbox(5, 5, (50, 70), 0))
        self.myPlayer.action.set_move(90, 50)
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.world_data["game_board"].partition.add_object(wall_object)
        self.movementController.handle_actions(self.myPlayer, self.world_data["game_board"])
        self.assertFalse(self.movementController.space_free)

    # player moves straight line past object that is at an angle, they should
    # not collide.
    def test_passing_object_angle_pass(self):
        self.myPlayer.shooter.hitbox.position = (50, 50)
        self.myPlayer.action.set_move(90, 50)
        wall_object = Wall(health=21, hitbox=Hitbox(5, 5, (65, 70), 290))
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.world_data["game_board"].partition.add_object(wall_object)
        self.movementController.handle_actions(self.myPlayer, self.world_data["game_board"])
        self.assertTrue(self.movementController.space_free)

    # player moves straight line past object that is at an angle, they should
    # be stopped from colliding
    def test_passing_object_angle_fail(self):
        self.myPlayer.shooter.hitbox.position = (50, 50)
        self.myPlayer.action.set_move(0, 50)
        wall_object = Wall(health=21, hitbox=Hitbox(10, 10, (60, 50), 70))
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.world_data["game_board"].partition.add_object(wall_object)
        self.movementController.handle_actions(self.myPlayer, self.world_data["game_board"])
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
