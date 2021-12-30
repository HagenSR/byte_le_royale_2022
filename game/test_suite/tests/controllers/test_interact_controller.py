import unittest

from game.common.action import Action
from game.common.door import Door
from game.common.game_board import GameBoard
from game.common.hitbox import Hitbox
from game.common.items.upgrade import Upgrade
from game.common.moving.shooter import Shooter
from game.common.player import Player
from game.controllers.interact_controller import InteractController
from game.common.enums import *
from game.common.items.money import Money


class TestInteractController(unittest.TestCase):
    def setUp(self):
        act = Action()
        act.set_action(ActionType.interact)
        self.myPlayer = Player(shooter=Shooter(
            0, 0, Hitbox(
                10, 10, (10, 10), 0)))
        self.myPlayer.action._chosen_action = ActionType.interact
        self.interactController = InteractController()
        self.world_data = {'game_board': GameBoard()}

    def test_interact_object_invalid(self):
        self.myPlayer.shooter.hitbox.position = (50, 50)
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.assertRaises(ValueError,
                          self.interactController.handle_actions,
                          self.myPlayer, self.world_data)

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

    # two door near player; two within range, should pick closest door
    def test_correct_door_opened_1(self):
        self.myPlayer.shooter.hitbox.position = (50, 50)
        door_object_1 = Door(Hitbox(3, 10, (61, 50)))  # is within range
        door_object_2 = Door(Hitbox(10, 3, (50, 63)))  # is out of range
        self.world_data["game_board"].partition.add_object(
            self.myPlayer.shooter)
        self.world_data["game_board"].partition.add_object(
            door_object_1)
        self.world_data["game_board"].partition.add_object(
            door_object_1)
        self.interactController.handle_actions(self.myPlayer, self.world_data)
        self.assertTrue(door_object_1.open_state)
        self.assertFalse(door_object_2.open_state)

    if __name__ == '__main__':
        unittest.main
