from game.config import *
from game.utils.helpers import write_json_file
from game.common.game_board import GameBoard
from game.common.stats import *


def generate():
    print('Generating game map...')

    data = dict()

    #game board will have all the containers/lists 
    game_map = GameBoard()
    #separate the seed for processing    
    for x in range(1, MAX_TICKS + 1):
        game_map.circle_radius -= GameStats.circle_shrink_distance
        data[x] = game_map.to_json()

    # Verify logs location exists
    if not os.path.exists(GAME_MAP_DIR):
        os.mkdir(GAME_MAP_DIR)

    # Write game map to file
    write_json_file(data, GAME_MAP_FILE)
    
def create_structures_file(file_path, ):

