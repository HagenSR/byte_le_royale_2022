import math
import copy

from game.common.stats import GameStats
from game.common.hitbox import Hitbox
from game.controllers.controller import Controller
from game.utils.calculate_new_location import calculate_location
from game.common.enums import *


class MovementController(Controller):

    def __init__(self):
        super().__init__()
        self.space_free = None

    def handle_actions(self, client, world):
        # If statement for if client chooses move action
        if client.action._chosen_action is ActionType.move:
            # shooter object is removed from old location on gameboard to avoid
            # object duplicates
            if client.shooter.speed > GameStats.player_stats["max_distance_per_turn"]:
                raise Exception(
                    "Player tried exceeding maximum distance per turn")
            world["game_board"].partition.remove_object(client.shooter)
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
                dummy_hitbox.position = (new_x, new_y)
                obj = world["game_board"].partition.find_object_hitbox(
                    dummy_hitbox)
                if not obj or not obj.collidable:
                    client.shooter.hitbox.position = (new_x, new_y)
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
            world["game_board"].partition.add_object(client.shooter)
            print('Space free? {0}'.format(self.space_free))
