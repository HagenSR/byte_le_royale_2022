import unittest

from game.common.action import Action
from game.common.game_board import GameBoard
from game.common.hitbox import Hitbox
from game.common.moving.shooter import Shooter
from game.common.player import Player
from game.controllers.interact_controller import InteractController
from game.common.enums import *
from game.common.items.money import Money


class TestInteractController(unittest.TestCase):
    def setUp(self):
        act = Action()
        act.set_action(ActionType.interact)
        self.myPlayer = Player(
            action=act, shooter=Shooter(
                0, 0, Hitbox(
                    10, 10, (10, 10))))
        self.interactController = InteractController()
        self.world_data = {'game_board': GameBoard()}

    # def test_interact_object_valid(self):

    # def test_interact_object_invalid(self):

    # def test_interact_door(self):

    # def test_pickup_upgrade(self):

   # def test_pickup_money(self):
       # self.myPlayer.shooter.money = 150
       # old_money = self.myPlayer.shooter.money
       # print(old_money)
       # money_object = Money(Hitbox(10, 10, (10, 10), health=10, count=1))
       # self.world_data["game_board"].partition.add_object(
            #money_object)
       # print(money_object.amount)
        #self.interactController.handle_actions(self.myPlayer, self.world_data)
        #self.assertTrue(self.myPlayer.shooter.money, (old_money + money_object.amount))

    if __name__ == '__main__':
        unittest.main
