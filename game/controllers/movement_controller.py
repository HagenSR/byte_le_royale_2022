from game.common.enums import *
from game.utils.collision_detection import check_collision
from game.common.game_board import GameBoard
from game.common.action import Action
from game.common.moving.shooter import Shooter
import math

from game.controllers.controller import Controller
from game.utils.calculate_new_location import calculate_location
<< << << < HEAD
== == == =
>>>>>> > f306ba3d397ca2f4d9fa022188efe859967102ca


# May need to import player and/or shooter

class MovementController(Controller):

    def __init__(self):
        super().__init__()
        self.space_free = None

    def handle_actions(self, client, world):
        # If statement for if client chooses move action
        if client.action._chosen_action is ActionType.move:
            # shooter object is removed from old location on gameboard to avoid
            # object duplicates
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
            while location != target_location and self.space_free:


<< << << < HEAD
                obj = world["game_board"].partition.find_object_hitbox(
                    client.shooter.hitbox)
                if not obj or not obj.collidable:
== == == =
                if not world["game_board"].partition.find_object_hitbox(
                        client.shooter.hitbox):
>>>>>> > f306ba3d397ca2f4d9fa022188efe859967102ca
                    new_x = location[0] + math.cos(angle)
                    new_y = location[1] + math.sin(angle)
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
            print(self.space_free)





