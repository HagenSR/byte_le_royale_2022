from copy import deepcopy
from game.controllers.loot_generation_controller import LootGenerationController
import random
from game.common.stats import GameStats

from game.common.action import Action
from game.common.enums import *
from game.common.player import Player
import game.config as config
from game.controllers.shop_controller import ShopController
from game.utils.threadBytel import CommunicationThread

from game.controllers.controller import Controller
from game.controllers.kill_boundary_controller import KillBoundaryController
from game.controllers.reload_controller import ReloadController
from game.controllers.loot_generation_controller import LootGenerationController
from game.controllers.teleporter_controller import TeleporterController


class MasterController(Controller):
    def __init__(self):
        super().__init__()
        self.game_over = False

        self.current_world_data = None

        self.boundary_controller = KillBoundaryController()
        self.shop_controller = ShopController()
        self.loot_generation_controller = LootGenerationController()

    # Receives all clients for the purpose of giving them the objects they
    # will control
    def give_clients_objects(self, clients):
        pass

    # Generator function. Given a key:value pair where the key is the identifier for the current world and the value is
    # the state of the world, returns the key that will give the appropriate
    # world information
    def game_loop_logic(self, start=1):
        self.turn = start
        # Basic loop from 1 to max turns
        while True:
            # Wait until the next call to give the number
            yield str(self.turn)
            # Increment the turn counter by 1
            self.turn += 1
            self.current_world_data["game_map"].circle_radius -= GameStats.circle_shrink_distance
            random.seed(self.seed)
    # Receives world data from the generated game log and is responsible for
    # interpreting it

    def interpret_current_turn_data(self, clients, world, turn):
        self.current_world_data = world
        self.seed = world["seed"][(turn % len(world['seed']))]

    # Receive a specific client and send them what they get per turn. Also
    # obfuscates necessary objects.
    def client_turn_arguments(self, client, turn):
        actions = Action()
        client.action = actions

        # Create deep copies of all objects sent to the player
        # Obfuscate data in objects that that player should not be able to see

        args = (self.turn, actions, self.current_world_data)
        return args

    # Perform the main logic that happens per turn
    def turn_logic(self, clients, turn):
        self.boundary_controller.handle_actions(
            clients, self.current_world_data["game_map"].circle_radius)

        for client in clients:
            ReloadController.handle_actions(client)
            self.shop_controller.handle_actions(client)

        if clients[0].shooter.health <= 0 or clients[1].shooter.health <= 0:
            self.game_over = True
        pass

    # Return serialized version of game
    def create_turn_log(self, clients, turn):
        data = dict()
        data['tick'] = turn
        data['clients'] = [client.to_json() for client in clients]
        # Add things that should be thrown into the turn logs here
        data['game_map'] = self.current_world_data["game_map"].to_json()

        return data

    # Gather necessary data together in results file
    def return_final_results(self, clients, turn):
        data = dict()

        data['players'] = list()
        # Determine results
        for client in clients:
            data['players'].append(client.to_json())

        return data
