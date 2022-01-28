import math
from game.client.user_client import UserClient
from game.common.enums import *

######################################################
# imports for type hints
from game.common.action import Action
from game.common.moving.shooter import Shooter
from game.utils.partition_grid import PartitionGrid
######################################################

from game.utils.player_utils import *


class Client(UserClient):
    # Variables and info you want to save between turns go here
    def __init__(self):
        super().__init__()
        self.prev_location = (0, 0)

    def team_name(self):
        """
        Allows the team to set a team name.
        :return: Your team name
        """
        return 'Bad Awful Client'

    # This is where your AI will decide what to do
    def take_turn(self, turn, actions: Action, game_board, partition_grid: PartitionGrid, shooter: Shooter) -> None:
        """
        This is where your AI will decide what to do.
        :param partition_grid: This is the representation of the game map divided into partitions
        :param turn:        The current turn of the game.
        :param actions:     This is the actions object that you use to declare your intended actions.
        :param world:       Generic world information
        :param shooter:      This is your in-game character object
        """
        angle = angle_to_point(shooter, game_board.center)

        if self.prev_location != shooter.hitbox.position:
            actions.set_move(int(angle), shooter.max_speed)
            self.prev_location = shooter.hitbox.position
        else:
            actions.set_shoot(shooter.heading)
