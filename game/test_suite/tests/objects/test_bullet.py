import unittest
from game.common.moving.damaging import bullet
from game.common.moving.damaging.bullet import Bullet
from game.common.stats import GameStats
from game.common.hitbox import Hitbox


class TestBullet(unittest.TestCase):

    def setUp(self):
        self.bltObj = Bullet((25, 25), False, range=5,
                             damage=5, heading=1, speed=1, health=5,
                             hitbox=Hitbox(5, 5, (5, 5)), collidable=True)

    def test_set_get_termination_valid(self):
        self.bltObj.termination = (10, 10)
        self.assertEqual(self.bltObj.termination, (10, 10))

    def test_set_get_termination_invalid_x_low(self):
        self.assertRaises(Exception, self.setTermination, -5)

    def test_set_get_termination_invalid_x_high(self):
        self.assertRaises(Exception, self.setTermination, 501)

    def test_set_get_termination_invalid_y_low(self):
        self.assertRaises(Exception, self.setTermination, -5)

    def test_set_get_termination_invalid_y_high(self):
        self.assertRaises(Exception, self.setTermination, 501)

    def test_set_get_termination_boundary_low(self):
        self.bltObj.termination = (0, 0)
        self.assertEqual(
            self.bltObj.termination, (0, 0))

    def test_set_get_termination_boundary_high(self):
        self.bltObj.termination = (GameStats.game_board_width, GameStats.game_board_height)
        self.assertEqual(
            self.bltObj.termination,
            (GameStats.game_board_width, GameStats.game_board_height))

    def test_bullet_obj_parent_params(self):
        testBlt = Bullet(
            termination=(10, 10),
            object_hit=True,
            range=10,
            damage=10,
            heading=1,
            speed=10,
            health=1,
            hitbox=Hitbox(
                10,
                10,
                (10,
                 10)),
            collidable=True)

        self.assertIsNotNone(testBlt.range)
        self.assertIsNotNone(testBlt.damage)
        self.assertIsNotNone(testBlt.heading)
        self.assertIsNotNone(testBlt.speed)
        self.assertIsNotNone(testBlt.hitbox.position)
        self.assertIsNotNone(testBlt.hitbox)
        self.assertIsNotNone(testBlt.collidable)

    # newTerm set as xy tuple
    def setTermination(self, newTerm):
        self.bltObj.termination = newTerm


if __name__ == '__main__':
    unittest.main
