from game.common.ray import Ray
from game.common.items.gun import Gun
from game.config import *
from game.common.enums import *

import math


# Get relevant collidables, 90 degree segment, will replace
def load_collidables(player, gameboard, shooter):
    partition_x = gameboard.partition.find_row(shooter.X)
    partition_y = gameboard.partition.find_column(shooter.Y)

    collidables = {x: 0 for x in gameboard.player_list}
    collidables.append({x: 0 for x in gameboard.wall_list})

    if 0 <= player.shooter.heading < (math.pi/2) or player.shooter.heading == (2*math.pi):
        for x in range(partition_x, gameboard.partition.width):
            for y in range(partition_y, gameboard.partition.height, -1):
                collidables.append(gameboard.partition.get_partition_objects(x, y))
    elif (math.pi/2) <= player.shooter.heading < math.pi:
        for x in range(partition_x, gameboard.partition.width):
            for y in range(partition_y, gameboard.partition.height):
                collidables.append(gameboard.parition.get_partition_objects(x, y))
    elif (math.pi) <= player.shooter.heading < ((3*math.pi)/2):
        for x in range(partition_x, gameboard.partition.width, -1):
            for y in range(partition_y, gameboard.partition.height, -1):
                collidables.append(gameboard.parition.get_partition_objects(x, y))
    elif (3*(math.pi)/2) <= player.shooter.heading <= (2*math.pi):
        for x in range(partition_x, gameboard.partition.width, -1):
            for y in range(partition_y, gameboard.partition.height):
                collidables.append(gameboard.parition.get_partition_objects(x, y))

    return collidables

# Calculate slope from player position and heading
def calculate_slope(player):
    if (player.shooter.heading != 0) and (player.shooter.heading != math.pi):
        adj_heading = math.radians(player.shooter.heading + (math.pi/2))
        slope = math.tan(adj_heading)
    else:
        slope = math.nan

    return slope


# Get y coordinate at x given slope
def calculate_ray_y(player, slope, x):
    if slope is not math.nan:
        ray_y = ((slope * (x - player.shooter.coordinates.X)) +
                player.shooter.coordinates.Y)
    else:
        ray_y = math.nan
    return ray_y


# Get x coordinate at y given slope
def calculate_ray_x(player, slope, y):
    if slope is not math.nan:
        ray_x = (((y - player.shooter.coordinates.Y) / slope)
                + player.shooter.coordinates.Y)
    else:
        ray_x = player.shooter.coordinates.X
    return ray_x


# Remove any objects that cannot be collided with
def cull_objects(player, gameboard, collidables, slope):
    if 0 <= player.shooter.heading < (math.pi/2) or player.shooter.heading == (2*math.pi):
        max_x = calculate_ray_x(player, slope, 0)
        if max_x > gameboard.width:
            max_x = gameboard.width
        for collidable in collidables.keys:
            if (collidable.coordinates.Y + (collidable.hitbox['width'] / 2)
                    < player.shooter.coordinates.X
                    or collidable.coordinates.X - (collidable.hitbox['width'] / 2) > max_x
                    or (collidable.coordinates.Y + (collidable.hitbox['height'] / 2)
                    < player.shooter.coordinates.Y)):
                collidables.pop(collidable)

    elif (math.pi/2) <= player.shooter.heading < math.pi:
        max_x = calculate_ray_x(player, slope, -gameboard.height)
        if max_x > gameboard.width:
            max_x = gameboard.width
        for collidable in collidables.keys:
            if ((collidable.coordinates.X - (collidable.hitbox['width'] / 2)
                    < player.shooter.coordinates.X)
                    or collidable.coordinates.X - (collidable.hitbox['width'] / 2) > max_x
                    or (collidable.coordinates.Y + (collidable.hitbox['height'] / 2)
                        > player.shooter.coordinates.Y)):
                collidables.pop(collidable)

    elif math.pi <= player.shooter.heading < ((3*math.pi)/2):
        max_x = calculate_ray_x(player.shooter, slope, -gameboard.height)
        if max_x < gameboard.width:
            max_x = 0
        for collidable in collidable.keys:
            if ((collidable.coordinates.X + (collidable.hitbox['width'] / 2)
                    > player.shooter.coordinates.X)
                    or collidable.coordinates.X + (collidable.hitbox['width'] / 2) < max_x
                    or (collidable.coordinates.Y + (collidable.hitbox['height'] / 2)
                        > player.shooter.coordinates.Y)):
                collidables.pop(collidable)

    elif player.shooter.heading >= ((3*math.pi)/2):
        max_x = calculate_ray_x(player.shooter, slope, 0)
        if max_x < gameboard.width:
            max_x = 0
        for collidable in collidable.keys:
            if ((collidable.coordinates.X + (collidable.hitbox['width'] / 2)
                > player.shooter.coordinates.X)
                    or collidable.coordinates.X + (collidable.hitbox['width'] / 2) < max_x
                    or (collidable.coordinates.Y - (collidable.hitbox['height'] / 2)
                        > player.shooter.coordinates.Y)):
                collidables.pop(collidable)

    return collidables


