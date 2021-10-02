import unittest
from game.controllers.loot_generation_controller import LootGenerationController
from game.common.game_board import GameBoard
from game.common.stats import GameStats
from game.common.hitbox import Hitbox


class TestLootGenerationController(unittest.TestCase):

    def test_places_loot(self):
        loot_gen_controller = LootGenerationController()
        loot_gen_controller.handle_actions(GameBoard())
        self.assertTrue((loot_gen_controller.gun_count +
                         loot_gen_controller.consumable_count +
                         loot_gen_controller.upgrade_count +
                         loot_gen_controller.money_count > 0))

    def test_does_not_place_loot(self):
        loot_gen_controller = LootGenerationController()
        loot_gen_controller.tick = 200
        loot_gen_controller.handle_actions(GameBoard())
        self.assertFalse((loot_gen_controller.gun_count +
                         loot_gen_controller.consumable_count +
                         loot_gen_controller.upgrade_count +
                         loot_gen_controller.money_count > 0))


if __name__ == '__main__':
    unittest.main()
