from game.common.hitbox import Hitbox
import unittest
from game.common.game_board import GameBoard
from game.common.stats import GameStats
from game.utils.generate_game import findPlotHitboxes, generate
import json


class TestGameBoardGeneration(unittest.TestCase):

    def setUp(self):
        # generate()
        # Based on the most recently generated game map
        with open('./logs/game_map.json') as fl:
            self.gameboard = GameBoard(10, 10)
            self.gameboard.from_json(json.load(fl)['game_map'])

    def test_init(self):
        self.assertIsNotNone(self.gameboard)

    def test_walls_atleast_one(self):
        self.assertGreater(len(self.gameboard.wall_list), 0)

    def test_no_walls_in_margin(self):
        print("Need rectangle collison Algorithm")


if __name__ == '__main__':
    unittest.main
