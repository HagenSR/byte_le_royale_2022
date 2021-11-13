from game.controllers.controller import Controller
import random
from game.common.enums import *
from game.common.stats import GameStats
from game.common.teleporter import Teleporter
from game.utils.collision_detection import *

class TeleporterController(Controller):

    def __init__(self, game_board):
        self.teleporter_list = self.game_board_teleporters(game_board)

    def handle_actions(self, client, game_board):
        if client.action._chosen_action is ActionType.use_teleporter:
            curr_teleporter = None
            for teleporter in self.teleporter_list:
                if check_collision(teleporter.hitbox, client.shooter.hitbox):
                    curr_teleporter = teleporter
            if curr_teleporter is None:
                return None
            teleport_to = random.choice(self.teleporter_list.remove(curr_teleporter))
            client.shooter.hitbox.position(teleport_to.hitbox.topLeft)


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