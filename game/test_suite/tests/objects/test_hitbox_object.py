import unittest 
from game.common.hitbox import Hitbox
from game.common.moving.damaging.damaging_object import DamagingObject
from game.common.stats import GameStats
from game.common.hitbox import Hitbox


class TestHitboxObject(unittest.TestCase):
    def setUp(self):
       self.hitbox = Hitbox(2,2,(0,0))
    
    def test_set_get_heigth_valid(self):
        self.hitbox.height = 10
        self.assertEqual(self.hitbox.height, 10)

    def test_set_get_heigth_valid(self):
        self.hitbox.height = 7
        self.assertEqual(self.hitbox.height, 7)

    def test_set_get_tuple_x_valid(self):
        self.hitbox.position = (50,10)
        self.assertEqual(self.hitbox.position, (50,10))
    
    def test_set_get_tuple_y_valid(self):
        self.hitbox.position = (10,50)
        self.assertEqual(self.hitbox.position, (10,50))

    def test_set_get_tuple_y_boundary_low(self):
        self.hitbox.position = (10,0)
        self.assertEqual(self.hitbox.position, (10,0))

    def test_set_get_tuple_x_boundary_high(self):
        self.hitbox.position = (GameStats.game_board_width,10)
        self.assertEqual(self.hitbox.position, (GameStats.game_board_width,10))

    # def test_set_get_tuple_X_invalid_high(self):
    #     self.hitbox.position = (10,GameStats.game_board_height)
    #     self.assertEqual(self.hitbox.position, (10,GameStats.game_board_height))

    # def test_set_get_tuple_y_invalid_high(self):
    #     self.hitbox.position = (10,GameStats.game_board_height)
    #     self.assertEqual(self.hitbox.position, (10,GameStats.game_board_height))

    def test_topLeft_corner(self):
        self.assertEqual(self.hitbox.topLeft, (-1,-1))

    def test_topRight_corner(self):
        self.assertEqual(self.hitbox.topRight, (1,-1))

    def test_bottomLeft_corner(self):
        self.assertEqual(self.hitbox.bottomLeft, (-1,1))

    def test_bottomRight_corner(self):
        self.assertEqual(self.hitbox.bottomRight, (1,1))

    def test_topLeft_corner_alt(self):
        self.hitbox.position = (10,10) 
        self.assertEqual(self.hitbox.topLeft, (9,9))

    def test_topRight_corner_alt(self):
        self.hitbox.position = (10,10) 
        self.assertEqual(self.hitbox.topRight, (11,9))

    def test_bottomLeft_corner_alt(self):
        self.hitbox.position = (10,10) 
        self.assertEqual(self.hitbox.bottomLeft, (9,11))

    def test_bottomRight_corner_alt(self):
        self.hitbox.position = (10,10) 
        self.assertEqual(self.hitbox.bottomRight, (11,11))

    def test_damaging_obj_parent_params(self):
        self.assertIsNotNone(self.hitbox.id)
        self.assertIsNotNone(self.hitbox.object_type)

    
    # Needs a rework

    def test_set_get_height_invalid_low(self):
          # Checks if an exception is raised by an Illegal set
          # Lambda is needed because the property set isn't considered a function (which assertRaises takes as an argument)
          self.assertRaises(Exception, lambda : {self.hitbox.height(10)})

    # def test_set_get_width_invalid_low(self):
    #     self.assertRaises(Exception, lambda : self.hitbox.width(10))
    
    # def test_set_get_tuple_x_boundary_low(self):
    #     self.assertRaises(Exception, lambda self.hitbox.position((10, 10)))

    # def test_set_get_tuple_x_invalid_high(self):
    # try:
    #     self.hitbox.position = (GameStats.game_board_width,10)
    # except:
    #     self.assertTrue(True)
    
if __name__ == '__main__':
     unittest.main 