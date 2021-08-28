import unittest

from game.common.action import Action
from game.common.enums import ActionType
from game.common.hitbox import Hitbox
from game.common.map_object import MapObject
from game.common.moving.shooter import Shooter
from game.common.player import Player
from game.common.stats import GameStats
from game.controllers.shop_controller import ShopController
from game.utils.partition_grid import PartitionGrid
from game.common.enums import *


class TestShopController(unittest.TestCase):
    def setUp(self):
        act = Action()
        act.set_action(ActionType.shop)
        self.myPlayer = Player(
            action=act, shooter=Shooter(
                0, 0, Hitbox(
                    10, 10, (10, 10))))
        self.shopController = ShopController()

    def test_shop_inventory_update(self):
        self.myPlayer.shooter.money = GameStats.shop_stats[Consumables.armor_pack]["cost"]
        self.myPlayer.action.selected_object = Consumables.armor_pack
        self.shopController.handle_actions(self.myPlayer)
        self.assertEqual(self.shopController.shop_inventory[self.myPlayer.action.selected_object]["quantity"], 4)
    # def test_user_inventory_error(self):
    # def test_user_cost_error(self):


if __name__ == '__main__':
    unittest.main
