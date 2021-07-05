import copy
import json
import os
import random
import importlib.resources
from game.common.hitbox import Hitbox
from game.common.wall import Wall
from game.config import *
from game.utils.helpers import write_json_file
from game.common.game_board import GameBoard
from game.common.stats import GameStats
import zipfile
import json


def create_structures_file(file_path):
    structures = []
    structures.append(Wall(Hitbox(100, 4, (0, 0)), destructible=True))
    with open(file_path, 'w') as fl:
        # Writes each object to json, then writes the string to file
        strs = [json.dumps(wall.to_json()) for wall in structures]
        s = "[%s]" % ",\n".join(strs)
        fl.write(s)


def read_structures_file(file_path):
    print("MAKE ME!")

def findPlotHitboxes():
    plot_hitbox_list = []

    # find the width and height of each plot, assuming 6 plots on a game board
    plot_width_hieght = ((GameStats.game_board_width - (20 * 4)) / 3)

    # This is the top left of the first plot
    hitbox_top_right_y = GameStats.corridor_width_height
    hitbox_top_right_x = GameStats.corridor_width_height

    # Create 9 plots, but the middle one is empty
    for i in range(3):
        for y in range(3):
            # Skip the middle plot
            if i == 1 and y == 1:
                hitbox_top_right_x += plot_width_hieght + GameStats.corridor_width_height
                continue
            # Add the plot to the plot list, increment x position to the next starting position
            plot_hitbox_list.append(Hitbox(plot_width_hieght, plot_width_hieght, (hitbox_top_right_x, hitbox_top_right_y)))
            hitbox_top_right_x += plot_width_hieght + GameStats.corridor_width_height
        # Increment y position down to the next starting position, reset X position back to the starting x position
        hitbox_top_right_y += plot_width_hieght + GameStats.corridor_width_height
        hitbox_top_right_x = GameStats.corridor_width_height
    return plot_hitbox_list


def generate():
    print('Generating game map...')

    data = dict()

    # game board will have all the containers/lists
    game_map = GameBoard()

    structuresList = []

    # Load in all of the structures from the zipped .pyz file. Note this assumes the terminal is open at the project root
    # Use ../../launcher.pyz if opening in the utils folder
    with zipfile.ZipFile('launcher.pyz') as z:
        wallList = []
        for filename in z.namelist():
            # Only load proper structure json
            if filename.startswith("game/utils/structures/") and filename.endswith('.json'):
                with z.open(filename, 'r') as fl:
                    # Read the zipped file, then decode it from bytes, then load it into json
                    filejsn = json.loads(fl.read().decode('utf-8'))
                    for entry in filejsn:
                        # Load in every wall in the structure
                        wall = Wall(Hitbox(1,1,(0,0)))
                        wall.from_json(entry)
                        wallList.append(wall)
                    structuresList.append(wallList)
         # Plots can potentially be empty
        structuresList.append(None)

    # Choose what structure goes in what plot
    plot_list = findPlotHitboxes()
    for plot in plot_list:
        struct = random.choice(structuresList)
        if struct:
            # Reposition structure to be on the plot
            for wall in struct:
                # A copy of wall is needed, because the original wall will persist in the structures list after it's position is altered
                wall_copy = copy.deepcopy(wall)
                x_offset = plot.position[0] + wall_copy.hitbox.position[0]
                y_offset = plot.position[1] + wall_copy.hitbox.position[1]
                wall_copy.position = (x_offset, y_offset)
                game_map.wall_list.append(wall_copy)

    # Verify logs location exists
    if not os.path.exists(GAME_MAP_DIR):
        os.mkdir(GAME_MAP_DIR)

    data['game_map'] = game_map.to_json()
    # Write game map to file
    write_json_file(data, GAME_MAP_FILE)


if __name__ == '__main__':
    generate()
