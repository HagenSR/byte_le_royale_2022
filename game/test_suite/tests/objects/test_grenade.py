from game.common.hitbox import Hitbox
import unittest
from game.common.moving.damaging import grenade
from game.common.moving.damaging.grenade import Grenade
from game.common.stats import GameStats


class TestGrenade(unittest.TestCase):

    def setUp(self):
        self.grnObj = Grenade(damage=10, heading=1, speed=1, range=1)

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
        testGrn = Grenade(fuse_time=20, range=10, damage=10, heading=1, speed=10, health=1,
                          hitbox=Hitbox(10, 10, (10, 10)), collidable=True)

        self.assertIsNotNone(testGrn.range)
        self.assertIsNotNone(testGrn.damage)
        self.assertIsNotNone(testGrn.heading)
        self.assertIsNotNone(testGrn.speed)
        self.assertIsNotNone(testGrn.hitbox.position)
        self.assertIsNotNone(testGrn.hitbox)
        self.assertIsNotNone(testGrn.collidable)

    def setFuse(self, newTime):
        self.grnObj.fuse_time = newTime


if __name__ == '__main__':
    unittest.main
