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

    # Tests that shop controller inventory is updated after item purchase
    def test_shop_inventory_update(self):
        self.myPlayer.shooter.money = GameStats.shop_stats[Consumables.shield]["cost"]
        self.myPlayer.action.item_to_purchase = Consumables.shield
        # before purchase, shop inventory for armor_pack will be 5
        self.shopController.handle_actions(self.myPlayer)
        # This assertion statement should prove that the item stock has gone
        # down by one after the purchase
        self.assertEqual(
            self.shopController.shop_inventory[self.myPlayer.action.item_to_purchase]["quantity"], 4)

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

    # Tests to make sure error is thrown if player has insufficient funds for
    # item
    def test_user_cost_error(self):
        self.myPlayer.shooter.money = 0
        self.myPlayer.action.item_to_purchase = Consumables.shield
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
