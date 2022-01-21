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
        #breakpoint()
        if client.action._chosen_action is ActionType.throw_grenade:
            grenade = client.shooter.remove_grenade()
            if grenade is None:
                self.decrement_fuse(game_board)
                return None
            if not isinstance(grenade, Grenade):
                self.decrement_fuse(game_board)
                return None
            #breakpoint()
            self.decrement_fuse(game_board)
            # use polar coordinate to rectangular coordinate formula to get new (x,y) for grenade
            gren_x = client.shooter.grenade_distance * math.cos(client.shooter.heading) + client.shooter.hitbox.position[0]
            gren_y = client.shooter.grenade_distance * math.sin(client.shooter.heading) + client.shooter.hitbox.position[1]
            while gren_x < 0:
                gren_x += 1
            while gren_y < 0:
                gren_y += 1
            while gren_x > GameStats.game_board_width:
                gren_x -= 1
            while gren_y > GameStats.game_board_height:
                gren_y -= 1
            grenade.hitbox.position = (gren_x, gren_y)
            #breakpoint()
            self.grenades_on_fuse.append(grenade)
        else:
            self.decrement_fuse(game_board)

    def grenade_boom_boom(self, game_board, grenade):
        breakpoint()
        grenade_boom_box = Hitbox(self.blast_radius, self.blast_radius,
                                  (grenade.hitbox.position[0] - (self.blast_radius // 2),
                                   grenade.hitbox.position[1] - (self.blast_radius // 2)))
        if grenade_boom_box.position[0] < 0:
            grenade_boom_box.position = (0, grenade_boom_box.position[1])
        if grenade_boom_box.position[1] < 0:
            grenade_boom_box.position = (grenade_boom_box.position[0], 0)
        if grenade_boom_box.position[0] > GameStats.game_board_width:
            grenade_boom_box.position = (500, grenade_boom_box.position[1])
        if grenade_boom_box.position[1] > GameStats.game_board_height:
            grenade_boom_box.position = (game_board.partition[0], 500)
        #breakpoint()
        collisions = game_board.partition.find_all_object_collisions(grenade_boom_box)
        #breakpoint()
        if collisions is False:
            return None
        for object in collisions:
            object.health -= grenade.damage

    def decrement_fuse(self, game_board):
        for grenade in self.grenades_on_fuse:
            #breakpoint()
            grenade._fuse_time -= 1

            if grenade.fuse_time == 0:
                self.grenade_boom_boom(game_board, grenade)
                self.grenades_on_fuse.remove(grenade)





