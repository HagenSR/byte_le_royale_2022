from copy import deepcopy
from math import trunc
import random

from game.common.hitbox import Hitbox
from game.common.items.gun import Gun
from game.common.moving.shooter import Shooter
from game.common.stats import GameStats
from game.common.action import Action
from game.controllers.interact_controller import InteractController
from game.common.enums import *
from game.controllers.shop_controller import ShopController
from game.controllers.use_controller import UseController
from game.controllers.shoot_controller import ShootController
from game.controllers.controller import Controller
from game.controllers.kill_boundary_controller import KillBoundaryController
from game.controllers.reload_controller import ReloadController
from game.controllers.loot_generation_controller import LootGenerationController
from game.controllers.teleporter_controller import TeleporterController
from game.controllers.movement_controller import MovementController


class MasterController(Controller):
    def __init__(self):
        super().__init__()
        self.game_over = False

        self.current_world_data = None

        self.boundary_controller = KillBoundaryController()
        self.shop_controller = ShopController()

        self.movement_controller = MovementController()
        self.seed = -1
        self.turn = 1
        self.shoot_controller = ShootController()
        self.loot_generation_controller = LootGenerationController()

        self.instantiated_teleporter_controller = False
        self.teleporter_controller = None

        self.use_controller = UseController()
        self.interact_controller = InteractController()

    # Receives all clients for the purpose of giving them the objects they
    # will control
    def give_clients_objects(self, clients):
        for index, client in enumerate(clients):
            ar = GameStats.player_stats["hitbox"][index]
            hit = Hitbox(ar[0], ar[1], (ar[2], ar[3]))
            client.shooter = Shooter(hitbox=hit)
            client.shooter.append_inventory(Gun(GunType.handgun, 1, Hitbox(0, 0, (0, 0))))

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

        if not self.instantiated_teleporter_controller:
            self.teleporter_controller = TeleporterController(self.current_world_data['game_map'])
            self.instantiated_teleporter_controller = True

    # Receive a specific client and send them what they get per turn. Also
    # obfuscates necessary objects.
    def client_turn_arguments(self, client, turn):
        actions = Action()
        client.action = actions

        # Create deep copies of all objects sent to the player
        game_board = deepcopy(self.current_world_data["game_map"])

        # Obfuscate data in objects that that player should not be able to see
        game_board.obfuscate()
        game_board.partition.obfuscate(client)
        shooter = deepcopy(client.shooter)

        args = (self.turn, actions, game_board, game_board.partition, shooter)
        return args

    # Perform the main logic that happens per turn
    def turn_logic(self, clients, turn):
        # clear ray list of any rays from previous ticks
        self.current_world_data["game_map"].ray_list = []
        self.boundary_controller.handle_actions(
            clients, self.current_world_data["game_map"].circle_radius)
        self.loot_generation_controller.handle_actions(
            self.current_world_data['game_map'])

        for client in clients:
            try:
                self.shoot_controller.handle_action(
                    client, self.current_world_data["game_map"])
                self.movement_controller.handle_actions(
                    client, self.current_world_data["game_map"])
                self.use_controller.handle_actions(client)
                self.shop_controller.handle_actions(client)
                ReloadController.handle_actions(client)
                self.teleporter_controller.handle_actions(
                    client, self.current_world_data['game_map'])
                self.interact_controller.handle_actions(
                    client, self.current_world_data["game_map"])
            except Exception as e:
                self.game_over = True
                client.shooter.health = 0
                print(f"Client {client.team_name} Raised an exception and lost")
                break

        if clients[0].shooter.health <= 0 or clients[1].shooter.health <= 0:
            self.game_over = True

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
        # Most of this is for the client runner, and ensuring a broken client results in that client losing
        data['players'] = list()
        data['errors'] = [(player.team_name, str(player.error)) for player in clients if player.error is not None]
        data['no_errors'] = [player.team_name for player in clients if player.error is None]
        data['players_dead'] = []
        data['players_alive'] = []
        if len(data['errors']) == 0:
            data["players_dead"] = [player.team_name for player in filter(
                lambda p: p.error is not None or p.shooter.health <= 0, clients)]
            data["players_alive"] = [player.team_name for player in filter(
                lambda p: p.error is None and p.shooter.health > 0, clients)]
            if len(data["players_alive"]) > 0:
                print(f"\nGame is ending because player "
                      f"{data['players_dead']} "
                      f"is out of health or raised an error, player "
                      f"{data['players_alive']} "
                      f"wins")
            else:
                print(f"\nGame is ending both players are out of health, the game is a tie.")
        else:
            if len(data["errors"]) == 1:
                print(f"\nGame is ending because player "
                      f"{data['errors'][0][0]} "
                      f"is raised an error, player "
                      f"{data['no_errors'][0]} "
                      f"wins")
            else:
                print(f"\nGame is ending both players errored")
            data["players_alive"] += data["no_errors"]
            data["players_dead"] += [player[0] for player in data["errors"]]
        # Determine results
        for client in clients:
            data['players'].append(client.to_json())

        return data