# Sort objects by distance from given player's shooter
def sort_objects(player, collidables, gun):
    for collidable in collidables.keys:
        dist = math.sqrt(((collidable.coordinates.X - player.shooter.coordinates.X) ** 2)
                + ((collidable.coordinates.Y - player.shooter.coordinates.Y) ** 2))
        if dist > gun.range:
            collidables.pop(collidable)
        else:
            collidables[collidable] = dist
    collidables = sorted(collidables.items(), key=lambda x:x[1])

    return collidables


# Determine which object ray collides with first
def determine_collision(player, collidables, slope, gun):
    # Get x and y limits given gun range and heading
    ray_x_limit = (player.shooter.coordinates.X + (gun.range 
        * math.cos(player.shooter.heading + math.pi/2)))
    ray_y_limit = (player.shooter.coordinates.Y + (gun.range 
        * math.sin(player.shooter.heading + math.pi/2)))
    default_endpoint = {'x': ray_x_limit, 'y': ray_y_limit}

    # Ray object used to provide data for visualizer
    ray = Ray(player.shooter.coordinates, default_endpoint, None, None)

    # AABB collision
    for collidable in collidables.keys:
        left_x = collidable.coordinates.X - (collidable.hitbox['width'] / 2)
        right_x = collidable.coordinates.X + (collidable.hitbox['width'] / 2)
        upper_y = collidable.coordinates.Y + (collidable.hitbox['height'] / 2)
        lower_y = collidable.coordinates.Y - (collidable.hitbox['height'] / 2)
        if 0 <= player.shooter.heading <= math.pi/2:
            ray_y = (calculate_ray_y(player, slope, left_x)
                    if calculate_ray_y(player, slope, left_x)
                    is not math.nan else lower_y)
            ray_x = calculate_ray_x(player, slope, lower_y)
        elif math.pi/2 <= player.shooter.heading <= math.pi:
            ray_y = (calculate_ray_y(player, slope, left_x)
                    if calculate_ray_y(player, slope, left_x)
                    is not math.nan else lower_y)
            ray_x = calculate_ray_x(player, slope, upper_y)
        elif math.pi <= player.shooting.heading <= ((3*math.pi)/2):
            ray_y = (calculate_ray_y(player, slope, right_x)
                    if calculate_ray_y(player, slope, right_x)
                    is not math.nan else lower_y)
            ray_x = calculate_ray_x(player, slope, upper_y)
        elif ((3*math.pi)/2) <= player.shooting.heading <= (2*math.pi):
            ray_y = (calculate_ray_y(player, slope, right_x)
                    if calculate_ray_y(player, slope, right_x)
                    is not math.nan else lower_y)
            ray_x = calculate_ray_x(player, slope, lower_y)
        if (lower_y <= ray_y <= upper_y) or (left_x <= ray_x <= right_x):
            endpoint = {'x': ray_x, 'y': ray_y}
            ray = Ray(player.shooter.coordinates, endpoint, collidable, gun.damage)
            break

    return ray


# Should probably replace with access to player's equipped weapon
def get_ray_collision(self, player, gameboard, gun):
    collidables = self.load_collidables(player, gameboard)
    slope = self.calculate_slope(player)
    self.cull_objects(player, gameboard, collidables, slope)
    self.sort_objects(player, collidables, gun)
    ray = determine_collision(player, collidables, slope, gun)

    return ray
