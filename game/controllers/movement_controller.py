import math
import copy

from game.controllers.controller import Controller
from game.utils.calculate_new_location import calculate_location
from game.common.enums import *


class MovementController(Controller):

    def __init__(self):
        super().__init__()
        self.target_position = None
        self.space_free = False

    def handle_actions(self, client, game_board):
        # If statement for if client chooses move action
        if client.action._chosen_action is ActionType.move:
            client.shooter.speed = client.action.speed

            client.shooter.heading = client.action.heading
            # shooter object is removed from old location on game board to avoid object duplicates
            game_board.partition.remove_object(client.shooter)
            # variable for client's location prior to movement
            location = client.shooter.hitbox.position
            # client's desired speed
            speed = client.shooter.speed
            # Angle they want to move in radians
            angle = math.radians(client.shooter.heading)
            # new location is calculated using utils methodcalculate_slope
            self.target_location = calculate_location(location, speed, angle)
            dummy_hitbox = copy.deepcopy(client.shooter.hitbox)
            self.space_free = True
            while (not math.isclose(location[0], self.target_location[0], abs_tol=1e-01)
                    or not math.isclose(location[1], self.target_location[1], abs_tol=1e-01)
                   and self.space_free):
                new_x = round(location[0] + math.cos(angle) * .01, 2)
                new_y = round(location[1] + math.sin(angle) * .01, 2)
                try:
                    dummy_hitbox.position = (new_x, new_y)
                except ValueError:
                    self.space_free = False
                    break
                obj = game_board.partition.find_object_hitbox(dummy_hitbox)
                if obj is False or not obj.collidable:
                    try:
                        client.shooter.hitbox.position = (new_x, new_y)
                    except ValueError:
                        self.space_free = False
                        break
                    location = client.shooter.hitbox.position
                else:
                    self.space_free = False
                    break
            # gameboard is updated with new client location
            game_board.partition.add_object(client.shooter)
