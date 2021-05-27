from game.common.moving.moving_object import MovingObject
from game.common.stats import GameStats


class Player(MovingObject):
    def __init__(self):
        super().__init__()
        self.health = GameStats.player_stats['starting_health']
        self.inventory = []
        self.money = GameStats.player_stats['starting_money']
        self.armor = None
        self.visible = []
        self.view_radius = GameStats.player_stats['view_radius']
        self.moving = False

    # purpose of this is to set the heading and direction in a controlled way
    def move(self, heading):
        self.__heading = heading
        self.__speed = GameStats.player_stats['move_speed']
        self.moving = True

