import copy
import json
import sys
import os
import random
import importlib.resources
from game.common.hitbox import Hitbox
from game.common.items.consumable import Consumable
from game.common.items.upgrade import Upgrade
from game.common.wall import Wall
from game.common.items.gun import Gun
from game.common.items.item import Item
from game.config import *
from game.utils import collision_detection
from game.utils.helpers import write_json_file
from game.common.game_board import GameBoard
from game.common.stats import GameStats
from game.common.door import Door
from game.common.teleporter import Teleporter
import zipfile
import json
from game.utils.collision_detection import distance
import requests
import uuid


def create_structures_file(file_path):
    Structures = []
    # Structure1 has no walls
    block = [(Wall(Hitbox(140, 140, (0, 0)), destructible=True, health=300))]
    Structures.append(block)
    outlet = [
        Wall(Hitbox(50, 20, (50, 10)), destructible=True),
        Wall(Hitbox(10, 75, (30, 45)), destructible=True),
        Wall(Hitbox(10, 75, (100, 45)), destructible=True),
        Wall(Hitbox(140, 20, (0, 120)), destructible=True),
        # Door Additions
        Wall(Hitbox(5, 5, (45, 40)), destructible=True),
        Wall(Hitbox(5, 5, (100, 40)), destructible=True),
        Door(Hitbox(3, 10, (45, 30))),
        Door(Hitbox(3, 10, (100, 30)))
    ]
    Structures.append(outlet)
    the_end = [
        Wall(Hitbox(18, 18, (30, 30)), destructible=True),
        Wall(Hitbox(18, 18, (60, 30)), destructible=True),
        Wall(Hitbox(18, 18, (90, 30)), destructible=True),
        Wall(Hitbox(18, 18, (30, 60)), destructible=True),
        Wall(Hitbox(18, 18, (60, 60)), destructible=True),
        Wall(Hitbox(18, 18, (90, 60)), destructible=True),
        Wall(Hitbox(18, 18, (30, 90)), destructible=True),
        Wall(Hitbox(18, 18, (60, 90)), destructible=True),
        Wall(Hitbox(18, 18, (90, 90)), destructible=True),
        # Door Additions
        Wall(Hitbox(2, 1, (48, 46)), destructible=True),
        Door(Hitbox(10, 3, (50, 47))),
        Wall(Hitbox(2, 1, (88, 46)), destructible=True),
        Door(Hitbox(10, 3, (78, 47))),
        Wall(Hitbox(2, 1, (60, 78)), destructible=True),
        Door(Hitbox(3, 10, (61, 80))),
        Wall(Hitbox(2, 1, (106, 88))),
        Door(Hitbox(3, 10, (106, 88)))
    ]
    Structures.append(the_end)
    smile = [
        Wall(Hitbox(40, 40, (30, 20)), destructible=True),
        Wall(Hitbox(40, 40, (90, 20)), destructible=True),
        Wall(Hitbox(20, 20, (0, 60)), destructible=True),
        Wall(Hitbox(20, 20, (25, 80)), destructible=True),
        Wall(Hitbox(50, 20, (50, 100)), destructible=True),
        Wall(Hitbox(20, 20, (100, 80)), destructible=True),
        Wall(Hitbox(20, 20, (120, 60)), destructible=True),
        # Door Additions
        Wall(Hitbox(5, 5, (15, 55)), destructible=True),
        Door(Hitbox(10, 3, (20, 55))),
    ]
    Structures.append(smile)
    funnel = [
        Wall(Hitbox(15, 140, (0, 0)), destructible=True),
        Wall(Hitbox(15, 108, (16, 15)), destructible=True),
        Wall(Hitbox(15, 76, (32, 30)), destructible=True),
        Wall(Hitbox(15, 40, (48, 45)), destructible=True),
        Wall(Hitbox(15, 44, (76, 45)), destructible=True),
        Wall(Hitbox(15, 76, (92, 30)), destructible=True),
        Wall(Hitbox(15, 108, (108, 15)), destructible=True),
        Wall(Hitbox(15, 140, (124, 0)), destructible=True),
        # Door Additions
        Wall(Hitbox(5, 10, (60, 70)), destructible=True),
        Wall(Hitbox(5, 10, (80, 70)), destructible=True),
        Door(Hitbox(3, 10, (65, 75)))
    ]
    Structures.append(funnel)
    right_u = [
        Wall(Hitbox(140, 30, (0, 0)), destructible=True),
        Wall(Hitbox(30, 80, (0, 30)), destructible=True),
        Wall(Hitbox(140, 30, (0, 110)), destructible=True),
    ]
    Structures.append(right_u)
    plus_sign = [
        Wall(Hitbox(50, 40, (0, 50)), destructible=True),
        Wall(Hitbox(40, 140, (40, 0)), destructible=True),
        Wall(Hitbox(50, 40, (100, 50)), destructible=True)
    ]
    Structures.append(plus_sign)
    four_corners = [
        Wall(Hitbox(40, 40, (0, 0)), destructible=True),
        Wall(Hitbox(40, 40, (100, 0)), destructible=True),
        Wall(Hitbox(40, 40, (0, 100)), destructible=True),
        Wall(Hitbox(40, 40, (100, 100)), destructible=True)
    ]
    Structures.append(four_corners)
    structure_h = [
        Wall(Hitbox(30, 100, (0, 20)), destructible=True),
        Wall(Hitbox(80, 30, (30, 55)), destructible=True),
        Wall(Hitbox(30, 100, (110, 20)), destructible=True)
    ]
    Structures.append(structure_h)
    structure_l = [
        Wall(Hitbox(10, 140, (0, 0)), destructible=True),
        Wall(Hitbox(130, 10, (10, 130)), destructible=True)
    ]
    Structures.append(structure_l)
    reflect_l = [
        Wall(Hitbox(130, 10, (0, 0)), destructible=True),
        Wall(Hitbox(10, 140, (130, 0)), destructible=True)
    ]
    Structures.append(reflect_l)
    incomplete_x = [
        Wall(Hitbox(28, 28, (0, 0)), destructible=True),
        Wall(Hitbox(28, 28, (28, 28)), destructible=True),
        Wall(Hitbox(28, 28, (112, 0)), destructible=True),
        Wall(Hitbox(28, 28, (84, 28)), destructible=True),
        Wall(Hitbox(28, 28, (28, 84)), destructible=True),
        Wall(Hitbox(28, 28, (0, 112)), destructible=True),
        Wall(Hitbox(28, 28, (84, 84)), destructible=True),
        Wall(Hitbox(28, 28, (112, 112)), destructible=True),
        # Door Additions
        Wall(Hitbox(9, 10, (56, 42)), destructible=True),
        Wall(Hitbox(9, 10, (78, 42)), destructible=True),
        Door(Hitbox(10, 3, (65, 43))),
        Wall(Hitbox(9, 10, (56, 98)), destructible=True),
        Wall(Hitbox(9, 10, (78, 98)), destructible=True),
        Door(Hitbox(10, 3, (65, 100)))
    ]
    Structures.append(incomplete_x)
    multi_directional = [
        Wall(Hitbox(30, 40, (0, 100)), destructible=True),
        Wall(Hitbox(30, 40, (28, 0)), destructible=True),
        Wall(Hitbox(30, 40, (82, 0)), destructible=True),
        Wall(Hitbox(30, 40, (110, 100)), destructible=True),
        Wall(Hitbox(30, 30, (32, 60)), destructible=True),
        Wall(Hitbox(30, 30, (55, 110)), destructible=True),
        Wall(Hitbox(30, 30, (100, 60)), destructible=True),
        # Door Additions
        Wall(Hitbox(38, 10, (32, 50)), destructible=True),
        Door(Hitbox(3, 10, (32, 40))),
        Wall(Hitbox(38, 10, (82, 50)), destructible=True),
        Door(Hitbox(3, 10, (82, 40)))
    ]
    Structures.append(multi_directional)
    center_stage = [
        Wall(Hitbox(15, 50, (10, 10)), destructible=True),
        Wall(Hitbox(50, 15, (10, 125)), destructible=True),
        Wall(Hitbox(50, 50, (45, 45)), destructible=True),
        Wall(Hitbox(50, 15, (90, 0)), destructible=True),
        Wall(Hitbox(15, 50, (115, 95)), destructible=True)
    ]
    Structures.append(center_stage)
    random_rectangles = [
        Wall(Hitbox(40, 10, (20, 20)), destructible=True),
        Wall(Hitbox(25, 30, (80, 30)), destructible=True),
        Wall(Hitbox(50, 15, (10, 100)), destructible=True),
        Wall(Hitbox(30, 20, (70, 10)), destructible=True)
    ]
    Structures.append(random_rectangles)
    creeper_aw_man = [
        Wall(Hitbox(25, 25, (30, 30)), destructible=True),
        Wall(Hitbox(25, 25, (70, 30)), destructible=True),
        Wall(Hitbox(15, 10, (55, 55)), destructible=True),
        Wall(Hitbox(40, 35, (42, 65)), destructible=True),
        Wall(Hitbox(13, 10, (42, 100)), destructible=True),
        Wall(Hitbox(13, 10, (70, 100)), destructible=True)
    ]
    Structures.append(creeper_aw_man)
    train_station = [
        Wall(Hitbox(40, 20, (50, 0)), destructible=True),
        Wall(Hitbox(140, 45, (0, 30)), destructible=True),
        Wall(Hitbox(140, 10, (0, 100)), destructible=True),
        Wall(Hitbox(40, 20, (50, 120)), destructible=True),
        # Door Additions
        Door(Hitbox(3, 10, (70, 20))),
        Wall(Hitbox(10, 15, (65, 75)), destructible=True),
        Door(Hitbox(3, 10, (70, 80))),
        Door(Hitbox(3, 10, (70, 110)))
    ]
    Structures.append(train_station)
    blockade = [
        Wall(Hitbox(30, 30, (10, 10)), destructible=True),
        Wall(Hitbox(30, 30, (70, 10)), destructible=True),
        Wall(Hitbox(30, 30, (110, 10)), destructible=True),
        Wall(Hitbox(30, 30, (35, 60)), destructible=True),
        Wall(Hitbox(30, 30, (90, 60)), destructible=True),
        Wall(Hitbox(30, 30, (70, 100)), destructible=True),
        # Door Additions
        Wall(Hitbox(20, 10, (40, 15)), destructible=True),
        Door(Hitbox(10, 3, (60, 18))),
        Wall(Hitbox(10, 10, (50, 90)), destructible=True),
        Door(Hitbox(3, 10, (95, 40)))
    ]
    Structures.append(blockade)
    pyramid_scheme = [
        Wall(Hitbox(30, 30, (70, 10)), destructible=True),
        Wall(Hitbox(30, 30, (35, 60)), destructible=True),
        Wall(Hitbox(30, 30, (90, 60)), destructible=True),
        Wall(Hitbox(30, 30, (10, 100)), destructible=True),
        Wall(Hitbox(30, 30, (70, 100)), destructible=True),
        Wall(Hitbox(30, 30, (110, 100)), destructible=True),
        # Door Additions
        Wall(Hitbox(10, 10, (70, 50)), destructible=True),
        Door(Hitbox(3, 10, (75, 40))),
        Wall(Hitbox(20, 16, (40, 100)), destructible=True),
        Door(Hitbox(10, 3, (60, 108)))
    ]
    Structures.append(pyramid_scheme)
    battle_box = [
        Wall(Hitbox(20, 40, (0, 0)), destructible=True),
        Wall(Hitbox(100, 10, (20, 0)), destructible=True),
        Wall(Hitbox(20, 40, (120, 0)), destructible=True),
        Wall(Hitbox(20, 40, (0, 100)), destructible=True),
        Wall(Hitbox(100, 10, (20, 130)), destructible=True),
        Wall(Hitbox(20, 40, (120, 100)), destructible=True),
        # Door Additions
        Wall(Hitbox(10, 25, (5, 40)), destructible=True),
        Wall(Hitbox(10, 25, (5, 75)), destructible=True),
        Door(Hitbox(3, 10, (10, 65))),
        Wall(Hitbox(10, 25, (125, 40)), destructible=True),
        Wall(Hitbox(10, 25, (125, 75)), destructible=True),
        Door(Hitbox(3, 10, (130, 65)))
    ]
    Structures.append(battle_box)
    structure_i = [
        Wall(Hitbox(140, 20, (0, 0)), destructible=True),
        Wall(Hitbox(30, 100, (60, 20)), destructible=True),
        Wall(Hitbox(140, 20, (0, 20)), destructible=True)
    ]
    Structures.append(structure_i)
    fortified = [
        Wall(Hitbox(140, 30, (0, 0)), destructible=True),
        Wall(Hitbox(30, 110, (0, 30)), destructible=True),
        Wall(Hitbox(30, 80, (110, 30)), destructible=True),
        Wall(Hitbox(110, 30, (30, 110)), destructible=True)
    ]
    Structures.append(fortified)
    square_in_h = [
        Wall(Hitbox(35, 140, (0, 0)), destructible=True),
        Wall(Hitbox(70, 25, (35, 100)), destructible=True),
        Wall(Hitbox(35, 140, (105, 0)), destructible=True),
        Wall(Hitbox(40, 40, (55, 40)), destructible=True)
    ]
    Structures.append(square_in_h)
    structure_name_list = [
        'bloc',
        'outlet',
        'the_end',
        'smile',
        'funnel',
        'right_u',
        'plus_sign',
        'four_corners',
        'structure_h',
        'structure_l',
        'reflect_l',
        'incomplete_x',
        'multi_directional',
        'center_stage',
        'random_rectangles',
        'creeper_aw_man',
        'train_station',
        'blockade',
        'pyramid_scheme',
        'battle_box',
        'structure_i',
        'fortified',
        'square_in_h']

    # Iterate over each structure and get its walls
    for i in range(len(Structures)):
        walls = []
        doors = []
        for object in Structures[i]:
            if isinstance(object, Wall):
                walls.append(object)
            elif isinstance(object, Door):
                doors.append(object)
        with open('./structures/' + structure_name_list[i] + '.json', 'w') as fl:
            # Writes each object to json, then writes the string to file
            strs = [json.dumps(wall.to_json()) for wall in walls]
            strs += ([json.dumps(door.to_json()) for door in doors])
            s = "[%s]" % ",\n".join(strs)
            fl.write(s)


