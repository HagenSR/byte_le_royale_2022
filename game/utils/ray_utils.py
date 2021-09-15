from game.common.ray import Ray
from game.config import *
from game.common.enums import *

import math


# Get relevant collidables in partitions bounded by furthest x, y and origin
def load_collidables(player, gameboard, ray_endpoint):
    ray_x_limit = ray_endpoint['x']
    ray_y_limit = ray_endpoint['y']
    # starting partition
    partition_x = gameboard.partition.find_column(
        player.shooter.hitbox.position[0])
    partition_y = gameboard.partition.find_row(
        player.shooter.hitbox.position[1])
    # ending partition
    end_partition_x = gameboard.partition.find_column(
        ray_x_limit)
    end_partition_y = gameboard.partition.find_row(
        ray_y_limit)
    collidables = {}
    # angle quadrants
    if 0 <= player.shooter.heading < (
            math.pi /
            2) or player.shooter.heading == (
            2 *
            math.pi):
        for x in range(partition_x, end_partition_x + 1):
            for y in range(partition_y, end_partition_y - 1, -1):
                for z in gameboard.partition.get_partition_objects(x, y):
                    if z is not player.shooter:
                        collidables[z] = 0
    elif (math.pi / 2) <= player.shooter.heading < math.pi:
        for x in range(partition_x, end_partition_x + 1):
            for y in range(partition_y, end_partition_y + 1):
                for z in gameboard.partition.get_partition_objects(x, y):
                    if z is not player.shooter:
                        collidables[z] = 0
    elif (math.pi) <= player.shooter.heading < ((3 * math.pi) / 2):
        for x in range(partition_x, end_partition_x - 1, -1):
            for y in range(partition_y, end_partition_y + 1):
                for z in gameboard.partition.get_partition_objects(x, y):
                    if z is not player.shooter:
                        collidables[z] = 0
    elif ((3 * math.pi) / 2) <= player.shooter.heading <= (2 * math.pi):
        for x in range(partition_x, end_partition_x - 1, -1):
            for y in range(partition_y, end_partition_y - 1, -1):
                for z in gameboard.partition.get_partition_objects(x, y):
                    if z is not player.shooter:
                        collidables[z] = 0
    return collidables


# Calculate slope from player position and heading
def calculate_slope(player):
    if (player.shooter.heading != 0) and (player.shooter.heading != math.pi):
        slope = -math.tan(player.shooter.heading + (math.pi / 2))
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
    if math.isclose(slope, 0, abs_tol=1e-8):
        ray_x = math.nan
    elif slope is not math.nan:
        ray_x = (((y - (-player.shooter.hitbox.position[1])) / slope)
                 + player.shooter.hitbox.position[0])
    else:
        ray_x = player.shooter.hitbox.position[0]

    return ray_x


def get_ray_limits(player, gameboard, slope):
    gun = player.shooter.primary_gun
    # Get final x and y coordinates given gun range and heading
    if 0 <= player.shooter.heading < math.pi:
        if player.shooter.heading == (math.pi / 2):
            ray_x_limit = player.shooter.hitbox.position[0] + gun.range
        else:
            ray_x_limit = (
                player.shooter.hitbox.position[0] +
                abs(
                    gun.range *
                    math.sin(
                        player.shooter.heading %
                        (math.pi /
                         2))))
        if ray_x_limit > gameboard.width:
            ray_x_limit = gameboard.width
    else:
        if player.shooter.heading == (3 * math.pi / 2):
            ray_x_limit = player.shooter.hitbox.position[0] - gun.range
        else:
            ray_x_limit = (
                player.shooter.hitbox.position[0] -
                abs(
                    gun.range *
                    math.sin(
                        player.shooter.heading %
                        (math.pi /
                         2))))
        if ray_x_limit < 0:
            ray_x_limit = 0
    if player.shooter.heading == math.pi / \
            2 or player.shooter.heading == (3 * (math.pi / 2)):
        ray_y_limit = player.shooter.hitbox.position[1]
    else:
        if 0 <= player.shooter.heading < math.pi / 2 or 3 * \
                (math.pi / 2) <= player.shooter.heading <= 2 * math.pi:
            ray_y_limit = -(-player.shooter.hitbox.position[1] + abs(
                gun.range * math.cos(player.shooter.heading % (math.pi / 2))))
            if ray_y_limit < 0:
                ray_y_limit = 0
        else:
            ray_y_limit = -(-player.shooter.hitbox.position[1] - abs(
                gun.range * math.cos(player.shooter.heading % (math.pi / 2))))
            if ray_y_limit > gameboard.height:
                ray_y_limit = gameboard.height

    return {'x': ray_x_limit, 'y': ray_y_limit}


