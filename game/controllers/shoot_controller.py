from game.common.moving.shooter import Shooter
from game.common.wall import Wall
from game.common.door import Door
from game.common.stats import GameStats
from game.utils.ray_utils import *
from game.controllers.controller import Controller
from game.common.enums import *


class ShootController(Controller):

    def handle_action(self, client, game_board):
        if(client.action is ActionType.shoot):
            gun = client.shooter.primary_gun
            if gun.pattern == ShotPattern.single:
                ray = get_gun_ray_collision(client, game_board)
                game_board.ray_list.append(ray)
                collision_object = ray.collision
                if(collision_object is None):
                    # no collision
                    return
                elif(isinstance(collision_object, Shooter)):
                    collision_object.health -= gun.damage
                elif(isinstance(collision_object, Wall) and collision_object.collidable is True):
                    collision_object.health -= gun.damage
                    if(collision_object.health <= 0):
                        game_board.partition.remove_object(collision_object)
                elif(isinstance(collision_object, Door) and collision_object.collidable is True):
                    collision_object.health -= gun.damage
                    if(collision_object.health <= 0):
                        game_board.partition.remove_object(collision_object)
            elif gun.pattern == ShotPattern.multi:
                for i in range(gun.fire_rate):
                    ray = get_gun_ray_collision(client, game_board)
                    game_board.ray_list.append(ray)
                    collision_object = ray.collision
                    if(collision_object is None):
                        # no collision
                        return
                    elif(isinstance(collision_object, Shooter)):
                        collision_object.health -= gun.damage
                    elif(isinstance(collision_object, Wall) and collision_object.collidable is True):
                        collision_object.health -= gun.damage
                        if(collision_object.health <= 0):
                            game_board.partition.remove_object(collision_object)
                    elif(isinstance(collision_object, Door) and collision_object.collidable is True):
                        collision_object.health -= gun.damage
                        if(collision_object.health <= 0):
                            game_board.partition.remove_object(collision_object)
            elif gun.pattern == ShotPattern.spread:
                arc_diff = (GameStats.shot_pattern_multi_arc /
                        GameStats.shot_pattern_multi_pellet_count)
                arc_start = (client.shooter.heading -
                        (GameStats.shot_pattern_multi_pellet_count / 2) * arc_diff)
                for i in range(GameStats.shot_pattern_multi_pellet_count):
                    curr_arc = arc_start + (i * arc_diff)
                    ray = get_ray_collision(
                            game_board,
                            client.shooter.hitbox.position,
                            curr_arc,
                            gun.range,
                            gun.damage /
                            GameStats.shot_pattern_multi_pellet_count,
                            [client.shooter]
                    )
                    game_board.ray_list.append(ray)
                    collision_object = ray.collision
                    if collision_object is None:
                        continue
                    elif(isinstance(ray.collision, Shooter)):
                        collision_object.health -= round(gun.damage
                                / GameStats.shot_pattern_multi_pellet_count)
                    elif(isinstance(ray.collision, Wall) and collision_object.collidable is True):
                        collision_object.health -= round(gun.damage
                                / GameStats.shot_pattern_multi_pellet_count)
                        if(collision_object.health <= 0):
                            game_board.partition.remove_object(collision_object)
                    elif(isinstance(collision_object, Door) and collision_object.collidable is True):
                        collision_object.health -= round(gun.damage
                                / GameStats.shot_pattern_multi_pellet_count)
                        if(collision_object.health <= 0):
                            game_board.partition.remove_object(collision_object)
