from game.controllers.controller import Controller
from game.common.game_board import GameBoard
from game.client.user_client import UserClient
from game.common.stats import GameStats
import copy


class PlayerViewController(Controller):
    def __init__(self):
        super().__init__()
        self.view_distance =

    def handle_actions(self, clients: list[UserClient], game_board: GameBoard):
        # Take partition grid, remove anything that shouldn't be seen by the player
        # return a deepcopy of the modified partition grid.
        for client in clients:
            map = copy.deepcopy(game_board.partition)
            client_heading = client.shooter.heading
            # Check all partitions, if a partition isn't in view, obfuscate it
            # if it is in view, remove only objects that aren't visible
            


    def in_view(self, partition, client_heading):
        """Returns true if any part of the partition is in view, false otherwise"""


