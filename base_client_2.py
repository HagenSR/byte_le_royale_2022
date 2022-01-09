import math

from game.client.user_client import UserClient
from game.common.enums import *

######################################################
# imports for type hints
from game.common.action import Action
from game.common.moving.shooter import Shooter
from game.utils.partition_grid import PartitionGrid
######################################################

from game.utils.collision_detection import distance_tuples

class Client(UserClient):
    # Variables and info you want to save between turns go here
    def __init__(self):
        super().__init__()

    def team_name(self):
        """
        Allows the team to set a team name.
        :return: Your team name
        """
        return 'Example Client'

    # This is where your AI will decide what to do
    def take_turn(self, turn, actions: Action, world, partition_grid: PartitionGrid, player: Shooter) -> None:
        """
        This is where your AI will decide what to do.
        :param partition_grid: This is the representation of the game map divided into partitions
        :param turn:        The current turn of the game.
        :param actions:     This is the actions object that you use to declare your intended actions.
        :param world:       Generic world information
        :param player:      This is your in-game character object
        """
        game_board = world["game_map"]
        angle = int(math.degrees(math.acos(
            abs(player.hitbox.position[1] - game_board.center[1]) /
            distance_tuples(player.hitbox.position, game_board.center))))

        actions.set_move(angle, player.max_speed)