def generateRandomNumbers():
    rtn = []
    for i in range(10000):
        rtn.append(random.randint(0, sys.maxsize))
    return rtn


def findPlotHitboxes():
    plot_hitbox_list = []

    # find the width and height of each plot, assuming 6 plots on a game board
    plot_width_height = ((GameStats.game_board_width - (20 * 4)) / 3)

    # This is the top left of the first plot
    hitbox_top_left_y = GameStats.corridor_width_height
    hitbox_top_left_x = GameStats.corridor_width_height

    # Create 9 plots, but the middle one is empty
    for i in range(3):
        for y in range(3):
            # Skip the middle plot
            if i == 1 and y == 1:
                hitbox_top_left_x += plot_width_height + GameStats.corridor_width_height
                continue
            # Add the plot to the plot list, increment x position to the next
            # starting position
            plot_hitbox_list.append(
                Hitbox(
                    plot_width_height,
                    plot_width_height,
                    (hitbox_top_left_x,
                     hitbox_top_left_y)))
            hitbox_top_left_x += plot_width_height + GameStats.corridor_width_height
        # Increment y position down to the next starting position, reset X
        # position back to the starting x position
        hitbox_top_left_y += plot_width_height + GameStats.corridor_width_height
        hitbox_top_left_x = GameStats.corridor_width_height
    return plot_hitbox_list


