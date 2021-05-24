# This is a quick example test file to show you the basics.
# Always remember to add the proper details to the __init__.py file in the 'tests' folder
# to insure your tests are run.

import unittest
from game.common.moving.moving_object import MovingObject

class TestMovingObject(unittest.TestCase): # Your test class is a subclass of unittest.Testcase, this is important

    def setUp(self): # This method is used to set up anything you wish to test prior to every test method below.
        self.movObj = MovingObject(10, 10)
    
    def test_set_get_heading_valid(self):
        self.setUp()
        self.movObj.set_heading(90)
        self.assertEqual(self.movObj.get_heading(), 90)
    
    def test_set_get_speed_valid(self):
        self.setUp()
        self.movObj.set_speed(100)
        self.assertEqual(self.movObj.get_speed(), 100)

    def test_set_get_heading_invalid_low(self):
        self.setUp()
        self.movObj.set_heading(-10)
        self.assertEqual(self.movObj.get_heading(), 10)

    def test_set_get_speed_invalid_low(self):
        self.setUp()
        self.movObj.set_speed(-1)
        self.assertEqual(self.movObj.get_speed(), 10)

    def test_set_get_heading_invalid_high(self):
        self.setUp()
        self.movObj.set_heading(370)
        self.assertEqual(self.movObj.get_heading(), 10)

    def test_set_get_heading_boundary_high(self):
        self.setUp()
        self.movObj.set_heading(360)
        self.assertEqual(self.movObj.get_heading(), 360)

    def test_set_get_heading_boundary_low(self):
        self.setUp()
        self.movObj.set_heading(0)
        self.assertEqual(self.movObj.get_heading(), 0)

    def test_set_get_speed_boundary_low(self):
        self.setUp()
        self.movObj.set_speed(0)
        self.assertEqual(self.movObj.get_speed(), 0)


    
    

    # This is just the very basics of how to set up a test file
    # For more info: https://docs.python.org/3/library/unittest.html


if __name__ == '__main__':
    unittest.main
