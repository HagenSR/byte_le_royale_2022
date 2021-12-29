# This is a quick example test file to show you the basics.
# Always remember to add the proper details to the __init__.py file in the 'tests' folder
# to insure your tests are run.

import unittest
from unittest.case import FunctionTestCase
from game.common.moving.moving_object import MovingObject
from game.common.stats import GameStats
from game.common.hitbox import Hitbox
import math


class TestMovingObject(
        unittest.TestCase):  # Your test class is a subclass of unittest.Testcase, this is important

    # This method is used to set up anything you wish to test prior to every
    # test method below.
    def setUp(self):
        self.movObj = MovingObject(1, 10)

    # Test if a valid heading set works
    def test_set_get_heading_valid(self):
        self.movObj.heading = 180
        self.assertEqual(self.movObj.heading, 180)

    # Test if a valid speed set works
    def test_set_get_speed_valid(self):
        self.movObj.speed = 100
        self.assertEqual(self.movObj.speed, 100)

    # Test if invalid sets don't work
    def test_set_get_heading_invalid_low(self):
        self.assertRaises(Exception, self.setHeading, -1)

    def test_set_get_speed_invalid_low(self):
        self.assertRaises(Exception, self.setSpeed, -1)

    def test_set_get_heading_invalid_high(self):
        self.assertRaises(Exception, self.setHeading, 361)

    def test_set_get_speed_invalid_high(self):
        self.assertRaises(
            Exception,
            self.setSpeed,
            (GameStats.moving_object_stats['max_speed'] + 1))

    # Check if boundary sets do work
    def test_set_get_heading_boundary_high(self):
        self.movObj.heading = 360
        self.assertEqual(self.movObj.heading, 360)

    def test_set_get_speed_boundary_high(self):
        self.movObj.speed = GameStats.moving_object_stats['max_speed']
        self.assertEqual(
            self.movObj.speed,
            GameStats.moving_object_stats['max_speed'])

    def test_set_get_heading_boundary_low(self):
        self.movObj.heading = 0
        self.assertEqual(self.movObj.heading, 0)

    def test_set_get_speed_boundary_low(self):
        self.movObj.speed = 0
        self.assertEqual(self.movObj.speed, 0)

    def test_moving_obj_parent_params(self):
        test_mov = MovingObject(
            1, 10, health=1, hitbox=Hitbox(
                10, 10, (10, 10)), collidable=True)
        self.assertIsNotNone(test_mov.hitbox.position)
        self.assertIsNotNone(test_mov.hitbox)
        self.assertIsNotNone(test_mov.collidable)
        self.assertIsNone(self.movObj.hitbox)
        self.assertIsNone(self.movObj.collidable)

    def setHeading(self, newHeading):
        self.movObj.heading = newHeading

    def setSpeed(self, newSpeed):
        self.movObj.speed = newSpeed

    def setHeading(self, newHeading):
        self.movObj.heading = newHeading

    def setSpeed(self, newSpeed):
        self.movObj.speed = newSpeed

    # This is just the very basics of how to set up a test file
    # For more info: https://docs.python.org/3/library/unittest.html


if __name__ == '__main__':
    unittest.main
