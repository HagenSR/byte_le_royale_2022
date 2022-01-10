import unittest

from game.common.action import Action
from game.common.hitbox import Hitbox
from game.common.items.consumable import Consumable
from game.common.moving.shooter import Shooter
from game.common.player import Player
from game.common.stats import GameStats
from game.controllers.shop_controller import ShopController
from game.common.enums import *


class TestShopController(unittest.TestCase):
    def setUp(self):
        self.myPlayer = Player(
            shooter=Shooter(
                0, 0, Hitbox(
                    10, 10, (10, 10))))
        self.myPlayer.action._chosen_action = ActionType.shop
        self.shopController = ShopController()

    # Tests to make sure player cannot buy items if inventory is full
    def test_user_inventory_error(self):
        self.myPlayer.shooter.money = GameStats.shop_stats[Consumables.speed]["cost"]
        self.myPlayer.action.item_to_purchase = Consumables.speed
        an_item = Consumable(hitbox=None, health=None,
                             consumable_enum=Consumables.speed)
        # All consumable slots in player's inventory should be full after the
        # for loop
        items = [an_item, an_item, an_item, an_item]
        for item in items:
            self.myPlayer.shooter.append_inventory(item)

        self.assertRaises(
            ValueError,
            self.shopController.handle_actions,
            self.myPlayer)

    # Tests to make sure item is in player's inventory after the purchase is
    # made
    def test_shop_gives_item(self):
        self.myPlayer.shooter.money = GameStats.shop_stats[Consumables.health_pack]["cost"]
        self.myPlayer.action.item_to_purchase = Consumables.health_pack
        self.shopController.handle_actions(self.myPlayer)
        an_item = Consumable(hitbox=None, health=None,
                             consumable_enum=Consumables.health_pack)
        # When the consumable_enum attributes are being compared, they should be pointing at the same int value in
        # the consumable enum. In this case, they should both contain the value
        # 2, for health_pack
        self.assertTrue(an_item.consumable_type ==
                        self.myPlayer.shooter.inventory["consumables"][0].consumable_type)


if __name__ == '__main__':
    unittest.main
