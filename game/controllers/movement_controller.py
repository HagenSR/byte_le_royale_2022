import math

from game.common.hitbox import Hitbox
from game.controllers.controller import Controller
from game.utils.calculate_new_location import calculate_location
from game.common.moving.shooter import Shooter
from game.common.action import Action
from game.common.game_board import GameBoard
from game.common.enums import *


# May need to import player and/or shooter

class MovementController(Controller):

    def __init__(self):
        super().__init__()
        self.current_world_data = None

    def handle_actions(self, client, world):
        current_world_data = world
        # If statement for if client chooses move action
        if client.action.chosen_action is ActionType.move:
            #shooter object is removed from old location on gameboard to avoid object duplicates
            self.current_world_data["game_board"].partition.remove_object(client.shooter)
            # variable for client's location prior to movement
            location = client.shooter.hitbox.position
            # client's desired speed
            speed = client.shooter.speed
            # Angle they want to move in radians
            angle = client.shooter.heading
            # new location is calculated using utils method
            target_location = calculate_location(location, speed, angle)
            space_free = True
            while(location != target_location and space_free):
                if(self.current_world_data["game_map"].partition.find_object_coordinates(location[0], location[1]) == False):
                    new_x = location[0] + math.cos(angle)
                    new_y = location[1] + math.sin(angle)
                    client.shooter.hitbox.position = (new_x, new_y)
                    location = client.shooter.hitbox.position
                else:
                    space_free = False
            #gameboard is updated with new client location
            self.current_world_data["game_board"].partitian.add_object(client.shooter)


