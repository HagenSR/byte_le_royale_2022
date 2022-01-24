from game.controllers.controller import Controller
from game.common.enums import *
from game.common.moving.damaging.grenade import Grenade
from game.common.hitbox import Hitbox
from game.common.stats import GameStats
from game.common.moving.shooter import Shooter
from game.utils import collision_detection
import math


class GrenadeController(Controller):

    def __init__(self):
        super().__init__()
        self.blast_radius = GameStats.blast_radius
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
            gren_x = client.action.grenade_distance * \
                math.cos(math.radians(client.shooter.heading)) + client.shooter.hitbox.position[0]
            gren_y = client.action.grenade_distance * \
                math.sin(math.radians(client.shooter.heading)) + client.shooter.hitbox.position[1]
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
        # Check all partitions, if a partition isn't in view, dont include it
        already_damaged = []
        for x in range(0, GameStats.game_board_width, game_board.partition.partition_width):
            for y in range(
                    0,
                    GameStats.game_board_height,
                    game_board.partition.partition_height):
                for obj in game_board.partition.get_partition_objects(x, y):
                    if collision_detection.intersect_circle(
                        (grenade.hitbox.position[0] +
                         grenade.hitbox.width //
                         2,
                         grenade.hitbox.position[1] +
                         grenade.hitbox.height //
                         2),
                        self.blast_radius,
                            obj.hitbox):
                        if obj.health is None or obj in already_damaged:
                            continue
                        obj.health -= grenade.damage
                        already_damaged.append(obj)
                        if obj.health <= 0 and not isinstance(obj, Shooter):
                            game_board.partition.remove_object(obj)

    def decrement_fuse(self, game_board):
        for grenade in self.grenades_on_fuse:
            grenade.fuse_time -= 1
            if grenade.fuse_time == 0:
                self.grenade_boom_boom(game_board, grenade)
                self.grenades_on_fuse.remove(grenade)
