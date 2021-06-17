import unittest 
from game.common.hitbox import Hitbox
from game.common.moving.damaging.damaging_object import DamagingObject
from game.common.stats import GameStats
from game.common.hitbox import Hitbox


class TestHitboxObject(unittest.TestCase):
    def setUp(self):
       self.hitbox = Hitbox(5,5,(5,5))
    
    def test_set_get_heigth_valid(self):
        self.hitbox.height = 10
        self.assertEqual(self.hitbox.height, 10)

    def test_set_get_heigth_valid(self):
        self.hitbox.height = 7
        self.assertEqual(self.hitbox.height, 7)

    def test_set_get_height_invalid_low(self):
        # Checks if an exception is raised by an Illegal set
        # Lambda is needed because the property set isn't considered a function (which assertRaises takes as an argument)
        self.assertRaises(Exception, lambda : {self.hitbox.height(10)})

    def test_set_get_width_invalid_low(self):
        self.assertRaises(Exception, lambda : self.hitbox.width(10))
    
    def test_set_get_tuple_x_boundary_low(self):
        self.assertRaises(Exception, lambda : self.hitbox.position((10, 10)))

    def test_set_get_tuple_y_boundary_low(self):
        self.hitbox.position = (10,0)
        self.assertEqual(self.hitbox.position[0], 10)
        self.assertEqual(self.hitbox.position[1], 0)

    def test_damaging_obj_parent_params(self):
        self.assertIsNotNone(self.hitbox.id)
        self.assertIsNotNone(self.hitbox.object_type)
    
if __name__ == '__main__':
     unittest.main 