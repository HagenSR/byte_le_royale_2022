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
        return 'Roomba Client'

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
        mappy = partition_grid.get_all_objects()
        shooter_position = (shooter.hitbox.position[0] + math.cos(math.radians(shooter.heading)),
                            shooter.hitbox.position[1] + math.sin(math.radians(shooter.heading)))
        object_in_front = partition_grid.find_object_coordinates(shooter_position[0], shooter_position[1])
        if self.prev_location != shooter.hitbox.middle:
            actions.set_move(int(angle), shooter.max_speed)
            self.prev_location = shooter.hitbox.middle
        elif object_in_front or 0 <= shooter_position[0] <= 500 or 0 <= shooter_position[1] <= 500 \
                and self.prev_location[0] != game_board.center:
            actions.set_move((shooter.heading + 90) % 360, shooter.max_speed)
        # if their is another player, shoot at it
        shooters = list(filter(lambda obj: obj.object_type == ObjectType.shooter, mappy))
        if len(shooters) > 1:
            actions.set_shoot(round(angle_to_point(shooter, shooters[0].hitbox.middle)))
            print('shot')
