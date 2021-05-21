import unittest
import math
from game.common.game_board import GameBoard

class TestGameBoard(unittest.TestCase):

    def test_circle_radius(self):
        # square board test
        game_board1 = GameBoard(10, 10)
        self.assertGreaterEqual(game_board1.circle_radius, math.sqrt(200)) # should succeed
        self.assertAlmostEqual(game_board1.circle_radius, math.sqrt(200)) # if the first test fails, but this one succeeds, then there might be rounding errors

        # rectangular board test, width greater than height
        game_board2 = GameBoard(15, 10)
        self.assertGreaterEqual(game_board1.circle_radius, math.sqrt(325)) # should succeed
        self.assertAlmostEqual(game_board1.circle_radius, math.sqrt(325)) # shows possible rounding errors

        # rectangular board test, height greater than width
        game_board3 = GameBoard(10, 15)
        self.assertGreaterEqual(game_board3.circle_radius, math.sqrt(325)) # should succeed
        self.assertAlmostEqual(game_board3.circle_radius, math.sqrt(325)) # shows possible rounding errors