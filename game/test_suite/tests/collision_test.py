import unittest
from game.common.hitbox import Hitbox
from game.utils.collision_detection import check_collision


class TestCollision(unittest.TestCase):

    def setUp(self):
        self.hitOne = Hitbox(10, 10, (5, 5))
        self.hitTwo = Hitbox(25, 25, (5, 6))

    """Below are 3 examples of true cases and false cases. The hit boxes were graphed out beforehand 
    in order to determine if the test cases are behaving as expected."""
    def test_collision_true_one(self):
        self.hitOne.position = (5, 5)
        self.hitOne.height = 5
        self.hitOne.width = 8

        self.hitTwo.position = (5, 6)
        self.hitTwo.height = 5
        self.hitTwo.width = 8
        self.assertTrue(check_collision(self.hitOne, self.hitTwo))

    def test_collision_false_one(self):
        self.hitOne.position = (5, 5)
        self.hitOne.height = 5
        self.hitOne.width = 8

        self.hitTwo.position = (20, 20)
        self.hitTwo.height = 5
        self.hitTwo.width = 8
        self.assertFalse(check_collision(self.hitOne, self.hitTwo))

    def test_collision_true_two(self):
        self.hitOne.position = (5, 5)
        self.hitOne.height = 6
        self.hitOne.width = 4

        self.hitTwo.position = (1, 3)
        self.hitTwo.height = 2
        self.hitTwo.width = 6
        self.assertTrue(check_collision(self.hitOne, self.hitTwo))

    def test_collision_false_two(self):
        self.hitOne.position = (5, 5)
        self.hitOne.height = 4
        self.hitOne.width = 4

        self.hitTwo.position = (20, 20)
        self.hitTwo.height = 6
        self.hitTwo.width = 2
        self.assertFalse(check_collision(self.hitOne, self.hitTwo))

    def test_collision_true_three(self):
        self.hitOne.position = (60, 50)
        self.hitOne.height = 40
        self.hitOne.width = 80

        self.hitTwo.position = (20, 20)
        self.hitTwo.height = 30
        self.hitTwo.width = 40
        self.assertTrue(check_collision(self.hitOne, self.hitTwo))

    def test_collision_false_three(self):
        self.hitOne.position = (60, 50)
        self.hitOne.height = 40
        self.hitOne.width = 80

        self.hitTwo.position = (20, 20)
        self.hitTwo.height = 10
        self.hitTwo.width = 20
        self.assertFalse(check_collision(self.hitOne, self.hitTwo))


if __name__ == '__main__':
    unittest.main
