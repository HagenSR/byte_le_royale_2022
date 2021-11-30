import unittest
from game.common.hitbox import Hitbox
from game.common.stats import GameStats
<<<<<<< HEAD

# from game.utils.collision_detection import check_collision, intersect_arc, collide_rect_hb
from game.utils.collision_detection import check_collision, intersect_circle

=======
from game.utils.collision_detection import intersect_circle, collide_rect_hb
>>>>>>> d0ac613effa0cfa06cbda2c9a0c78285284b417d


class TestCollision(unittest.TestCase):

    def setUp(self):
        self.hitOne = Hitbox(10, 10, (5, 5))
        self.hitTwo = Hitbox(25, 25, (5, 6))

    # Below are 3 examples of true cases and false cases. The hit boxes were graphed out beforehand
    # in order to determine if the test cases are behaving as expected.

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
        # self.assertFalse(check_collision(self.hitOne, self.hitTwo))
        self.assertFalse(check_collision(self.hitOne, self.hitTwo))

    def test_collision_true_two(self):
        self.hitOne.position = (5, 5)
        self.hitOne.height = 6
        self.hitOne.width = 4

        self.hitTwo.position = (1, 3)
        self.hitTwo.height = 6
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
        self.hitTwo.height = 50
        self.hitTwo.width = 60
        self.assertTrue(check_collision(self.hitOne, self.hitTwo))

    def test_collision_false_three(self):
        self.hitOne.position = (60, 50)
        self.hitOne.height = 40
        self.hitOne.width = 80

        self.hitTwo.position = (20, 20)
        self.hitTwo.height = 10
        self.hitTwo.width = 20
        self.assertFalse(check_collision(self.hitOne, self.hitTwo))

    # tests for methods used in player view controller
    def test_circle(self):
        hitbox1 = Hitbox(2, 2, (2, 2))
        self.assertTrue(intersect_circle((3, 1), 5, hitbox1))

    def test_arc_intersect_circle_in_rect(self):
        center = (10, 10)
        radius = 6

        self.assertTrue(
            intersect_circle(
                center,
                radius,
                self.hitOne))

    def test_arc_intersect_circle_on_edge(self):
        center = (10, 15)
        radius = 4

        self.assertTrue(
            intersect_circle(
                center,
                radius,
                self.hitOne))

    def test_arc_intersect_circle_to_side_and_top(self):
        center = (3, 3)
        radius = 5

        self.assertTrue(
            intersect_circle(
                center,
                radius,
                self.hitOne))

    def test_arc_intersect_false(self):
        center = (3, 3)
        radius = 1

        self.assertFalse(
            intersect_circle(
                center,
                radius,
                self.hitOne))


if __name__ == '__main__':
    unittest.main
