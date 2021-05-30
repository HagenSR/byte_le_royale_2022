# When you create a new test file, make sure to add it here.
# Simply import the class from your file, and then add that class to the '__all__' array.

from game.test_suite.tests.test_game_board import TestGameBoard
from game.test_suite.tests.test_moving_object import TestMovingObject
from game.test_suite.tests.test_damaging_object import TestDamagingObject

__all__ = [
    'TestGameBoard',
    'TestMovingObject',
    'TestDamagingObject'
]