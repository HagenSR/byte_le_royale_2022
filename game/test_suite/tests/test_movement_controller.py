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
        self.world_data["game_board"].partition.add_object(self.myPlayer.shooter)

    def test_updated_location(self):
        self.myPlayer.shooter.speed = 50
        self.myPlayer.shooter.heading = 0.34
        location = self.myPlayer.shooter.hitbox.position
        speed = self.myPlayer.shooter.speed
        angle = self.myPlayer.shooter.heading
        target_location = calculate_location(location, speed, angle)
        self.movementController.handle_actions(self.myPlayer, self.world_data)
        self.assertEqual(self.myPlayer,
                         self.movementController.current_world_data["game_map"].partition.get_partition_objects(
                             target_location[0], target_location[1]))

    def test_edge_of_map_invalid(self):
        self.myPlayer.shooter.speed = 50
        self.myPlayer.shooter.heading = 0.34
        self.myPlayer.shooter.hitbox.position = (500, 500)
        location = self.myPlayer.shooter.hitbox.position
        speed = self.myPlayer.shooter.speed
        angle = self.myPlayer.shooter.heading
        target_location = calculate_location(location, speed, angle)
        self.movementController.handle_actions(self.myPlayer, self.world_data)
        self.assertRaises(Exception, self.setPosition, target_location)

    def setPosition(self, new_pos):
        self.myPlayer.shooter.hitbox.position = new_pos

    def setHeading(self, new_hd):
        self.myPlayer.shooter.speed = new_hd

    def setSpeed(self, new_spd):
        self.myPlayer.shooter.heading = new_spd


if __name__ == '__main__':
    unittest.main
