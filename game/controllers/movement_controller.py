import math

from game.common.hitbox import Hitbox
from game.controllers.controller import Controller
from game.common.moving.shooter import Shooter
from game.common.action import Action
from game.utils.collision_detection import check_collision
from game.common.enums import *


# May need to import player and/or shooter

class MovementController(Controller):

    def __init__(self):
        super().__init__()

    def handle_actions(self, client, world):
        # If statement for if client chooses move action
        if client.action.chosen_action is ActionType.move:
            # client's shooter object moving attribute turns true
            client.shooter.moving = True
            target_location = self.calculate_location(client)

    # eventually move to utils
    def calculate_location(self, client):
        # original location as xy point
        origin = client.shooter.hitbox.middle
        speed = client.shooter.speed
        angle = client.shooter.heading
        new_x = origin[0] + (speed * math.cos(angle))
        new_y = origin[1] + (speed * math.sin(angle))

        return new_x, new_y
