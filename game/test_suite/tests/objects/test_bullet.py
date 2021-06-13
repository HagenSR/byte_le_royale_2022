import unittest 
from game.common.moving.damaging import bullet
from game.common.moving.damaging.bullet import Bullet
from game.common.stats import GameStats

class TestBullet(unittest.TestCase):

    def setUp(self):
       self.bltObj = Bullet()