from game.common.wall import *
from game.common.hitbox import *
import json


def create_structures_file(file_path):
    structure1 = []
    structure1.append(Wall(Hitbox(220, 4, (110, 138)), destructible = True))
    with open(file_path, 'w') as fl:
        json.dump(structure1[0].to_json(), fl)
    
    
def read_structures_file(file_path):
    print("MAKE ME!")
        