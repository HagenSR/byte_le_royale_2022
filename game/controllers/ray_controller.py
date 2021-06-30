from game.controllers.controller import Controller
from game.common.ray import Ray
from game.common.items.gun import Gun
from game.config import *
from game.common.enums import *

import math


class RayController(Controller):
    def __init__(self):
        super().__init__()

    def load_collidables(self, gameboard):
        collidables = {x: 0 for x in gameboard.player_list}
        collidables.append({x: 0 for x in gameboard.wall_list})

        return collidables

    def calculate_slope(self, player):
        if (player.shooter.heading != 0) and (player.shooter.heading != 180):
            adj_heading = math.radians(player.shooter.heading + 90)
            slope = math.tan(adj_heading)
        else:
            slope = math.nan

        return slope

    def calculate_ray_y(self, player, slope, x):
        if slope is not math.nan:
            ray_y = ((slope * (x - player.shooter.coordinates['x'])) +
                player.shooter.coordinates['y'])
        else:
            ray_y = math.nan
        return ray_y

    def calculate_ray_x(self, player, slope, y):
        if slope is not math.nan:
            ray_x = (((y - player.shooter.coordinates['y']) / slope)
                    + player.shooter.coordinates['x'])
        else:
            ray_x = player.shooter.coordinates['x']
        return ray_x

    def cull_objects(self, player, gameboard, collidables, slope):
        if 0 <= player.shooter.heading < 90 or player.shooter.heading == 360:
            max_x = self.calculate_ray_x(player, slope, 0)
            if max_x > gameboard.width:
                max_x = gameboard.width
            for collidable in collidables.keys:
                if (collidable.coordinates['x'] + (collidable.hitbox['width'] / 2)
                        < player.shooter.coordinates['x']
                        or collidable.coordinates['x'] - (collidable.hitbox['width'] / 2) > max_x
                        or (collidable.coordinates['y'] + (collidable.hitbox['height'] / 2)
                        < player.shooter.coordinates['y'])):
                    collidables.pop(collidable)

        elif 90 <= player.shooter.heading < 180:
            max_x = self.calculate_ray_x(player, slope, -gameboard.height)
            if max_x > gameboard.width:
                max_x = gameboard.width
            for collidable in collidables.keys:
                if ((collidable.coordinates['x'] - (collidable.hitbox['width'] / 2)
                        < player.shooter.coordinates['x'])
                        or collidable.coordinates['x'] - (collidable.hitbox['width'] / 2) > max_x
                        or (collidable.coordinates['y'] + (collidable.hitbox['height'] / 2)
                            > player.shooter.coordinates['y'])):
                    collidables.pop(collidable)

        elif 180 <= player.shooter.heading < 270:
            max_x = self.calculate_ray_x(player.shooter, slope, -gameboard.height)
            if max_x < gameboard.width:
                max_x = 0
            for collidable in collidable.keys:
                if ((collidable.coordinates['x'] + (collidable.hitbox['width'] / 2)
                        > player.shooter.coordinates['x'])
                        or collidable.coordinates['x'] + (collidable.hitbox['width'] / 2) < max_x
                        or (collidable.coordinates['y'] + (collidable.hitbox['height'] / 2)
                            > player.shooter.coordinates['y'])):
                    collidables.pop(collidable)

        elif player.shooter.heading >= 270:
            max_x = self.calculate_ray_x(player.shooter, slope, 0)
            if max_x < gameboard.width:
                max_x = 0
            for collidable in collidable.keys:
                if ((collidable.coordinates['x'] + (collidable.hitbox['width'] / 2)
                    > player.shooter.coordinates['x'])
                        or collidable.coordinates['x'] + (collidable.hitbox['width'] / 2) < max_x
                        or (collidable.coordinates['y'] - (collidable.hitbox['height'] / 2)
                            > player.shooter.coordinates['y'])):
                    collidables.pop(collidable)

        return collidables


    def sort_objects(self, player, collidables, gun):
        for collidable in collidables.keys:
            dist = math.sqrt(((collidable.coordinates['x'] - player.shooter.coordinates['x']) ** 2)
                    + ((collidable.coordinates['y'] - player.shooter.coordinates['y']) ** 2))
            if dist > gun.range:
                collidables.pop(collidable)
            else:
                collidables[collidable] = dist
        collidables = sorted(collidables.items(), key=lambda x:x[1])

        return collidables

    def determine_collision(self, player, collidables, slope, gun):
        ray_x_limit = player.shooter.coordinates['x'] + (gun.range
                * math.cos(math.radians(player.shooter.heading + 90)))
        ray_y_limit = player.shooter.coordinates['y'] + (gun.range
                * math.sin(math.radians(player.shooter.heading + 90)))
        default_endpoint = {'x': ray_x_limit, 'y': ray_y_limit}
        ray = Ray(player.shooter.coordinates, default_endpoint, None, None)
        for collidable in collidables.keys:
            left_x = collidable.coordinates['x'] - (collidable.hitbox['width'] / 2)
            right_x = collidable.coordinates['x'] + (collidable.hitbox['width'] / 2)
            upper_y = collidable.coordinates['y'] + (collidable.hitbox['height'] / 2)
            lower_y = collidable.coordinates['y'] - (collidable.hitbox['height'] / 2)
            if 0 <= player.shooter.heading <= 90:
                ray_y = (self.calculate_ray_y(player, slope, left_x)
                        if self.calculate_ray_y(player, slope, left_x)
                        is not math.nan else lower_y)
                ray_x = self.calculate_ray_x(player, slope, lower_y)
            elif 90 <= player.shooter.heading <= 180:
                ray_y = (self.calculate_ray_y(player, slope, left_x)
                        if self.calculate_ray_y(player, slope, left_x)
                        is not math.nan else lower_y)
                ray_x = self.calculate_ray_x(player, slope, upper_y)
            elif 180 <= player.shooting.heading <= 270:
                ray_y = (self.calculate_ray_y(player, slope, right_x)
                        if self.calculate_ray_y(player, slope, right_x)
                        is not math.nan else lower_y)
                ray_x = self.calculate_ray_x(player, slope, upper_y)
            elif 270 <= player.shooting.heading <= 360:
                ray_y = (self.calculate_ray_y(player, slope, right_x)
                        if self.calculate_ray_y(player, slope, right_x)
                        is not math.nan else lower_y)
                ray_x = self.calculate_ray_x(player, slope, lower_y)
            if (lower_y <= ray_y <= upper_y) or (left_x <= ray_x <= right_x):
                endpoint = {'x': ray_x, 'y': ray_y}
                ray = Ray(player.shooter.coordinates, endpoint, collidable, gun.damage)
                break

        return ray

    def handle_actions(self, player, gameboard):
        gameboard.ray_list.clear()
        if (isinstance(player.action.action_parameter, Gun) is True
                and player.action._chosen_action is ActionType.shoot):
            gun = player.action.action_parameter
            collidables = self.load_collidables(gameboard)
            slope = self.calculate_slope(player)

            self.cull_objects(player, gameboard, collidables, slope)
            self.sort_objects(player, collidables, gun)
            ray = self.determine_collision(player, collidables, slope, gun)
            gameboard.ray_list.append(ray)
