import time

from game.controllers.controller import Controller
import random
from game.common.enums import *
from game.common.stats import GameStats
from game.common.teleporter import Teleporter
from game.utils.collision_detection import *
import asyncio


class TeleporterController(Controller):

    def __init__(self, game_board):
        self.teleporter_list = self.game_board_teleporters(game_board)
        # Teleporter object will be the key, value will be cooldown turns
        self.disabled_teleporters = {}

    def handle_actions(self, client):
        if client.action._chosen_action is ActionType.use_teleporter:
            # Get teleporter player is on
            for teleporter in self.teleporter_list:
                if check_collision(teleporter.hitbox, client.shooter.hitbox):
                    curr_teleporter = teleporter
            # Player is not on a teleporter
            if curr_teleporter is None:
                return None
            # Player should not be able to teleport to same location
            self.teleporter_list.remove(curr_teleporter)
            if curr_teleporter in self.disabled_teleporters:
                self.teleporter_list.append(curr_teleporter)
                return None
            elif len(self.teleporter_list) == 0:
                return None
            elif len(self.teleporter_list) == 1:
                teleport_to = self.teleporter_list[0]
            else:
                teleport_to = random.choice(self.teleporter_list)
            client.shooter.hitbox.position = teleport_to.hitbox.position
            self.teleporter_list.append(curr_teleporter)
            # Decrement other teleporters cooldowns, then Disable receently used teleporter
            self.process_turn()
            self.disabled_teleporters[teleport_to] = teleport_to.turn_cooldown
        else:
            # Teleport was not chosen action, need to decrement teleporter cooldowns
            self.process_turn()

    def game_board_teleporters(self, game_board):
        teleporter_list = []
        for x in range(0, GameStats.game_board_width,
                       game_board.partition.partition_width):
            for y in range(0, GameStats.game_board_height,
                           game_board.partition.partition_height):
                for object in game_board.partition.get_partition_objects(x, y):
                    if isinstance(object, Teleporter):
                        teleporter_list.append(object)
        return teleporter_list

    # Decrement cooldown of teleporters
    def process_turn(self):
        for teleporter in self.disabled_teleporters:
            new_value = self.disabled_teleporters.get(teleporter) - 1
            if new_value == 0:
                self.disabled_teleporters.pop(teleporter)
            else:
                self.disabled_teleporters[teleporter] = new_value


