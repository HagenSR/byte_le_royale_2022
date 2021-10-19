import unittest
from game.controllers.loot_generation_controller import LootGenerationController
from game.common.game_board import GameBoard
from game.common.stats import GameStats
from game.common.hitbox import Hitbox


class TestLootGenerationController(unittest.TestCase):

    def test_places_loot(self):
        loot_gen_controller = LootGenerationController()
        game_board = GameBoard()
        loot_gen_controller.handle_actions(game_board)
        num_items = 0
        # get number of objects in each partition
        for x in range(0,GameStats.game_board_width, game_board.partition.partition_width):
            for y in range(0, GameStats.game_board_height, game_board.partition.partition_height):
                for object in game_board.partition.get_partition_objects(x, y):
                    num_items += 1
        self.assertTrue(num_items > 0)

    def test_does_not_place_loot(self):
        loot_gen_controller = LootGenerationController()
        loot_gen_controller.tick = 200
        # circle should be too small to spawn items
        game_board = GameBoard()
        game_board.circle_radius = 4
        loot_gen_controller.handle_actions(game_board)
        num_items = 0
        for x in range(0,500,25):
            for y in range(0,500,25):
                for object in game_board.partition.get_partition_objects(x, y):
                    num_items += 1
        self.assertEqual(num_items, 0)


if __name__ == '__main__':
    unittest.main()