# Sort objects by distance from given player's shooter
def sort_objects(player, collidables):
    gun = player.shooter.primary_gun
    # assign distances, discard if out of bounds
    for collidable in list(collidables.keys()):
        dist = math.sqrt(
            ((collidable.hitbox.position[0] - player.shooter.hitbox.position[0]) ** 2) + (
                (-collidable.hitbox.position[1] - -player.shooter.hitbox.position[1]) ** 2))
        if dist > gun.range:
            collidables.pop(collidable)
        else:
            collidables[collidable] = dist
    # sort collidables by distance
    collidables = sorted(collidables.items(), key=lambda x: x[1])

    return collidables


# Determine which object ray collides with first
def determine_collision(player, gameboard, collidables, slope, ray_endpoint):
    gun = player.shooter.primary_gun

    # Ray object used to provide data for visualizer
    ray = Ray(player.shooter.hitbox.position, ray_endpoint, None, None)

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
            ray_x = (
                calculate_ray_x(
                    player,
                    slope,
                    lower_y) if calculate_ray_x(
                    player,
                    slope,
                    lower_y) is not math.nan else left_x)
        elif math.pi / 2 < player.shooter.heading <= math.pi:
            ray_y = (calculate_ray_y(player, slope, left_x)
                     if calculate_ray_y(player, slope, left_x)
                     is not math.nan else lower_y)
            ray_x = (
                calculate_ray_x(
                    player,
                    slope,
                    upper_y) if calculate_ray_x(
                    player,
                    slope,
                    upper_y) is not math.nan else left_x)
        elif math.pi < player.shooter.heading <= ((3 * math.pi) / 2):
            ray_y = (calculate_ray_y(player, slope, right_x)
                     if calculate_ray_y(player, slope, right_x)
                     is not math.nan else lower_y)
            ray_x = (
                calculate_ray_x(
                    player,
                    slope,
                    upper_y) if calculate_ray_x(
                    player,
                    slope,
                    upper_y) is not math.nan else right_x)
        elif ((3 * math.pi) / 2) < player.shooter.heading <= (2 * math.pi):
            ray_y = (calculate_ray_y(player, slope, right_x)
                     if calculate_ray_y(player, slope, right_x)
                     is not math.nan else lower_y)
            ray_x = (
                calculate_ray_x(
                    player,
                    slope,
                    lower_y) if calculate_ray_x(
                    player,
                    slope,
                    lower_y) is not math.nan else right_x)
        if (lower_y <= ray_y <= upper_y) and (left_x <= ray_x <= right_x):
            endpoint = {'x': ray_x, 'y': -ray_y}
            ray = Ray(
                player.shooter.hitbox.position,
                endpoint,
                collidable,
                gun.damage)
            break
    return ray


# Method to be called by controller
def get_ray_collision(player, gameboard):
    slope = calculate_slope(player)
    ray_endpoint = get_ray_limits(player, gameboard, slope)
    collidables = load_collidables(player, gameboard, ray_endpoint)
    sort_objects(player, collidables)
    ray = determine_collision(
        player,
        gameboard,
        collidables,
        slope,
        ray_endpoint)

    return ray
