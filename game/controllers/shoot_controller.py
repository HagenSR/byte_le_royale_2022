from game.common.moving.shooter import Shooter
from game.common.wall import Wall
from game.common.door import Door
from game.common.stats import GameStats
from game.utils.ray_utils import *
from game.controllers.controller import Controller
from game.common.enums import *


def apply_damage(collision_object, ray, gun, game_board, pellet_count):
    if collision_object is None:
        # no collision
        return
    elif isinstance(ray.collision, Shooter):
        collision_object.health -= round(
            gun.damage / pellet_count)
    elif isinstance(ray.collision, Wall):
        collision_object.health -= round(
            gun.damage / pellet_count)
        if collision_object.health <= 0:
            game_board.partition.remove_object(
                collision_object)
    elif isinstance(collision_object, Door):
        collision_object.health -= round(
            gun.damage / pellet_count)
        if collision_object.health <= 0:
            game_board.partition.remove_object(
                collision_object)


class ShootController(Controller):
    def __init__(self):
        super().__init__()

    def handle_action(self, client, game_board):
        if client.action._chosen_action is ActionType.shoot:
            client.shooter.heading = client.action.heading
            if client.shooter.primary_gun.mag_ammo <= 0:
                return
            gun = client.shooter.primary_gun
            if not gun:
                raise AttributeError("Client tried to shoot but doesn't have a primary gun equipped")
            if gun.pattern == ShotPattern.single:
                ray = get_gun_ray_collision(client, game_board)
                game_board.ray_list.append(ray)
                collision_object = ray.collision
                apply_damage(collision_object, ray, gun, game_board, 1)
                gun.mag_ammo -= 1
            elif gun.pattern == ShotPattern.multi:
                for i in range(gun.fire_rate):
                    ray = get_gun_ray_collision(client, game_board)
                    game_board.ray_list.append(ray)
                    collision_object = ray.collision
                    apply_damage(collision_object, ray, gun, game_board, 1)
                    gun.mag_ammo -= 1
            elif gun.pattern == ShotPattern.spread:
                arc_diff = (GameStats.shot_pattern_multi_arc /
                            gun.fire_rate)
                arc_start = (client.shooter.heading -
                             (gun.fire_rate /
                              2) *
                             arc_diff)
                for i in range(gun.fire_rate):
                    curr_arc = arc_start + (i * arc_diff)
                    ray = get_ray_collision(
                        game_board,
                        client.shooter.hitbox.position,
                        curr_arc,
                        gun.range,
                        gun.damage /
                        gun.fire_rate,
                        [client.shooter]
                    )
                    game_board.ray_list.append(ray)
                    collision_object = ray.collision
                    apply_damage(
                        collision_object,
                        ray,
                        gun,
                        game_board,
                        gun.fire_rate)
                    gun.mag_ammo -= 1
