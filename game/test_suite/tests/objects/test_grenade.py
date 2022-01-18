from game.common.hitbox import Hitbox
import unittest
from game.common.moving.damaging import grenade
from game.common.moving.damaging.grenade import Grenade
from game.common.stats import GameStats


class TestGrenade(unittest.TestCase):

    def setUp(self):
        self.grnObj = Grenade(hitbox=Hitbox(10, 10, (10, 10)), health=10, fuse_time=10, damage=50)

    def test_set_get_fuse_time_valid(self):
        self.grnObj.fuse_time = 20
        self.assertEqual(self.grnObj.fuse_time, 20)

    def test_set_get_fuse_time_invalid_low(self):
        self.assertRaises(Exception, self.setFuse, (0))

    def test_set_get_fuse_time_invalid_high(self):
        self.assertRaises(Exception, self.setFuse, (100))

    def test_set_get_fuse_time_boundary_low(self):
        self.grnObj.fuse_time = GameStats.grenade_stats['min_fuse_time']
        self.assertEqual(
            self.grnObj.fuse_time,
            GameStats.grenade_stats['min_fuse_time'])

    def test_set_get_fuse_time_boundary_high(self):
        self.grnObj.fuse_time = GameStats.grenade_stats['max_fuse_time']
        self.assertEqual(
            self.grnObj.fuse_time,
            GameStats.grenade_stats['max_fuse_time'])

    def test_grenade_obj_parent_params(self):
        testGrn = Grenade(hitbox=Hitbox(10,10,(10,10)), health=10, fuse_time=10, damage=10)

        #only two parent parameters
        self.assertIsNotNone(testGrn.hitbox)
        self.assertIsNotNone(testGrn.health)

    def setFuse(self, newTime):
        self.grnObj.fuse_time = newTime


if __name__ == '__main__':
    unittest.main
