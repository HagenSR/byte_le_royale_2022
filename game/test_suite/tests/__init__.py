# When you create a new test file, make sure to add it here.
# Simply import the class from your file, and then add that class to the
# '__all__' array.

from game.test_suite.tests.objects.test_game_board import TestGameBoard
from game.test_suite.tests.objects.test_moving_object import TestMovingObject
from game.test_suite.tests.objects.test_damaging_object import TestDamagingObject
from game.test_suite.tests.objects.test_grenade import TestGrenade
from game.test_suite.tests.objects.test_initialization import TestInit
from game.test_suite.tests.objects.test_shooter import TestShooterObject
from game.test_suite.tests.objects.test_hitbox_object import TestHitboxObject
from game.test_suite.tests.collision_test import TestCollision


__all__ = [
    'TestGameBoard',
    'TestMovingObject',
    'TestDamagingObject',
    'TestShooterObject',
    'TestGrenade',
    'TestInit',
    'TestHitboxObject',
    'TestCollision'
]
