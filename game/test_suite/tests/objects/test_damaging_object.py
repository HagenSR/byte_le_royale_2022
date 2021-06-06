import unittest 
from game.common.moving.damaging import damaging_object
from game.common.moving.damaging.damaging_object import DamagingObject
from game.common.stats import GameStats

class TestDamagingObject(unittest.TestCase):

    def setUp(self):
       self.dmgObj = DamagingObject(10, 10)
    
    def test_set_get_range_valid(self):
        self.dmgObj.range = 50
        self.assertEqual(self.dmgObj.range, 50)

    def test_set_get_damage_valid(self):
        self.dmgObj.damage = 50
        self.assertEqual(self.dmgObj.damage, 50)


    def test_set_get_range_invalid_low(self):
        # Checks if an exception is raised by an Illegal set
        # Lambda is needed because the property set isn't considered a function (which assertRaises takes as an argument)
        self.assertRaises(Exception, lambda : self.dmgObj.range(-10))

    def test_set_get_damage_invalid_low(self):
        self.assertRaises(Exception, lambda : self.dmgObj.damage(-10))
    
    def test_set_get_range_boundary_low(self):
        self.dmgObj.range = 0
        self.assertEqual(self.dmgObj.range, 0)

    # for now I have the lower boundary be zero but can be subject to change
    def test_set_get_damage_boundary_low(self): 
        self.dmgObj.damage = 0
        self.assertEqual(self.dmgObj.damage, 0)

    def test_set_get_range_boundary_high(self): 
        self.dmgObj.range = GameStats.damaging_object_stats['max_range']
        self.assertEqual(self.dmgObj.range, GameStats.damaging_object_stats['max_range']) 

    def test_set_get_damage_boundary_high(self): 
        self.dmgObj.damage = GameStats.damaging_object_stats['max_damage']
        self.assertEqual(self.dmgObj.damage, GameStats.damaging_object_stats['max_damage'])  

    def test_damaging_obj_parent_params(self):
        testDmg = DamagingObject(range = 10, damage = 10, heading = 10, speed = 10, health = 1, coordinates=[{'x': 450, 'y': 450}, {'x': 50, 'y': 50}], 
        hitbox={'width': 10, 'height': 10}, collidable=True)
        
       
        self.assertIsNotNone(testDmg.heading)
        self.assertIsNotNone(testDmg.speed)
        self.assertIsNotNone(testDmg.coordinates)
        self.assertIsNotNone(testDmg.hitbox)
        self.assertIsNotNone(testDmg.collidable)

       
        self.assertIsNone(self.dmgObj.heading)
        self.assertIsNone(self.dmgObj.speed)
        self.assertIsNone(self.dmgObj.coordinates)
        self.assertIsNone(self.dmgObj.hitbox)
        self.assertIsNone(self.dmgObj.collidable)
    
if __name__ == '__main__':
     unittest.main 