def generate():
    print('Generating game map...')

    data = dict()

    # game board will have all the containers/lists
    game_map = GameBoard()

    structures_list = []

    # Load in all of the structures from the zipped .pyz file. Note this assumes the terminal is open at the project root
    # Use ../../launcher.pyz if opening in the utils folder or ./launcher.pyz
    # for the .pyz
    with zipfile.ZipFile('./launcher.pyz') as z:
        for filename in z.namelist():
            # Only load proper structure json
            if filename.startswith(
                    "game/utils/structures/") and filename.endswith('.json'):
                with z.open(filename, 'r') as fl:
                    # Read the zipped file, then decode it from bytes, then
                    # load it into json
                    # print(requests.get(fl.read().decode('utf-8')).content)
                    filejsn = json.loads(fl.read().decode('utf-8'))
                    wallList = []
                    for entry in filejsn:
                        # Load in every wall in the structure
                        if entry['object_type'] == ObjectType.wall:
                            wall = Wall(Hitbox(1, 1, (0, 0)))
                            wall.from_json(entry)
                            wall.id = str(uuid.uuid4())
                            wallList.append(wall)
                        elif entry['object_type'] == ObjectType.door:
                            door = Door(Hitbox(1, 1, (0, 0)))
                            door.from_json(entry)
                            door.id = str(uuid.uuid4())
                            wallList.append(door)
                    structures_list.append(wallList)
        # Plots can potentially be empty
        # structures_list.append(None)

    # Choose what structure goes in what plot
    plot_list = findPlotHitboxes()
    for plot in plot_list:
        struct = random.choice(structures_list)
        if struct:
            # Reposition structure to be on the plot
            for wall in struct:
                # A copy of wall is needed, because the original wall will
                # persist in the structures list after it's position is altered
                wall_copy = copy.deepcopy(wall)
                x_offset = plot.position[0] + wall_copy.hitbox.position[0]
                y_offset = plot.position[1] + wall_copy.hitbox.position[1]
                wall_copy.hitbox.position = (x_offset, y_offset)
                wall_copy.id = str(uuid.uuid4())
                game_map.partition.add_object(wall_copy)

    # place 5 teleporters
    for i in range(5):
        teleporter_x, teleporter_y = find_teleporter_position()
        dummy_wall = Wall(hitbox=Hitbox(10, 10, (teleporter_x, teleporter_y)))
        while game_map.partition.find_object_object(dummy_wall) \
                or teleporter_x >= GameStats.game_board_width or teleporter_y >= GameStats.game_board_height \
                or teleporter_x < 0 or teleporter_y < 0 \
                or determine_teleporter_nearby(dummy_wall, game_map):
            teleporter_x, teleporter_y = find_teleporter_position()
            dummy_wall = Wall(hitbox=(Hitbox(10, 10, (teleporter_x, teleporter_y))))
        new_tel = Teleporter(Hitbox(10, 10, (teleporter_x, teleporter_y)))
        new_tel.id = str(uuid.uuid4())
        game_map.partition.add_object(new_tel)
        game_map.teleporter_list.append(new_tel)

    # Verify logs location exists
    if not os.path.exists(GAME_MAP_DIR):
        os.mkdir(GAME_MAP_DIR)

    data['game_map'] = game_map.to_json()
    data['seed'] = generateRandomNumbers()
    # Write game map to file
    write_json_file(data, GAME_MAP_FILE)


