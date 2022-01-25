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
        # This is the list that contains all the objects on the map your player can see
        map_objects = partition_grid.get_all_objects()
        # This is a tuple that represents the position 1 unit in front of where the player
        forward_position = (shooter.hitbox.middle[0] + shooter.hitbox.width + math.cos(math.radians(shooter.heading)),
                            shooter.hitbox.middle[1] + shooter.hitbox.height + math.sin(math.radians(shooter.heading)))
        object_in_front = None
        if forward_position[0] < game_board.width and forward_position[1] < game_board.height:
            # this will get the object that is in front of the player if there is one
            object_in_front = partition_grid.find_object_coordinates(forward_position[0], forward_position[1])
        if self.prev_location != shooter.hitbox.middle:
            # If the player moved last turn, move them towards the center
            angle = angle_to_point(shooter, game_board.center)
            actions.set_move(int(angle), shooter.max_speed)
            self.prev_location = shooter.hitbox.middle
        elif object_in_front or 0 <= forward_position[0] <= 500 or 0 <= forward_position[1] <= 500 \
                and self.prev_location != game_board.center:
            # if there is something in front of the player, but the player isn't already in the center,
            # turn 90 degrees and try to move again
            actions.set_move((shooter.heading + 90) % 360, shooter.max_speed)
        # if their is another player, shoot at it
        shooters = list(filter(lambda obj: obj.object_type == ObjectType.shooter, map_objects))
        if len(shooters) > 1:
            actions.set_shoot(round(angle_to_point(shooter, shooters[0].hitbox.middle)))
