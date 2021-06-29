from game.common.hitbox import Hitbox
from game.common.stats import GameStats
from game.common.enums import *


def check_collision(hitbox_one, hitbox_two):
    if (hitbox_one.topLeft[0] < hitbox_two.topRight[0] and
            hitbox_one.topRight[0] > hitbox_two.topLeft[0] and
            hitbox_one.topLeft[1] > hitbox_two.bottomLeft[1] and
            hitbox_one.bottomRight[1] < hitbox_two.topRight[1]):
        return True
    else:
        return False
