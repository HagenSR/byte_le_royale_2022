import unittest
from game.common.hitbox import Hitbox
from game.common.moving.damaging.damaging_object import DamagingObject
from game.common.stats import GameStats
from game.common.hitbox import Hitbox


class TestHitboxObject(unittest.TestCase):
    def setUp(self):
        self.hitbox = Hitbox(2, 2, (0, 0))

    def test_set_get_heigth_valid(self):
        self.hitbox.height = 10
        self.assertEqual(self.hitbox.height, 10)

    def test_set_get_heigth_valid(self):
        self.hitbox.height = 7
        self.assertEqual(self.hitbox.height, 7)

    def test_set_get_tuple_x_valid(self):
        self.hitbox.position = (50, 10)
        self.assertEqual(self.hitbox.position, (50, 10))

    def test_set_get_tuple_y_valid(self):
        self.hitbox.position = (10, 50)
        self.assertEqual(self.hitbox.position, (10, 50))

    def test_set_get_tuple_y_boundary_low(self):
        self.hitbox.position = (10, 0)
        self.assertEqual(self.hitbox.position, (10, 0))

    def test_set_get_tuple_y_boundary_high(self):
        self.hitbox.position = (10, GameStats.game_board_height - self.hitbox.height)
        self.assertEqual(self.hitbox.position,
                         (10, GameStats.game_board_height- self.hitbox.height))

    def test_set_get_tuple_x_boundary_high(self):
        self.hitbox.position = (GameStats.game_board_width - self.hitbox.width, 10)
        self.assertEqual(self.hitbox.position,
                         (GameStats.game_board_width - self.hitbox.width, 10))

    def test_set_get_tuple_x_invalid_high(self):
        self.assertRaises(ValueError, self.setPosition,
                          (GameStats.game_board_width + 1, 10))

    def test_set_get_tuple_y_invalid_high(self):
        self.assertRaises(ValueError, self.setPosition,
                          (10, GameStats.game_board_height + 1))

    def test_set_get_tuple_x_boundary_low(self):
        self.assertRaises(ValueError, self.setPosition, ((-1, 10)))

    def test_set_get_tuple_y_boundary_low(self):
        self.assertRaises(ValueError, self.setPosition, ((10, -1)))

    def test_topLeft_corner(self):
        self.assertEqual(self.hitbox.topLeft, (0, 0))

    def test_topRight_corner(self):
        self.assertEqual(self.hitbox.topRight, (2, 0))

    def test_bottomLeft_corner(self):
        self.assertEqual(self.hitbox.bottomLeft, (0, 2))

    def test_bottomRight_corner(self):
        self.assertEqual(self.hitbox.bottomRight, (2, 2))

    def test_middle(self):
        self.assertEqual(self.hitbox.middle, (1, 1))

    def test_topLeft_corner_alt(self):
        self.hitbox.position = (10, 10)
        self.assertEqual(self.hitbox.topLeft, (10, 10))

    def test_topRight_corner_alt(self):
        self.hitbox.position = (10, 10)
        self.assertEqual(self.hitbox.topRight, (12, 10))

    def test_bottomLeft_corner_alt(self):
        self.hitbox.position = (10, 10)
        self.assertEqual(self.hitbox.bottomLeft, (10, 12))

    def test_bottomRight_corner_alt(self):
        self.hitbox.position = (10, 10)
        self.assertEqual(self.hitbox.bottomRight, (12, 12))

    def test_middle_alt(self):
        self.hitbox.position = (10, 10)
        self.assertEqual(self.hitbox.middle, (11, 11))

    def test_damaging_obj_parent_params(self):
        self.assertIsNotNone(self.hitbox.id)
        self.assertIsNotNone(self.hitbox.object_type)

    def test_set_get_height_invalid_low(self):
        self.assertRaises(ValueError, self.setHeight, -1)

    def test_set_get_width_invalid_low(self):
        self.assertRaises(ValueError, self.setWidth, (-1))

    def setPosition(self, newPos):
        self.hitbox.position = newPos

    def setHeight(self, newHeight):
        self.hitbox.height = newHeight

    def setWidth(self, newWidth):
        self.hitbox.width = newWidth


if __name__ == '__main__':
    unittest.main
