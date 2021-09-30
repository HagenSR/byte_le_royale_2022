import unittest
from game.controllers.loot_generation_controller import LootGenerationController
from game.common.game_board import GameBoard
from game.common.stats import GameStats
from game.common.hitbox import Hitbox


class TestLootGenerationController(unittest.TestCase):

    def setUp(self):
        self.loot_gen_controller = LootGenerationController()

    def test_places_loot(self):
        kill_boundary_radius = 499
        self.loot_gen_controller.handle_actions(GameBoard(), kill_boundary_radius)
        self.assertTrue((GameStats.gun_count +
                         GameStats.consumable_count +
                         GameStats.upgrade_count +
                         GameStats.money_count > 0))

    def test_does_not_place_loot(self):
        # radius too small to place loot
        kill_boundary_radius = 1
        self.loot_gen_controller.handle_actions(GameBoard(), kill_boundary_radius)
        self.assertFalse((GameStats.gun_count +
                         GameStats.consumable_count +
                         GameStats.upgrade_count +
                         GameStats.money_count > 0))


if __name__ == '__main__':
    unittest.main()
