from game.controllers.controller import Controller
import random
from game.common.enums import *
from game.common.teleporter import Teleporter


class TeleporterController(Controller):

    def __init__(self, game_board):
        self.enabled_teleporters = game_board.teleporter_list
        # Teleporter object will be the key, value will be cooldown turns
        self.disabled_teleporters = []

    def handle_actions(self, client, game_board):
        if client.action._chosen_action is ActionType.use_teleporter:
            # Get teleporter player is on
            curr_teleporter = game_board.partition.find_object_object(client.shooter)
            if curr_teleporter is False or isinstance(curr_teleporter, Teleporter) is False or curr_teleporter in self.disabled_teleporters:
                self.process_turn()
                return None
            # Player should not be able to teleport to same location
            self.enabled_teleporters.remove(curr_teleporter)
            # Player should not be able to teleport to deactivated teleporter
            if len(self.enabled_teleporters) == 0:
                self.enabled_teleporters.append(curr_teleporter)
                self.process_turn()
                return None
            else:
                teleport_to = random.choice(self.enabled_teleporters)
            client.shooter.hitbox.position = teleport_to.hitbox.position
            # Decrement other teleporters cooldowns, then Disable receently used teleporters
            self.process_turn()
            self.disabled_teleporters.append(teleport_to)
            self.enabled_teleporters.remove(teleport_to)
            self.disabled_teleporters.append(curr_teleporter)
            # curr_teleporter is disabled before if statement
        else:
            # Teleport was not chosen action, need to decrement teleporter cooldowns
            self.process_turn()

    # Decrement cooldown of teleporters
    def process_turn(self):
        for tel in self.disabled_teleporters:
            tel.countdown -= 1
            if tel.countdown == 0:
                self.enabled_teleporters.append(tel)
                self.disabled_teleporters.remove(tel)
                # reset possible cooldown timer
                tel.countdown = tel.turn_cooldown

