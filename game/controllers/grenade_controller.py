from game.controllers.controller import Controller
from game.common.enums import *
from game.common.moving.damaging.grenade import Grenade
from game.common.hitbox import Hitbox
from game.utils.collision_detection import *
from game.common.stats import GameStats
import math


class GrenadeController(Controller):

    def __init__(self):
        super().__init__()
        self.blast_radius = 40
        self.grenades_on_fuse = []

    def handle_actions(self, client, game_board):
        if client.action._chosen_action is ActionType.throw_grenade:
            grenade = client.shooter.remove_from_inventory(Grenade)
            if grenade is None:
                return None
            if not isinstance(grenade, Grenade()):
                return None
            self.decrement_fuse(game_board)
            # use polar coordinate to rectangular coordinate formula to get new (x,y) for grenade
            gren_x = client.shooter.grenade_distance * math.cos(client.heading) + client.shooter.hitbox.position[0]
            gren_y = client.shooter.grenade_distance * math.sin(client.heading) + client.shooter.hitbox.position[1]
            while gren_x < 0:
                gren_x += 1
            while gren_y < 0:
                gren_y += 1
            while gren_x > GameStats.game_board_width:
                gren_x -= 1
            while gren_y > GameStats.game_board_height:
                gren_y -= 1
            grenade.hitbox.position = (gren_x, gren_y)
            breakpoint()
            self.grenades_on_fuse.append(grenade)
        else:
            self.decrement_fuse(game_board)

    def grenade_boom_boom(self, game_board, grenade):
        grenade_boom_box = Hitbox(self.blast_radius, self.blast_radius,
                                  (grenade.hitbox.position[0] - (self.blast_radius // 2),
                                   grenade.hitbox.position[1] - (self.blast_radius//2)))
        for object in game_board.partition.get_partition_objects(grenade_boom_box.position[0], grenade_boom_box.position[1]):
            if check_collision(object.hitbox, grenade.hitbox):
                object.health -= grenade.damage

    def decrement_fuse(self, game_board = None):
        for grenade in self.grenades_on_fuse:
            grenade.fuse_time -= 1
            if grenade.fuse_time == 0:
                self.grenades_on_fuse.remove(grenade)
                self.grenade_boom_boom(game_board, grenade)