def find_teleporter_position():
    x_pos = None
    y_pos = None
    x_corridor = random.randint(1, 4)
    y_corridor = random.randint(1, 4)
    corridor_size = GameStats.corridor_width_height
    plot_size = GameStats.plot_width_height

    if x_corridor == 1:
        x_pos = random.randint(1, GameStats.corridor_width_height - 10)
    elif x_corridor == 2:
        x_pos = random.randint(corridor_size + plot_size, corridor_size * 2 + plot_size - 10)
    elif x_corridor == 3:
        x_pos = random.randint(corridor_size * 2 + plot_size * 2, corridor_size * 3 + plot_size * 2 - 10)
    elif x_corridor == 4:
        # teleporters are 10 x 10 so they must spawn 10 left of game board width
        x_pos = random.randint(corridor_size * 3 + plot_size * 3, GameStats.game_board_width - 11)

    if y_corridor == 1:
        y_pos = random.randint(1, GameStats.corridor_width_height - 10)
    elif y_corridor == 2:
        y_pos = random.randint(corridor_size + plot_size, corridor_size * 2 + plot_size - 10)
    elif y_corridor == 3:
        y_pos = random.randint(corridor_size * 2 + plot_size * 2, corridor_size * 3 + plot_size * 2 - 10)
    elif y_corridor == 4:
        # teleporters are 10 x 10 so they must spawn 10 left of game board height
        y_pos = random.randint(corridor_size * 3 + plot_size * 3, GameStats.game_board_width - 11)

    return x_pos, y_pos


def determine_teleporter_nearby(teleporter, game_board):
    for obj in game_board.teleporter_list:
        if len(game_board.teleporter_list) < 1:
            return False
        if distance(teleporter.hitbox.middle[0], teleporter.hitbox.middle[1], obj.hitbox.middle[0],
                    obj.hitbox.middle[1]) < GameStats.min_teleporter_distance:
            return True

    return False


if __name__ == '__main__':
    create_structures_file("./structures.json")
