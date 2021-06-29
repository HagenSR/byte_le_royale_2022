import json
import os
import random

from game.common.hitbox import Hitbox
from game.common.wall import Wall
from game.config import *
from game.utils.helpers import write_json_file
from game.common.game_board import GameBoard
from game.common.stats import GameStats
import json


def create_structures_file(file_path):
    structures = []
    structures.append(Wall(Hitbox(220, 4, (110, 138)), destructible=True))
    structures.append(Wall(Hitbox(4, 220, (2, 110)), destructible=True))
    with open(file_path, 'w') as fl:
        # Writes each object to json, then writes the string to file
        strs = [json.dumps(wall.to_json()) for wall in structures]
        s = "[%s]" % ",\n".join(strs)
        open(file_path, 'w').write(s)


def read_structures_file(file_path):
    print("MAKE ME!")

def findPlotHitboxes():
    plotHitboxList = []

    # find the width and height of each plot, assuming 6 plots on a game board
    plotWidth = ((GameStats.game_board_width - (20 * 3)) / 2)
    plotHeight = ((GameStats.game_board_height - (20*4)) / 3)

    # This is the middle of the first plot, Top Left
    hitboxTopRightYLeft = (plotHeight / 2) + 20
    hitboxTopRightXLeft = (plotWidth/2) + 20
    for i in range(3):
        # For the left plot
        plotHitboxList.append(Hitbox(plotWidth, plotHeight, (hitboxTopRightXLeft, hitboxTopRightYLeft)))
        # The right plot is one game plot + 20 over
        plotHitboxList.append(Hitbox(plotWidth, plotHeight, ((hitboxTopRightXLeft + plotWidth + 20), hitboxTopRightYLeft)))
        hitboxTopRightYLeft += plotHeight + 20
    return plotHitboxList


def generate():
    print('Generating game map...')

    data = dict()

    # game board will have all the containers/lists
    game_map = GameBoard()

    plotsList = findPlotHitboxes()

    structuresList = []

    # Need to figure out how to access structures folder
    structPath = './launcher.pyz/game/utils/structures'

    # Load in all of the structures
    for file in os.listdir(structPath):
        wallList = []
        with open(structPath.format(file)) as fl:
            filejsn = json.load(fl)
            for entry in filejsn:
                wall = Hitbox(1,1,(0,0))
                wall.from_json(entry)
                wallList.append(wall)
            structuresList.append(wallList)
    # Plots can potentially be empty
    structuresList.append(None)

    # Choose what structure goes in what plot
    for plot in findPlotHitboxes():
        struct = random.choice(structuresList)
        if struct:
            # Add offset to every wall and add to game map walls list
            for wall in struct:
                offsetX = wall.position[0] + plot.position[0]
                offsetY = wall.position[1] + plot.position[1]
                wall.position = (offsetX, offsetY)
                game_map.wall_list.append(wall)

    # Verify logs location exists
    if not os.path.exists(GAME_MAP_DIR):
        os.mkdir(GAME_MAP_DIR)

    # Write game map to file
    write_json_file(data, GAME_MAP_FILE)


if __name__ == '__main__':
    generate()
