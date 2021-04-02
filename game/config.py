import os

from game.common.enums import *

# Runtime settings / Restrictions --------------------------------------------------------------------------------------
# The engine requires these to operate
MAX_TICKS = 500                                     # max number of ticks the server will run regardless of game state
TQDM_BAR_FORMAT = "Game running at {rate_fmt} "     # how TQDM displays the bar
TQDM_UNITS = " turns"                               # units TQDM takes in the bar

MAX_SECONDS_PER_TURN = 0.1                          # max number of basic operations clients have for their turns

MIN_CLIENTS_START = None                            # minimum number of clients required to start running the game; should be None when SET_NUMBER_OF_CLIENTS is used
MAX_CLIENTS_START = None                            # maximum number of clients required to start running the game; should be None when SET_NUMBER_OF_CLIENTS is used
SET_NUMBER_OF_CLIENTS_START = 2                     # required number of clients to start running the game; should be None when MIN_CLIENTS or MAX_CLIENTS are used
CLIENT_KEYWORD = "client"                           # string required to be in the name of every client file, not found otherwise
CLIENT_DIRECTORY = "./"                             # location where client code will be found

MIN_CLIENTS_CONTINUE = None                         # minimum number of clients required to continue running the game; should be None when SET_NUMBER_OF_CLIENTS is used
MAX_CLIENTS_CONTINUE = None                         # maximum number of clients required to continue running the game; should be None when SET_NUMBER_OF_CLIENTS is used
SET_NUMBER_OF_CLIENTS_CONTINUE = 2                  # required number of clients to continue running the game; should be None when MIN_CLIENTS or MAX_CLIENTS are used

ALLOWED_MODULES = ["game.client.user_client",       # modules that clients are specifically allowed to access
                   "game.common.enums"]

RESULTS_FILE_NAME = "results.json"                                  # Name and extension of results file
RESULTS_DIR = os.path.join(os.getcwd(), "logs")                     # Location of the results file
RESULTS_FILE = os.path.join(RESULTS_DIR, RESULTS_FILE_NAME)         # Results directory combined with file name

LOGS_FILE_NAME = 'turn_logs.json'
LOGS_DIR = os.path.join(os.getcwd(), "logs")                        # Directory for game log files
LOGS_FILE = os.path.join(LOGS_DIR, LOGS_FILE_NAME)

GAME_MAP_FILE_NAME = "game_map.json"                                # Name and extension of game file that holds generated world
GAME_MAP_DIR = os.path.join(os.getcwd(), "logs")                    # Location of game map file
GAME_MAP_FILE = os.path.join(GAME_MAP_DIR, GAME_MAP_FILE_NAME)      # Filepath for game map file


class Debug:                    # Keeps track of the current debug level of the game
    level = DebugLevel.none

# Other Settings Here --------------------------------------------------------------------------------------------------
