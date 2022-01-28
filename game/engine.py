from datetime import datetime
from game.common.stats import GameStats
from game.common.moving.shooter import Shooter
import importlib
import json
import os
import sys
import traceback

from game.common.player import Player
from game.common.game_board import GameBoard
from game.common.hitbox import Hitbox

from game.config import *
from game.controllers.master_controller import MasterController
from game.utils.helpers import write_json_file
from game.utils.engine_thread import Thread, CommunicationThread
from game.utils.validation import verify_code, verify_num_clients

from tqdm import tqdm


class Engine:
    def __init__(self, quiet_mode=False, use_filenames_as_team_names=False):
        self.clients = list()
        self.master_controller = MasterController()
        self.tick_number = 0

        self.game_logs = dict()
        self.world = dict()
        self.current_world_key = None

        self.quiet_mode = quiet_mode
        self.use_filenames = use_filenames_as_team_names

        # Delete logs, then recreate logs dir
        for file in os.scandir(LOGS_DIR):
            if ('map' not in file.path):
                os.remove(file.path)

    # Starting point of the engine. Runs other methods then sits on top of a
    # basic game loop until over
    def loop(self):
        # If quiet mode is activated, replace stdout with devnull
        error = ""
        try:
            f = sys.stdout
            if self.quiet_mode:
                f = open(os.devnull, 'w')
                sys.stdout = f
            self.boot()
            self.load()
            for self.current_world_key in tqdm(
                    self.master_controller.game_loop_logic(),
                    bar_format=TQDM_BAR_FORMAT,
                    unit=TQDM_UNITS,
                    file=f):
                self.pre_tick()
                self.tick()
                self.post_tick()
                if self.tick_number >= MAX_TICKS:
                    break
        except Exception as e:
            print(str(e))
        finally:
            self.shutdown()

    # Finds, checks, and instantiates clients
    def boot(self):
        # Insert path of where clients are expected to be inside where python
        # will look
        current_dir = os.getcwd()
        sys.path.insert(0, current_dir)
        sys.path.insert(0, f'{current_dir}/{CLIENT_DIRECTORY}')

        # Find and load clients in
        for filename in os.listdir(CLIENT_DIRECTORY):
            try:
                filename = filename.replace('.py', '')

                # Filter out files that do not contain CLIENT_KEYWORD in their
                # filename (located in config)
                if CLIENT_KEYWORD.upper() not in filename.upper():
                    continue

                # Filter out folders
                if os.path.isdir(os.path.join(CLIENT_DIRECTORY, filename)):
                    continue

                # Otherwise, instantiate the player
                # Add players one and two
                player = Player()
                self.clients.append(player)

                # Verify client isn't using invalid imports or opening anything
                imports, opening, printing = verify_code(filename + '.py')
                if len(imports) != 0:
                    player.functional = False
                    player.error = f'Player has attempted illegal imports: {imports}'

                if opening:
                    player.functional = False
                    player.error = PermissionError(
                        f'Player is using "open" which is forbidden.')

                # Attempt creation of the client object
                obj = None
                try:
                    # Import client's code
                    im = importlib.import_module(f'{filename}', CLIENT_DIRECTORY)
                    obj = im.Client()
                except Exception:
                    player.functional = False
                    player.error = str(traceback.format_exc())

                player.code = obj
                thr = None
                try:
                    # Retrieve team name
                    thr = CommunicationThread(player.code.team_name, list(), str)
                    thr.start()
                    thr.join(0.01)  # Shouldn't take long to get a string

                    if thr.is_alive():
                        player.functional = False
                        player.error = TimeoutError(
                            'Client failed to provide a team name in time.')

                    if thr.error is not None:
                        player.functional = False
                        player.error = thr.error
                finally:
                    # Note: I keep the above thread for both naming conventions to check for client errors
                    try:
                        if self.use_filenames:
                            player.team_name = filename
                            thr.retrieve_value()
                        else:
                            player.team_name = thr.retrieve_value()
                    except Exception as e:
                        player.functional = False
                        player.error = str(e)
            except Exception:
                print(f"Bad client for {filename}")

        self.clients.sort(key=lambda clnt: clnt.team_name, reverse=True)
        # Verify correct number of clients have connected to start
        func_clients = [client for client in self.clients if client.functional]
        client_num_correct = verify_num_clients(func_clients,
                                                SET_NUMBER_OF_CLIENTS_START,
                                                MIN_CLIENTS_START,
                                                MAX_CLIENTS_START)

        if client_num_correct is not None:
            self.shutdown(source='Client_error')

        # Finally, request master controller to establish clients with basic
        # objects
        if SET_NUMBER_OF_CLIENTS_START == 1:
            self.master_controller.give_clients_objects(self.clients[0])
        else:
            self.master_controller.give_clients_objects(self.clients)

    # Loads in the world
    def load(self):
        # Verify the log directory exists
        if not os.path.exists(LOGS_DIR):
            raise FileNotFoundError('Log directory not found.')

        # Verify the game map exists
        if not os.path.exists(GAME_MAP_FILE):
            raise FileNotFoundError('Game map not found.')

        # Delete previous logs
        if os.path.exists(LOGS_FILE):
            os.remove(LOGS_FILE)

        with open(GAME_MAP_FILE) as json_file:
            world = json.load(json_file)
        # Yes, this is a bit ugly. Load game map json to game map object
        gameBoard = GameBoard()
        game_map = gameBoard.from_json(world['game_map'])

        # add game map object to dictionary
        world.pop("game_map", None)
        self.world["game_map"] = game_map
        self.world['seed'] = world['seed']

        # attach shooters to the game map
        for client in self.clients:
            self.world["game_map"].partition.add_object(client.shooter)

    # Sits on top of all actions that need to happen before the player takes
    # their turn
    def pre_tick(self):
        # Increment the tick
        self.tick_number += 1

        # game map isn't tick based, only need the previous game map to persist
        # Retrieve current world info
        # if self.current_world_key not in self.world:
        #     raise KeyError('Given generated world key does not exist inside the world.')
        # current_world = self.world['game_map']

        # Send current world information to master controller for purposes
        if SET_NUMBER_OF_CLIENTS_START == 1:
            self.master_controller.interpret_current_turn_data(
                self.clients[0], self.world, self.tick_number)
        else:
            self.master_controller.interpret_current_turn_data(
                self.clients, self.world, self.tick_number)

    # Does actions like lets the player take their turn and asks master
    # controller to perform game logic
    def tick(self):
        # Create list of threads to run client's code
        threads = list()
        for client in self.clients:
            # Skip non-functional clients
            if not client.functional:
                continue

            # Retrieve list of arguments to pass
            arguments = self.master_controller.client_turn_arguments(
                client, self.tick_number)

            # Create the thread, pass the arguments
            thr = Thread(func=client.code.take_turn, args=arguments)
            threads.append(thr)

        # Start all threads
        [thr.start() for thr in threads]

        # Time and wait for clients to be done
        start_time = datetime.now()
        for thr in threads:
            # We only want to wait a maximum of MAX_SECONDS_PER_TURN once all of the clients have started.
            # However, we can't simultaneously join threads without more threads or multiprocessing.
            # Solution: join one thread at a time, keep track of total running time between each join, and reduce the
            # join time so it is always less than MAX_SECONDS_PER_TURN.
            # Get time elapsed in microseconds
            time_elapsed = datetime.now().microsecond - start_time.microsecond
            # Convert to seconds
            time_elapsed /= 1000000
            # Subtract value from MAX_SECONDS_PER_TURN to get time remaining
            time_remaining = MAX_SECONDS_PER_TURN - time_elapsed
            # Ensure value never goes negative
            time_remaining = max(0.0, time_remaining)

            thr.join(time_remaining)

        # Go through each thread and check if they are still alive
        for client, thr in zip(self.clients, threads):
            # If thread is no longer alive, mark it as non-functional,
            # preventing it from receiving future turns
            if thr.is_alive():
                client.functional = False
                client.error = str(TimeoutError(
                    f'{client.id} failed to reply in time and has been dropped.'))
                print(client.error)

            # Also check to see if the client had created an error and save it
            if thr.error is not None:
                client.functional = False
                client.error = str(thr.error)
                print(thr.error)

        # Verify there are enough clients to continue the game
        func_clients = [client for client in self.clients if client.functional]
        client_num_correct = verify_num_clients(func_clients,
                                                SET_NUMBER_OF_CLIENTS_CONTINUE,
                                                MIN_CLIENTS_CONTINUE,
                                                MAX_CLIENTS_CONTINUE)
        if client_num_correct is not None:
            self.shutdown(source='Client_error')

        # Finally, consult master controller for game logic
        if SET_NUMBER_OF_CLIENTS_START == 1:
            self.master_controller.turn_logic(
                self.clients[0], self.tick_number)
        else:
            self.master_controller.turn_logic(self.clients, self.tick_number)

    # Does any actions that need to happen after the game logic, then creates
    # the game log for the turn
    def post_tick(self):
        # Add logs to logs list
        data = None
        if SET_NUMBER_OF_CLIENTS_START == 1:
            data = self.master_controller.create_turn_log(
                self.clients[0], self.tick_number)
        else:
            data = self.master_controller.create_turn_log(
                self.clients, self.tick_number)

        # self.game_logs[self.tick_number] = data

        with open(os.path.join(LOGS_DIR, f"turn_{self.tick_number:04d}.json"), 'w+') as f:
            json.dump(data, f)

        # Perform a game over check
        if self.master_controller.game_over:
            self.shutdown()

        # Perform a game over check
        if self.master_controller.game_over:
            self.shutdown()

    # Attempts to safely handle an engine shutdown given any game state
    def shutdown(self, source=None):

        # Retrieve and write results information
        results_information = None
        if SET_NUMBER_OF_CLIENTS_START == 1:
            results_information = self.master_controller.return_final_results(
                self.clients[0], self.tick_number)
        else:
            results_information = self.master_controller.return_final_results(
                self.clients, self.tick_number)
        if source:
            results_information['reason'] = source

        write_json_file(results_information, RESULTS_FILE)

        # Exit game
        if source:
            print(f'\nGame has ended due to {source}.')

            # Flush standard out
            sys.stdout.flush()

            os._exit(1)
        else:
            print(f'\nGame has successfully ended.')

            # Flush standard out
            sys.stdout.flush()

            os._exit(0)

    # Debug print statement
    def debug(*args):
        if Debug.level >= DebugLevel.engine:
            print('Engine: ', end='')
            print(*args)
