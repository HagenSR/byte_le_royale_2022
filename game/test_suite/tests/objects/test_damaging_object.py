import unittest 
from game.common.moving.damaging import damaging_object
from game.common.moving.damaging.damaging_object import DamagingObject
from game.common.stats import GameStats
from game.common.hitbox import Hitbox


class TestDamagingObject(unittest.TestCase):
    def setUp(self):
       self.dmgObj = DamagingObject(10, 10, heading= 1, speed= 1, hitbox= Hitbox(5,5 ,(5,5)), collidable=True)
    
    def test_set_get_range_valid(self):
        self.dmgObj.range = 50
        self.assertEqual(self.dmgObj.range, 50)

    def test_set_get_damage_valid(self):
        self.dmgObj.damage = 50
        self.assertEqual(self.dmgObj.damage, 50)


    def test_set_get_range_invalid_low(self):
        self.assertRaises(Exception, self.setRange, (-10))
        
    def test_set_get_range_invalid_high(self):
        self.assertRaises(Exception, self.setRange, (GameStats.damaging_object_stats['max_range'] + 1))

    def test_set_get_damage_invalid_low(self):
        self.assertRaises(Exception, self.setDamage, (-10))
        
    def test_set_get_damage_invalid_high(self):
        self.assertRaises(Exception, self.setDamage, GameStats.damaging_object_stats['max_damage'] + 1)
    
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
        testDmg = DamagingObject(range = 10, damage = 10, heading = 1, speed = 10, health = 1, hitbox= Hitbox(5,5,(5,5)), collidable=True)
        
       
        self.assertIsNotNone(testDmg.heading)
        self.assertIsNotNone(testDmg.speed)
        self.assertIsNotNone(testDmg.hitbox.position)
        self.assertIsNotNone(testDmg.hitbox)
        self.assertIsNotNone(testDmg.collidable)
        
    def setRange(self, newRange):
        self.dmgObj.range = newRange
        
    def setDamage(self, newDamage):
        self.dmgObj.damage = newDamage
    
if __name__ == '__main__':
     unittest.main 