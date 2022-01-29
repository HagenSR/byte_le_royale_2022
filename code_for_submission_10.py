import math
from game.client.user_client import UserClient
from game.common.enums import *

######################################################
# imports for type hints
from game.common.action import Action
from game.common.moving.shooter import Shooter
from game.utils.partition_grid import PartitionGrid
######################################################
import random
from game.utils.player_utils import *


class Client(UserClient):
    # Variables and info you want to save between turns go here
    def __init__(self):
        super().__init__()
        self.prev_location = (0, 0)
        self.angle = -1

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
        if shooter.hitbox.position == self.prev_location or self.angle != -1:
            self.angle = int(((random.randint(-55, 55) + angle_to_point(shooter, game_board.center))) % 360)
            obs = partition_grid.find_all_object_collisions(shooter.hitbox)
            # for ob in obs:
            #     print(f"BAD OBJECTS {ob.id}")
        else:
            self.angle = int((angle_to_point(shooter, game_board.center)) % 360)

        if distance_tuples(shooter.hitbox.position, game_board.center) > 100:
            actions.set_move(int(self.angle), int(shooter.max_speed / 4))
            # print(f"Moving, Position {shooter.hitbox.position}, angle: {self.angle}")
        self.prev_location = shooter.hitbox.position
