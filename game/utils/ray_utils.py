from game.common.ray import Ray
from game.common.items.gun import Gun
from game.config import *
from game.common.enums import *

import math


# Get relevant collidables, 90 degree segment, will replace
def load_collidables(player, gameboard):
    partition_x = gameboard.partition.find_row(
        player.shooter.hitbox.position[0])
    partition_y = gameboard.partition.find_column(
        player.shooter.hitbox.position[1])
    collidables = {}
    if 0 <= player.shooter.heading < (
            math.pi /
            2) or player.shooter.heading == (
            2 *
            math.pi):
        for x in range(partition_x, gameboard.partition.get_partitions_wide()):
            for y in range(partition_y, -1, -1):
                for z in gameboard.partition.get_partition_objects(x, y):
                    collidables[z] = 0
    elif (math.pi / 2) <= player.shooter.heading < math.pi:
        for x in range(partition_x, gameboard.partition.get_partitions_wide()):
            for y in range(
                    partition_y,
                    gameboard.partition.get_partitions_tall()):
                for z in gameboard.partition.get_partition_objects(x, y):
                    collidables[z] = 0
    elif (math.pi) <= player.shooter.heading < ((3 * math.pi) / 2):
        for x in range(partition_x, -1, -1):
            for y in range(
                    partition_y,
                    gameboard.partition.get_partitions_tall()):
                for z in gameboard.partition.get_partition_objects(x, y):
                    collidables[z] = 0
    elif ((3 * math.pi) / 2) <= player.shooter.heading <= (2 * math.pi):
        for x in range(partition_x, -1, -1):
            for y in range(partition_y, -1, -1):
                for z in gameboard.partition.get_partition_objects(x, y):
                    collidables[z] = 0

    return collidables


# Calculate slope from player position and heading
def calculate_slope(player):
    if (player.shooter.heading != 0) and (player.shooter.heading != math.pi):
        slope = math.tan(player.shooter.heading)
    else:
        slope = math.nan

    return slope


# Get y coordinate at x given slope
def calculate_ray_y(player, slope, x):
    if slope is not math.nan:
        ray_y = ((slope * (x - player.shooter.hitbox.position[0])) +
                 -player.shooter.hitbox.position[1])
    else:
        ray_y = math.nan

    return ray_y


# Get x coordinate at y given slope
def calculate_ray_x(player, slope, y):
    if slope is not math.nan:
        ray_x = (((y - (-player.shooter.hitbox.position[1])) / slope)
                 + player.shooter.hitbox.position[0])
    else:
        ray_x = player.shooter.hitbox.position[0]

    return ray_x


# Sort objects by distance from given player's shooter
def sort_objects(player, collidables, gun):
    for collidable in list(collidables.keys()):
        dist = math.sqrt(
            ((collidable.hitbox.position[0] - player.shooter.hitbox.position[0]) ** 2) + (
                (-collidable.hitbox.position[1] - -player.shooter.hitbox.position[1]) ** 2))
        if dist > gun.range:
            collidables.pop(collidable)
        else:
            collidables[collidable] = dist
    collidables = sorted(collidables.items(), key=lambda x: x[1])

    return collidables


# Determine which object ray collides with first
def determine_collision(player, collidables, slope, gun):
    # Get x and y limits given gun range and heading
    if 0 <= player.shooter.heading < math.pi / 2:
        ray_x_limit = (
            player.shooter.hitbox.position[0] + abs(gun.range * math.cos(player.shooter.heading)))
        ray_y_limit = (-player.shooter.hitbox.position[1] + abs(
            gun.range * math.sin(player.shooter.heading)))
    elif math.pi / 2 <= player.shooter.heading < math.pi:
        ray_x_limit = (
            player.shooter.hitbox.position[0] + abs(gun.range * math.cos(player.shooter.heading)))
        ray_y_limit = (-player.shooter.hitbox.position[1] - abs(
            gun.range * math.sin(player.shooter.heading)))
    elif math.pi <= player.shooter.heading < (3 * (math.pi / 4)):
        ray_x_limit = (
            player.shooter.hitbox.position[0] - abs(gun.range * math.cos(player.shooter.heading)))
        ray_y_limit = (-player.shooter.hitbox.position[1] - abs(
            gun.range * math.sin(player.shooter.heading)))
    elif (3 * (math.pi / 4)) <= player.shooter.heading < 2 * math.pi:
        ray_x_limit = (
            player.shooter.hitbox.position[0] - abs(gun.range * math.cos(player.shooter.heading)))
        ray_y_limit = (-player.shooter.hitbox.position[1] + abs(
            gun.range * math.sin(player.shooter.heading)))

    default_endpoint = {'x': ray_x_limit, 'y': -ray_y_limit}

    # Ray object used to provide data for visualizer
    ray = Ray(player.shooter.hitbox.position, default_endpoint, None, None)

    # AABB collision
    for collidable in collidables.keys():
        left_x = collidable.hitbox.position[0] - (collidable.hitbox.width / 2)
        right_x = collidable.hitbox.position[0] + (collidable.hitbox.width / 2)
        upper_y = - \
            collidable.hitbox.position[1] + (collidable.hitbox.height / 2)
        lower_y = - \
            collidable.hitbox.position[1] - (collidable.hitbox.height / 2)
        if 0 <= player.shooter.heading <= math.pi / 2:
            ray_y = (calculate_ray_y(player, slope, left_x)
                     if calculate_ray_y(player, slope, left_x)
                     is not math.nan else lower_y)
            ray_x = calculate_ray_x(player, slope, lower_y)
        elif math.pi / 2 <= player.shooter.heading <= math.pi:
            ray_y = (calculate_ray_y(player, slope, left_x)
                     if calculate_ray_y(player, slope, left_x)
                     is not math.nan else lower_y)
            ray_x = calculate_ray_x(player, slope, upper_y)
        elif math.pi <= player.shooter.heading <= ((3 * math.pi) / 2):
            ray_y = (calculate_ray_y(player, slope, right_x)
                     if calculate_ray_y(player, slope, right_x)
                     is not math.nan else lower_y)
            ray_x = calculate_ray_x(player, slope, upper_y)
        elif ((3 * math.pi) / 2) <= player.shooter.heading <= (2 * math.pi):
            ray_y = (calculate_ray_y(player, slope, right_x)
                     if calculate_ray_y(player, slope, right_x)
                     is not math.nan else lower_y)
            ray_x = calculate_ray_x(player, slope, lower_y)
        if (lower_y <= ray_y <= upper_y) and (left_x <= ray_x <= right_x):
            endpoint = {'x': ray_x, 'y': -ray_y}
            ray = Ray(
                player.shooter.hitbox.position,
                endpoint,
                collidable,
                gun.damage)
            break

    return ray


# Should probably replace with access to player's equipped weapon
def get_ray_collision(player, gameboard, gun):
    collidables = load_collidables(player, gameboard)
    slope = calculate_slope(player)
    sort_objects(player, collidables, gun)
    ray = determine_collision(player, collidables, slope, gun)

    return ray
