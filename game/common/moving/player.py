from game.common.moving.moving_object import MovingObject
from game.common.stats import GameStats
from game.common.enums import *


class Player(MovingObject):
    def __init__(self):
        super().__init__()
        self.health = GameStats.player_stats['starting_health']
        self.inventory = []
        self.money = GameStats.player_stats['starting_money']
        self.armor = None
        self.visible = []
        self.view_radius = GameStats.player_stats['view_radius']

    def move(self, heading, distance):
        self.__heading = heading
        self.__speed = GameStats.player_stats['move_speed']

        # TODO add logic for movement, might want in controller instead

