from game.config import *
from game.utils.helpers import write_json_file


def generate():
    print('Generating game map...')

    data = dict()

    for x in range(1, MAX_TICKS + 1):
        data[x] = 'data'

    # Verify logs location exists
    if not os.path.exists(GAME_MAP_DIR):
        os.mkdir(GAME_MAP_DIR)

    # Write game map to file
    write_json_file(data, GAME_MAP_FILE)
