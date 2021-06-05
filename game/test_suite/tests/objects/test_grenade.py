import unittest 
from game.common.moving.damaging import grenade
from game.common.moving.damaging.grenade import Grenade
from game.common.stats import GameStats

class TestGrenade(unittest.TestCase):

    def setUp(self):
       self.grnObj = Grenade(10)
    
    def test_set_get_fuse_time_valid(self):
        self.grnObj.fuse_time = 20
        self.assertEqual(self.grnObj.fuse_time, 20)
     

    def test_set_get_fuse_time_invalid_low(self):
         self.assertRaises(Exception, lambda : self.grnObj.fuse_time(0))

    def test_set_get_fuse_time_boundary_low(self):
        self.grnObj.fuse_time = GameStats.grenade_stats['min_fuse_time']
        self.assertEqual(self.grnObj.fuse_time, GameStats.grenade_stats['min_fuse_time'])
     

    def test_set_get_fuse_time_boundary_high(self): 
        self.grnObj.fuse_time = GameStats.grenade_stats['max_fuse_time']
        self.assertEqual(self.grnObj.fuse_time, GameStats.grenade_stats['max_fuse_time'])
       

    def test_grenade_obj_parent_params(self):
      
        testGrn = Grenade(fuse_time = 20, range = 10, damage = 10, heading = 10, speed = 10, health = 1, coordinates=[{'x': 450, 'y': 450}, {'x': 50, 'y': 50}], 
        hitbox={'width': 10, 'height': 10}, collidable=True)
        
        self.assertIsNotNone(testGrn.range)
        self.assertIsNotNone(testGrn.damage)
        self.assertIsNotNone(testGrn.heading)
        self.assertIsNotNone(testGrn.speed)
        self.assertIsNotNone(testGrn.coordinates)
        self.assertIsNotNone(testGrn.hitbox)
        self.assertIsNotNone(testGrn.collidable)

        self.assertIsNone(self.grnObj.range)
        self.assertIsNone(self.grnObj.damage)
        self.assertIsNone(self.grnObj.heading)
        self.assertIsNone(self.grnObj.speed)
        self.assertIsNone(self.grnObj.coordinates)
        self.assertIsNone(self.grnObj.hitbox)
        self.assertIsNone(self.grnObj.collidable)
    
if __name__ == '__main__':
     unittest.main 