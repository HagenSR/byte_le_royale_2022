import os

from game.common.enums import *

# Runtime settings / Restrictions ----------------------------------------
# The engine requires these to operate
# max number of ticks the server will run regardless of game state
MAX_TICKS = 500
TQDM_BAR_FORMAT = "Game running at {rate_fmt} "  # how TQDM displays the bar
TQDM_UNITS = " ticks"  # units TQDM takes in the bar

# max number of basic operations clients have for their turns
MAX_SECONDS_PER_TURN = 0.1

# minimum number of clients required to start running the game; should be
# None when SET_NUMBER_OF_CLIENTS is used
MIN_CLIENTS_START = None
# maximum number of clients required to start running the game; should be
# None when SET_NUMBER_OF_CLIENTS is used
MAX_CLIENTS_START = None
# required number of clients to start running the game; should be None
# when MIN_CLIENTS or MAX_CLIENTS are used
SET_NUMBER_OF_CLIENTS_START = 2
# string required to be in the name of every client file, not found otherwise
CLIENT_KEYWORD = "client"
# location where client code will be found
CLIENT_DIRECTORY = "./"

# minimum number of clients required to continue running the game; should
# be None when SET_NUMBER_OF_CLIENTS is used
MIN_CLIENTS_CONTINUE = None
# maximum number of clients required to continue running the game; should
# be None when SET_NUMBER_OF_CLIENTS is used
MAX_CLIENTS_CONTINUE = None
# required number of clients to continue running the game; should be None
# when MIN_CLIENTS or MAX_CLIENTS are used
SET_NUMBER_OF_CLIENTS_CONTINUE = 2

ALLOWED_MODULES = ["game.client.user_client",  # modules that clients are specifically allowed to access
                   "game.common.enums",
                   "math",
                   "game.common.action",
                   "game.common.moving.shooter",
                   "game.utils.partition_grid",
                   "game.utils.collision_detection",
                   "game.utils.player_utils"]

# Name and extension of results file
RESULTS_FILE_NAME = "results.json"
# Location of the results file
RESULTS_DIR = os.path.join(os.getcwd(), "logs")
# Results directory combined with file name
RESULTS_FILE = os.path.join(RESULTS_DIR, RESULTS_FILE_NAME)

LOGS_FILE_NAME = 'turn_logs.json'
# Directory for game log files
LOGS_DIR = os.path.join(os.getcwd(), "logs")
LOGS_FILE = os.path.join(LOGS_DIR, LOGS_FILE_NAME)

# Name and extension of game file that holds generated world
GAME_MAP_FILE_NAME = "game_map.json"
# Location of game map file
GAME_MAP_DIR = os.path.join(os.getcwd(), "logs")
# Filepath for game map file
GAME_MAP_FILE = os.path.join(GAME_MAP_DIR, GAME_MAP_FILE_NAME)


class Debug:  # Keeps track of the current debug level of the game
    level = DebugLevel.none

# Other Settings Here ----------------------------------------------------
