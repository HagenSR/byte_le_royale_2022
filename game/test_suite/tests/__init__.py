# When you create a new test file, make sure to add it here.
# Simply import the class from your file, and then add that class to the
# '__all__' array.

from game.test_suite.tests.objects.test_game_board import TestGameBoard
from game.test_suite.tests.objects.test_moving_object import TestMovingObject
from game.test_suite.tests.objects.test_damaging_object import TestDamagingObject
from game.test_suite.tests.objects.test_grenade import TestGrenade
from game.test_suite.tests.objects.test_bullet import TestBullet
from game.test_suite.tests.objects.test_initialization import TestInit
from game.test_suite.tests.objects.test_shooter import TestShooterObject
from game.test_suite.tests.objects.test_hitbox_object import TestHitboxObject
from game.test_suite.tests.test_shop_controller import TestShopController
from game.test_suite.tests.utils.ray_collision_test import TestRayCollision
#from game.test_suite.tests.utils.test_game_board_generation import TestGameBoardGeneration
from game.test_suite.tests.collision_test import TestCollision
from game.test_suite.tests.controllers.test_kill_boundary_controller import TestKillBoundary
from game.test_suite.tests.controllers.test_reload_controller import TestReloadController


__all__ = [
    'TestGameBoard',
    'TestMovingObject',
    'TestDamagingObject',
    'TestShooterObject',
    'TestGrenade',
    'TestBullet',
    'TestInit',
    'TestHitboxObject',
    # 'TestGameBoardGeneration'
    'TestCollision',
    'TestShopController',
    'TestKillBoundary',
    'TestRayCollision',
    'TestReloadController'
]
