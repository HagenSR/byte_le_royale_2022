import unittest
from game.common.stats import GameStats
from game.controllers.loot_generation_controller import LootGenerationController
from game.common.items.consumable import Consumable
from game.common.wall import Wall
from game.common.hitbox import Hitbox
from game.utils.item_gen_utils import *
import random


class TestItemGenerationUtil(unittest.TestCase):

    def test_has_reached_item_cap(self):
        item_gen_utils = ItemGenUtils()
        item_gen_utils.upgrade_count = 500
        self.assertTrue(
            item_gen_utils.has_reached_item_cap(ObjectType.upgrade))

    def test_pick_item(self):
        item_gen_utils = ItemGenUtils()
        item = item_gen_utils.pick_item(50, 50, 1)
        self.assertTrue(
            item is ObjectType.consumable or ObjectType.upgrade or ObjectType.gun or ObjectType.money)

    def test_place_item(self):
        item_gen_utils = ItemGenUtils()
        game_board = GameBoard()

        # Set seed so it always appears in same random gausian position
        random.seed(42)
        big_boi_wall = Wall(Hitbox(250, 250, (game_board.center[0], game_board.center[1])), 10, False)
        game_board.partition.add_object(big_boi_wall)
        item = item_gen_utils.place_item(game_board, loot_wave_num=1)
        self.assertFalse(game_board.partition.find_object_hitbox(item.hitbox))


if __name__ == '__main__':
    unittest.main()
