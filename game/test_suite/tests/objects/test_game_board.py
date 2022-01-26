import unittest
import math
from game.common.game_board import GameBoard


class TestGameBoard(unittest.TestCase):
    # square board test
    def test_circle_square(self):
        game_board1 = GameBoard(100, 100)
        self.assertGreaterEqual(
            game_board1.circle_radius, .5 * math.sqrt(20000))  # should succeed

    # rectangular board test, width greater than height
    def test_circle_rect_width(self):
        game_board2 = GameBoard(150, 100)
        self.assertGreaterEqual(
            game_board2.circle_radius, .5 * math.sqrt(22500))  # should succeed

    # rectangular board test, height greater than width
    def test_circle_rect_height(self):
        game_board3 = GameBoard(100, 150)
        self.assertGreaterEqual(
            game_board3.circle_radius, .5 * math.sqrt(32500))  # should succeed

    # check each corner's location, and if y value of corner is >= y value of the circle at that x,
    # then that corner must be inside the circle
    def test_circle_game_stats(self):
        # formula for circle: x^2 + y^2 = r^2
        def check_corner(corner_x, corner_y, radius):
            circle_y = math.sqrt(radius ** 2 - corner_x ** 2)
            if circle_y >= corner_y:
                return True
            return False

        game_board4 = GameBoard()
        radius = game_board4.circle_radius
        width = game_board4.width
        height = game_board4.height
        self.assertTrue(
            check_corner(width / 2, height / 2, radius) and  # QI
            check_corner(-1 * (width / 2), height / 2, radius) and  # QII
            # QIII
            check_corner(-1 * (width / 2), -1 * (height / 2), radius) and
            check_corner(width / 2, -1 * (height / 2), radius)  # QIV
        )
