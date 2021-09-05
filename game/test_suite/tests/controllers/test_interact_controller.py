import unittest

from game.common.action import Action
from game.common.hitbox import Hitbox
from game.common.moving.shooter import Shooter
from game.common.player import Player
from game.common.stats import GameStats
from game.controllers.interact_controller import InteractController
from game.common.enums import *

class TestShopController(unittest.TestCase):
    def setUp(self):
        act = Action()
        act.set_action(ActionType.interact)
        self.myPlayer = Player(
            action=act, shooter=Shooter(
                0, 0, Hitbox(
                    10, 10, (10, 10))))
        self.interactController = InteractController()

    def test_interact_object_valid(self):

    def test_interact_object_invalid(self):

    def test_interact_door(self):

    def test_pickup_upgrade(self):

    def test_pickup_money(self):




 if __name__ == '__main__':
    unittest.main