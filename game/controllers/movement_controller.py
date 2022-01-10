import math
import copy

from game.controllers.controller import Controller
from game.utils.calculate_new_location import calculate_location
from game.common.enums import *


class MovementController(Controller):

    def __init__(self):
        super().__init__()
        self.space_free = None

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
            angle = client.shooter.heading
            # new location is calculated using utils method
            target_location = calculate_location(location, speed, angle)
            self.space_free = True
            dummy_hitbox = copy.deepcopy(client.shooter.hitbox)
            while location != target_location and self.space_free:
                location = client.shooter.hitbox.position
                new_x = location[0] + math.cos(angle)
                new_y = location[1] + math.sin(angle)
                try:
                    dummy_hitbox.position = (new_x, new_y)
                except ValueError:
                    self.space_free = False
                obj = game_board.partition.find_object_hitbox(
                    dummy_hitbox)
                if not obj or not obj.collidable:
                    try:
                        client.shooter.hitbox.position = (new_x, new_y)
                    except ValueError:
                        self.space_free = False
                    if abs(
                            new_x -
                            target_location[0]) < 0.00001 and abs(
                            new_y -
                            target_location[1]) < 0.00001:
                        client.shooter.hitbox.position = target_location
                    location = client.shooter.hitbox.position
                else:
                    self.space_free = False
            # gameboard is updated with new client location
            game_board.partition.add_object(client.shooter)
