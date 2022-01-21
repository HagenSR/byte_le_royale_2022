import unittest

from game.common.hitbox import Hitbox
from game.utils.collision_detection import intersect_circle


class TestIntersectCircle(unittest.TestCase):
    def setUp(self) -> None:
        self.center = (10, 10)
        self.radius = 3

    def test_inside_circle(self):
        hitbox = Hitbox(2, 2, (9, 9))
        self.assertTrue(intersect_circle(self.center, self.radius, hitbox))

    def test_on_edge(self):
        hitbox = Hitbox(2, 2, (9, 5))
        self.assertFalse(intersect_circle(self.center, self.radius, hitbox))

    def test_on_edge_in_circle(self):
        hitbox = Hitbox(2, 2, (6, 9))
        self.assertTrue(intersect_circle(self.center, self.radius, hitbox))

    def test_on_corner(self):
        hitbox = Hitbox(2, 2, (12, 7))
        self.assertTrue(intersect_circle(self.center, self.radius, hitbox))

    def test_outside_circle_corner(self):
        hitbox = Hitbox(2, 2, (6, 5))
        self.assertFalse(intersect_circle(self.center, self.radius, hitbox))

    def test_outside_circle_lower_corner(self):
        hitbox = Hitbox(2, 2, (5, 6))
        self.assertFalse(intersect_circle(self.center, self.radius, hitbox))

    def test_edge_slightly_up(self):
        hitbox = Hitbox(2, 2, (5, 8))
        self.assertFalse(intersect_circle(self.center, self.radius, hitbox))
