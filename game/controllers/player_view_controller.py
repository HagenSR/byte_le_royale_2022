from game.controllers.controller import Controller
from game.common.game_board import GameBoard
from game.client.user_client import UserClient
from game.common.stats import GameStats
from game.utils.collision_detection import arc_intersect
import copy


class PlayerViewController(Controller):
    def __init__(self):
        super().__init__()

    def handle_actions(self, clients: list[UserClient], game_board: GameBoard):
        # Take partition grid, remove anything that shouldn't be seen by the player
        # return a deepcopy of the modified partition grid.
        for client in clients:
            board = copy.deepcopy(game_board.partition)
            # get center of client hitbox for origin of view arc
            client_shooter_xy = (
                client.shooter.hitbox.topLeft[0] + client.shooter.hitbox.topRight[0] / 2,
                client.shooter.hitbox.topLeft[1] + client.shooter.hitbox.bottomLeft[1] / 2)
            client_heading = client.shooter.heading
            client_view_distance = client.shooter.view_distance
            client_field_of_view = client.shooter.field_of_view

            # Check all partitions, if a partition isn't in view, obfuscate it
            # if it is in view, remove only objects that aren't visible
            for x, y in range(0, GameStats.game_board_width, board.partition_width), range(0, GameStats.game_board_height, board.partition_height):
                partition = board.get_partition_hitbox(x, y)
                # remove everything from a partition that isn't in view at all
                if not self.in_view(
                        partition,
                        client_heading,
                        client_field_of_view,
                        client_view_distance,
                        client_shooter_xy):
                    board.obfuscate_partition(x, y)
                else:
                    # if a partition is in view, need to check each object to see if it's in view, remove it if it isn't
                    for obj in board.get_partition_objects(x, y):
                        if not self.in_view(
                                obj.hitbox,
                                client_heading,
                                client_field_of_view,
                                client_view_distance,
                                client_shooter_xy):
                            board.remove_object(obj)

            # TODO give partition board to client

    def in_view(self, partition_hitbox, client_heading, client_field_of_view, client_view_distance, client_shooter_xy):
        """Returns true if any part of the partition is in view, false otherwise"""
        return arc_intersect(
            client_shooter_xy,
            client_view_distance,
            client_field_of_view,
            partition_hitbox,
            client_heading
        )

