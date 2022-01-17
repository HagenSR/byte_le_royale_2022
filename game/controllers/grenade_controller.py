from game.controllers.controller import Controller
from game.common.enums import *
from game.common.moving.damaging.grenade import Grenade
from game.common.hitbox import Hitbox
from game.utils.collision_detection import *
import math

class GrenadeController(Controller):

    def __init__(self):
        super().__init__()
        self.blast_radius = 40
        self.grenades_on_fuse = []

    def handle_actions(self, client, distance, grenade, game_board):
        if client.action._chosen_action is ActionType.throw_grenade:
            self.decrement_fuse(game_board)
            if not isinstance(grenade, Grenade()):
                return None
            grenade = client.shooter.remove_from_inventory(grenade)
            if grenade is None:
                return None
            gren_x = distance * math.cos(client.heading)
            gren_y = distance * math.sin(client.heading)
            grenade.hitbox.position = (gren_x, gren_y)
            self.grenades_on_fuse.append(grenade)
        else:
            self.decrement_fuse(game_board)

    def grenade_boom_boom(self, game_board, grenade):
        grenade_boom_box = (grenade.hitbox.position[0] + grenade.range, grenade.hitbox.position[1] + grenade.range)
        for object in game_board.partition.get_partition_objects(grenade_boom_box[0], grenade_boom_box[1]):
            if isinstance(object, Hitbox()) and check_collision(object.hitbox, grenade.hitbox):
                object.health -= grenade.damage

    def decrement_fuse(self, game_board = None):
        for grenade in self.grenades_on_fuse:
            grenade.fuse_time -= 1
            if grenade.fuse_time == 0:
                self.grenades_on_fuse.remove(grenade)
                self.grenade_boom_boom(game_board, grenade)





