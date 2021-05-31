# This is a quick example test file to show you the basics.
# Always remember to add the proper details to the __init__.py file in the 'tests' folder
# to insure your tests are run.

import unittest
from game.common.moving.moving_object import MovingObject
from game.common.stats import GameStats


class TestMovingObject(unittest.TestCase):  # Your test class is a subclass of unittest.Testcase, this is important

    def setUp(self):  # This method is used to set up anything you wish to test prior to every test method below.
        self.movObj = MovingObject(10, 10)
    
    # Test if a valid heading set works
    def test_set_get_heading_valid(self):
        self.setUp()
        self.movObj.heading = 90
        self.assertEqual(self.movObj.heading, 90)
    
    # Test if a valid speed set works
    def test_set_get_speed_valid(self):
        self.setUp()
        self.movObj.speed = 100
        self.assertEqual(self.movObj.speed, 100)

    # Test if invalid sets don't work
    def test_set_get_heading_invalid_low(self):
        self.setUp()
        self.movObj.heading = -10
        self.assertEqual(self.movObj.heading, 10)

    def test_set_get_speed_invalid_low(self):
        self.setUp()
        self.movObj.speed = -1
        self.assertEqual(self.movObj.speed, 10)

    def test_set_get_heading_invalid_high(self):
        self.setUp()
        self.movObj.heading = 370
        self.assertEqual(self.movObj.heading, 10)

    # Check if boundary sets do work
    def test_set_get_heading_boundary_high(self):
        self.setUp()
        self.movObj.heading = 360
        self.assertEqual(self.movObj.heading, 360)

    def test_set_get_speed_boundary_high(self):
        self.setUp()
        self.movObj.speed = GameStats.moving_object_stats['max_speed']
        self.assertEqual(self.movObj.speed, GameStats.moving_object_stats['max_speed'])

    def test_set_get_heading_boundary_low(self):
        self.setUp()
        self.movObj.heading = 0
        self.assertEqual(self.movObj.heading, 0)

    def test_set_get_speed_boundary_low(self):
        self.setUp()
        self.movObj.speed = 0
        self.assertEqual(self.movObj.speed, 0)

    def test_moving_obj_parent_params(self):
        self.setUp()
        test_mov = MovingObject(10, 10, health=1, coordinates=[{'x': 450, 'y': 450}, {'x': 50, 'y': 50}], hitbox={'width': 10, 'height': 10}, collidable=True)
        self.assertIsNotNone(test_mov.coordinates)
        self.assertIsNotNone(test_mov.hitbox)
        self.assertIsNotNone(test_mov.collidable)
        self.assertIsNone(self.movObj.coordinates)
        self.assertIsNone(self.movObj.hitbox)
        self.assertIsNone(self.movObj.collidable)

    # This is just the very basics of how to set up a test file
    # For more info: https://docs.python.org/3/library/unittest.html


if __name__ == '__main__':
    unittest.main
