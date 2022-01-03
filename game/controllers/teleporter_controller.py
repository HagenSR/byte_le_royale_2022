from game.controllers.controller import Controller
import random
from game.common.enums import *
from game.common.stats import GameStats
from game.common.teleporter import Teleporter
from game.utils.collision_detection import *
from game.common.hitbox import Hitbox
import json


class TeleporterController(Controller):

    def __init__(self):
        self.teleporter_list = self.game_board_teleporters()

        # Teleporter object will be the key, value will be cooldown turns left
        self.disabled_teleporters = {}

    def handle_actions(self, client):
        if client.action._chosen_action is ActionType.use_teleporter:
            print(f'list len: {len(self.teleporter_list)}')
            # Get teleporter player is on
            for teleporter in self.teleporter_list:
                if check_collision(teleporter.hitbox, client.shooter.hitbox):
                    curr_teleporter = teleporter
            # Player is not on a teleporter
            if curr_teleporter is None:
                return None
            # Player should not be able to teleport to same location
            self.teleporter_list.remove(curr_teleporter)
            # Player should not be able to teleport to deactivated teleporter
            for teleporter in self.disabled_teleporters.keys():
                if teleporter is not curr_teleporter:
                    self.teleporter_list.remove(teleporter)
            # Determine where to teleport to
            if curr_teleporter in self.disabled_teleporters.keys():
                # Add teleporters back to list
                print('hit here')
                self.teleporter_list.append(curr_teleporter)
                for teleporter in self.disabled_teleporters.keys():
                    self.teleporter_list.append(teleporter)
                self.process_turn()
                return None
            elif len(self.teleporter_list) == 0:
                self.teleporter_list.append(curr_teleporter)
                for teleporter in self.disabled_teleporters.keys():
                    self.teleporter_list.append(teleporter)
                self.process_turn()
                return None
            elif len(self.teleporter_list) == 1:
                teleport_to = self.teleporter_list[0]
            else:
                teleport_to = random.choice(self.teleporter_list)
            client.shooter.hitbox.position = teleport_to.hitbox.position
            # Add teleporters back to list
            self.teleporter_list.append(curr_teleporter)
            for teleporter in self.disabled_teleporters.keys():
                if teleporter is not curr_teleporter:
                    self.teleporter_list.append(teleporter)
            # Decrement other teleporters cooldowns, then Disable recently used teleporter
            self.process_turn()
            self.disabled_teleporters[teleport_to] = teleport_to.turn_cooldown
            self.disabled_teleporters[curr_teleporter] = curr_teleporter.turn_cooldown
        else:
            # Teleport was not chosen action, need to decrement teleporter cooldowns
            self.process_turn()

    def game_board_teleporters(self):
        teleporter_list = []
        with open('./game_teleporters.json', 'r') as fl:
            filejsn = json.loads(fl.read())
            for entry in filejsn:
                teleporter = Teleporter(Hitbox(1, 1, (2, 2)))
                teleporter.from_json(entry)
                teleporter_list.append(teleporter)
        return teleporter_list

    # Decrement cooldown of teleporters
    def process_turn(self):
        to_remove = []
        for teleporter in self.disabled_teleporters:
            new_value = self.disabled_teleporters.get(teleporter) - 1
            if new_value == 0:
                to_remove.append(teleporter)
            else:
                self.disabled_teleporters[teleporter] = new_value
        for removal in to_remove:
            self.disabled_teleporters.pop(removal)
