import unittest

from game.common.action import Action
from game.common.enums import ActionType, GunType, GunLevel
from game.common.game_board import GameBoard
from game.common.hitbox import Hitbox
from game.common.items.gun import Gun
from game.common.map_object import MapObject
from game.common.moving.shooter import Shooter
from game.common.player import Player
from game.controllers.movement_controller import MovementController
from game.utils.partition_grid import PartitionGrid
from game.utils.calculate_new_location import calculate_location
from game.common.wall import Wall


class TestMovementController(unittest.TestCase):

    def setUp(self):
        act = Action()
        act.set_action(ActionType.move)
        self.myPlayer = Player(
            action=act, shooter=Shooter(
                0, 0, Hitbox(
                    10, 10, (10, 10))))
        self.movementController = MovementController()
        self.world_data = {'game_board': GameBoard()}

    def test_updated_location(self):
        print("testing location")
        self.world_data["game_board"].partition.add_object(self.myPlayer.shooter)
        self.myPlayer.shooter.speed = 10
        self.myPlayer.shooter.heading = 0.34
        location = self.myPlayer.shooter.hitbox.position
        # print(location)
        speed = self.myPlayer.shooter.speed
        angle = self.myPlayer.shooter.heading
        target_location = calculate_location(location, speed, angle)
        # print(target_location)
        self.movementController.handle_actions(self.myPlayer, self.world_data)
        x_val = self.myPlayer.shooter.hitbox.position[0]
        y_val = self.myPlayer.shooter.hitbox.position[1]
        self.assertTrue(self.world_data["game_board"].partition.find_object_coordinates(x_val, y_val))

    def test_player_removed(self):
        print("testing removed")
        self.myPlayer.shooter.hitbox.position = (0, 0)
        self.world_data["game_board"].partition.add_object(self.myPlayer.shooter)
        self.myPlayer.shooter.speed = 10
        self.myPlayer.shooter.heading = 0.34
        location = self.myPlayer.shooter.hitbox.position
        speed = self.myPlayer.shooter.speed
        angle = self.myPlayer.shooter.heading
        target_location = calculate_location(location, speed, angle)
        self.movementController.handle_actions(self.myPlayer, self.world_data)
        self.assertFalse(self.world_data["game_board"].partition.find_object_coordinates(0, 0))

    def test_edge_of_map_invalid(self):
        print("testing edge of map")
        self.myPlayer.shooter.hitbox.position = (500, 500)
        self.world_data["game_board"].partition.add_object(self.myPlayer.shooter)
        self.myPlayer.shooter.speed = 50
        self.myPlayer.shooter.heading = 0.34
        location = self.myPlayer.shooter.hitbox.position
        speed = self.myPlayer.shooter.speed
        angle = self.myPlayer.shooter.heading
        self.assertRaises(ValueError, self.movementController.handle_actions, self.myPlayer, self.world_data)

    def test_object_in_path(self):
        print("testing object path")
        self.myPlayer.shooter.hitbox.position = (50, 50)
        wall_object = Wall(hitbox=Hitbox(10, 10, (55, 50)))
        self.world_data["game_board"].partition.add_object(self.myPlayer.shooter)
        self.world_data["game_board"].partition.add_object(wall_object)
        self.myPlayer.shooter.speed = 50
        self.myPlayer.shooter.heading = 1.5707
        location = self.myPlayer.shooter.hitbox.position
        speed = self.myPlayer.shooter.speed
        angle = self.myPlayer.shooter.heading
        self.movementController.handle_actions(self.myPlayer, self.world_data)
        self.assertFalse(self.movementController.space_free)

    def setPosition(self, new_pos):
        self.myPlayer.shooter.hitbox.position = new_pos

    def setHeading(self, new_hd):
        self.myPlayer.shooter.speed = new_hd

    def setSpeed(self, new_spd):
        self.myPlayer.shooter.heading = new_spd


if __name__ == '__main__':
    unittest.main
