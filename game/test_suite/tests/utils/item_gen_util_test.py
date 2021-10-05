import unittest
from game.common.stats import GameStats
from game.controllers.loot_generation_controller import LootGenerationController
from game.common.items.consumable import Consumable
from game.utils.item_gen_utils import *


class TestItemGenerationUtil(unittest.TestCase):
    def test_has_reached_item_cap(self):
        loot_gen_controller = LootGenerationController()
        loot_gen_controller.consumable_count = 6000
        self.assertTrue(
            has_reached_item_cap(
                ObjectType.consumable,
                loot_gen_controller.consumable_count,
                0,
                0,
                0))

    def test_pick_item(self):
        loot_gen_controller = LootGenerationController()
        xPos, yPos = 0, 0
        picked_items = []
        for i in range(100):
            item = pick_item(
                xPos,
                yPos,
                loot_gen_controller.consumable_count,
                loot_gen_controller.upgrade_count,
                loot_gen_controller.gun_count,
                loot_gen_controller.money_count,
                1)
            picked_items.append(item)
        self.assertIn(ObjectType.gun, picked_items)


if __name__ == '__main__':
    unittest.main()
