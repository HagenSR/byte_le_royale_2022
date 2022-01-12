import unittest

from game.common.action import Action
from game.common.door import Door
from game.common.game_board import GameBoard
from game.common.hitbox import Hitbox
from game.common.items.upgrade import Upgrade
from game.common.moving.shooter import Shooter
from game.common.player import Player
from game.common.stats import GameStats
from game.controllers.interact_controller import InteractController
from game.common.enums import *
from game.common.items.money import Money


class TestInteractController(unittest.TestCase):
    def setUp(self):
        self.myPlayer = Player(
            shooter=Shooter(
                0, 0, Hitbox(
                    10, 10, (10, 10), 0)))
        self.myPlayer.action._chosen_action = ActionType.interact
        self.interactController = InteractController()
        self.world_data = {'game_board': GameBoard()}

    # def test_interact_object_valid(self):

    def test_interact_door_too_far(self):
        self.myPlayer.shooter.hitbox.position = (50, 50)
        door_object = Door(Hitbox(3, 10, (80, 50)))
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        # self.world_data["game_board"].partition.add_object(
        # door_object)
        self.assertRaises(ValueError,
                          self.interactController.handle_actions,
                          self.myPlayer, self.world_data)

        self.myPlayer = Player(shooter=Shooter(
            0, 0, Hitbox(
                10, 10, (10, 10), 0)))
        self.myPlayer.action._chosen_action = ActionType.interact
        self.interactController = InteractController()
        self.world_data = {'game_board': GameBoard()}

    # testing controller when no objects/doors are present
    def test_interact_object_invalid(self):
        self.myPlayer.shooter.hitbox.position = (50, 50)
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.assertRaises(ValueError,
                          self.interactController.handle_actions,
                          self.myPlayer, self.world_data)

    # interacting with upgrade beneath player
    def test_pickup_upgrade(self):
        an_item = Upgrade(Hitbox(
            10, 10, (45, 50), 0))
        for slot in self.myPlayer.shooter.inventory['upgrades']:
            self.myPlayer.shooter.append_inventory(an_item)
        self.myPlayer.shooter.remove_from_inventory(an_item)
        self.myPlayer.shooter.hitbox.position = (50, 50)
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.world_data["game_board"].partition.add_object(
            an_item)
        self.interactController.handle_actions(self.myPlayer, self.world_data)
        self.assertFalse(self.myPlayer.shooter.has_empty_slot('upgrades'))

    # interacting with money beneath player
    def test_pickup_money(self):
        self.myPlayer.shooter.money = 150
        old_money = self.myPlayer.shooter.money
        money_object = Money(Hitbox(10, 10, (10, 10), 0))
        self.world_data["game_board"].partition.add_object(
            money_object)
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.interactController.handle_actions(self.myPlayer, self.world_data)
        self.assertTrue(self.myPlayer.shooter.money, (old_money + money_object.amount))

    # attempting to interact with door out of range
    def test_interact_door_too_far(self):
        self.myPlayer.shooter.hitbox.position = (50, 50)
        door_object = Door(Hitbox(3, 10, (80, 50)))
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.world_data["game_board"].partition.add_object(
            door_object)
        self.assertRaises(ValueError,
                          self.interactController.handle_actions,
                          self.myPlayer, self.world_data)

    # standing beside door left side
    def test_beside_open_door_1(self):
        self.myPlayer.shooter.hitbox.position = (50, 50)
        door_object = Door(Hitbox(3, 10, (61, 50)))
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.world_data["game_board"].partition.add_object(
            door_object)
        self.interactController.handle_actions(self.myPlayer, self.world_data)
        self.assertTrue(door_object.open_state)

    # standing beside door right side
    def test_beside_open_door_2(self):
        self.myPlayer.shooter.hitbox.position = (50, 50)
        door_object = Door(Hitbox(3, 10, (49, 50)))
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.world_data["game_board"].partition.add_object(
            door_object)
        self.interactController.handle_actions(self.myPlayer, self.world_data)
        self.assertTrue(door_object.open_state)

    # standing beside door top
    def test_beside_open_door_3(self):
        self.myPlayer.shooter.hitbox.position = (50, 50)
        door_object = Door(Hitbox(10, 3, (50, 46)))
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.world_data["game_board"].partition.add_object(
            door_object)
        self.interactController.handle_actions(self.myPlayer, self.world_data)
        self.assertTrue(door_object.open_state)

    # standing beside door bottom
    def test_beside_open_door_4(self):
        self.myPlayer.shooter.hitbox.position = (50, 50)
        door_object = Door(Hitbox(10, 3, (50, 61)))
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.world_data["game_board"].partition.add_object(
            door_object)
        self.interactController.handle_actions(self.myPlayer, self.world_data)
        self.assertTrue(door_object.open_state)

    # two doors within range, should detect both doors but only open door 1
    def test_correct_door_opened_1(self):
        self.myPlayer.shooter.hitbox.position = (50, 50)
        door_object_1 = Door(Hitbox(3, 10, (61, 50)))  # is closest door
        door_object_2 = Door(Hitbox(10, 3, (50, 62)))
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.world_data["game_board"].partition.add_object(
            door_object_1)
        self.world_data["game_board"].partition.add_object(
            door_object_2)
        self.interactController.handle_actions(self.myPlayer, self.world_data)
        self.assertTrue(door_object_1.open_state)
        self.assertFalse(door_object_2.open_state)

    # three doors within range, should detect all doors but only open door 3
    def test_correct_door_opened_2(self):
        self.myPlayer.shooter.hitbox.position = (70, 75)
        door_object_1 = Door(Hitbox(3, 10, (83, 75))) # is closest door
        door_object_2 = Door(Hitbox(10, 3, (70, 89)))
        door_object_3 = Door(Hitbox(10, 3, (70, 70)))
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.world_data["game_board"].partition.add_object(
            door_object_1)
        self.world_data["game_board"].partition.add_object(
            door_object_2)
        self.world_data["game_board"].partition.add_object(
            door_object_3)
        self.interactController.handle_actions(self.myPlayer, self.world_data)
        self.assertTrue(door_object_1.open_state)
        self.assertFalse(door_object_2.open_state)
        self.assertFalse(door_object_3.open_state)

    # two doors within range, should detect both doors but only open door 2
    def test_correct_door_opened_3(self):
        self.myPlayer.shooter.hitbox.position = (30, 30)
        door_object_1 = Door(Hitbox(3, 10, (44, 30)))
        door_object_2 = Door(Hitbox(3, 10, (26, 30)))  # is closest door
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.world_data["game_board"].partition.add_object(
            door_object_1)
        self.world_data["game_board"].partition.add_object(
            door_object_2)
        self.interactController.handle_actions(self.myPlayer, self.world_data)
        self.assertFalse(door_object_1.open_state)
        self.assertTrue(door_object_2.open_state)

    # testing max distance in the down direction
    def test_door_max_dist_1(self):
        self.myPlayer.shooter.hitbox.position = (50, 50)
        door_object = Door(Hitbox(10, 3, (50, self.myPlayer.shooter.hitbox.middle[1] +
                                          GameStats.max_allowed_dist_from_door)))
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.world_data["game_board"].partition.add_object(
            door_object)
        self.interactController.handle_actions(self.myPlayer, self.world_data)
        self.assertTrue(door_object.open_state)

    # testing max distance to the right
    def test_door_max_dist_2(self):
        self.myPlayer.shooter.hitbox.position = (50, 50)
        door_object = Door(Hitbox(3, 10, (self.myPlayer.shooter.hitbox.middle[0] +
                                          GameStats.max_allowed_dist_from_door, 50)))
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.world_data["game_board"].partition.add_object(
            door_object)
        self.interactController.handle_actions(self.myPlayer, self.world_data)
        self.assertTrue(door_object.open_state)

    # testing max distance in the up direction
    def test_door_max_dist_3(self):
        self.myPlayer.shooter.hitbox.position = (50, 50)
        door_object = Door(Hitbox(10, 3, (50, self.myPlayer.shooter.hitbox.middle[1] -
                                          GameStats.max_allowed_dist_from_door)))
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.world_data["game_board"].partition.add_object(
            door_object)
        self.interactController.handle_actions(self.myPlayer, self.world_data)
        self.assertTrue(door_object.open_state)

    # testing max distance in the left direction
    def test_door_max_dist_4(self):
        self.myPlayer.shooter.hitbox.position = (50, 50)
        door_object = Door(Hitbox(3, 10, (self.myPlayer.shooter.hitbox.middle[0] -
                                          GameStats.max_allowed_dist_from_door, 50)))
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.world_data["game_board"].partition.add_object(
            door_object)
        self.interactController.handle_actions(self.myPlayer, self.world_data)
        self.assertTrue(door_object.open_state)

    if __name__ == '__main__':
        unittest.main
