from game.controllers.controller import Controller
from game.common.enums import *
from game.common.moving.damaging.grenade import Grenade
from game.common.hitbox import Hitbox
from game.common.stats import GameStats
from game.common.moving.shooter import Shooter
import math


class GrenadeController(Controller):

    def __init__(self):
        super().__init__()
        self.x_blast_radius = 40
        self.y_blast_radius = 40
        self.grenades_on_fuse = []

    def handle_actions(self, client, game_board):
        if client.action._chosen_action is ActionType.throw_grenade:
            grenade = client.shooter.remove_grenade()
            if grenade is None:
                self.decrement_fuse(game_board)
                return None
            if not isinstance(grenade, Grenade):
                self.decrement_fuse(game_board)
                return None
            self.decrement_fuse(game_board)
            # use polar coordinate to rectangular coordinate formula to get new (x,y) for grenade
            gren_x = client.shooter.grenade_distance * \
                math.cos(client.shooter.heading) + client.shooter.hitbox.position[0]
            gren_y = client.shooter.grenade_distance * \
                math.sin(client.shooter.heading) + client.shooter.hitbox.position[1]
            if gren_x < 0:
                gren_x = 0
            if gren_y < 0:
                gren_y = 0
            if gren_x > GameStats.game_board_width:
                gren_x = 500 - grenade.hitbox.width
            if gren_y > GameStats.game_board_height:
                gren_y = 500 - grenade.hitbox.height
            grenade.hitbox.position = (gren_x, gren_y)
            self.grenades_on_fuse.append(grenade)
        else:
            self.decrement_fuse(game_board)

    def grenade_boom_boom(self, game_board, grenade):
        x_pos = grenade.hitbox.position[0] - (self.x_blast_radius // 2)
        y_pos = grenade.hitbox.position[1] - (self.y_blast_radius // 2)
        # If damage hitbox is outside game map, make it be to the edges of the map
        if x_pos < 0:
            x_pos = 0
        if y_pos < 0:
            y_pos = 0
        if x_pos > GameStats.game_board_width:
            x_pos = 500 - self.x_blast_radius
        if y_pos > GameStats.game_board_height:
            y_pos = 500 - self.y_blast_radius
        # Right side or bottom side of hitbox spawns out of bounds (fit to game border)
        while x_pos + self.x_blast_radius > GameStats.game_board_width:
            self.x_blast_radius -= 1
        while y_pos + self.y_blast_radius > GameStats.game_board_height:
            self.y_blast_radius -= 1

        grenade_boom_box = Hitbox(self.x_blast_radius, self.y_blast_radius, (x_pos, y_pos))

        collisions = game_board.partition.find_all_object_collisions(grenade_boom_box)
        # Nothing to hit in radius
        if collisions is False:
            return None
        # Deal damage
        for object in collisions:
            if object.health is None:
                continue
            object.health -= grenade.damage
            if object.health <= 0 and not isinstance(object, Shooter):
                game_board.partition.remove_object(object)

    def decrement_fuse(self, game_board):
        for grenade in self.grenades_on_fuse:
            grenade._fuse_time -= 1
            if grenade.fuse_time == 0:
                self.grenade_boom_boom(game_board, grenade)
                self.grenades_on_fuse.remove(grenade)
