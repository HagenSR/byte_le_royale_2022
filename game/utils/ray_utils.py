from game.common.ray import Ray
from game.config import *
from game.common.enums import *

import math


# Get relevant collidables in partitions bounded by furthest x, y and origin
def load_collidables_in_ray_range(heading, x, y, gameboard, ray_endpoint, exclusions=[]):
    ray_x_limit = ray_endpoint[0]
    ray_y_limit = ray_endpoint[1]
    # starting partition
    partition_x = gameboard.partition.find_column(x)
    partition_y = gameboard.partition.find_row(y)
    # ending partition
    end_partition_x = gameboard.partition.find_column(
        ray_x_limit)
    end_partition_y = gameboard.partition.find_row(
        ray_y_limit)
    collidables = {}
    # angle quadrants, initialize distances to 0
    if math.pi / 2 >= heading >= 0:
        for x in range(partition_x, end_partition_x + 1):
            for y in range(partition_y, end_partition_y - 1, -1):
                for z in gameboard.partition.get_partition_objects(x, y):
                    if z not in exclusions:
                        collidables[z] = 0
    elif math.pi >= heading > math.pi / 2:
        for x in range(partition_x, end_partition_x - 1, -1):
            for y in range(partition_y, end_partition_y - 1, -1):
                for z in gameboard.partition.get_partition_objects(x, y):
                    if z not in exclusions:
                        collidables[z] = 0
    elif (3 * math.pi) / 2 >= heading > math.pi:
        for x in range(partition_x, end_partition_x - 1, -1):
            for y in range(partition_y, end_partition_y + 1):
                for z in gameboard.partition.get_partition_objects(x, y):
                    if z not in exclusions:
                        collidables[z] = 0
    elif (3 * math.pi) / 2 < heading <= 2 * math.pi:
        for x in range(partition_x, end_partition_x + 1):
            for y in range(partition_y, end_partition_y + 1):
                for z in gameboard.partition.get_partition_objects(x, y):
                    if z not in exclusions:
                        collidables[z] = 0

    return collidables


# get collidables in a cube of partitions bounded by range
def load_collidables_in_range(gameboard, x, y, max_range, exclusions=[]):
    collidables = {}
    if x - max_range >= 0:
        start_partition_x = gameboard.partition.find_column(x - max_range)
    else:
        start_partition_x = gameboard.partition.find_column(0)
    if y - max_range >= 0:
        start_partition_y = gameboard.partition.find_row(y - max_range)
    else:
        start_partition_y = gameboard.partition.find_row(0)
    if x + max_range <= gameboard.width:
        end_partition_x = gameboard.partition.find_column(x + max_range)
    else:
        end_partition_x = gameboard.partition.find_column(gameboard.width)
    if y + max_range <= gameboard.height:
        end_partition_y = gameboard.partition.find_column(y + max_range)
    else:
        end_partition_y = gameboard.partition.find_column(gameboard.height)
    for x in range(start_partition_x, end_partition_x + 1):
        for y in range(start_partition_y, end_partition_y + 1):
            for z in gameboard.partition.get_partition_objects(x, y):
                if z not in exclusions:
                    collidables[z] = 0

    return collidables


# Calculate slope from player heading
def calculate_slope(heading):
    if (heading != math.pi / 2
            and heading != ((3 * math.pi) / 2)):
        slope = math.tan(heading)
    else:
        slope = math.nan

    return slope


# Get y coordinate at x given slope
def calculate_ray_y(x1, y1, slope, x):
    if slope is not math.nan:
        ray_y = ((slope * (x - x1)) + -y1)
    else:
        ray_y = math.nan

    return ray_y


# Get x coordinate at y given slope
def calculate_ray_x(x1, y1, slope, y):
    if math.isclose(slope, 0, abs_tol=1e-8):
        ray_x = math.nan
    elif slope is not math.nan:
        ray_x = ((y - (-y1)) / slope) + x1
    else:
        ray_x = x1

    return ray_x


def get_ray_limits(heading, x1, y1, gameboard, slope, ray_range):
    # Get final x and y coordinates given gun range and heading
    if (0 <= heading < math.pi / 2
            or (3 * math.pi) / 2 < heading <= 2 * math.pi):
        if heading == 0 or heading == 2 * math.pi:
            ray_x_limit = x1 + ray_range
        else:
            ray_x_limit = (
                x1 +
                abs(
                    ray_range *
                    math.sin(
                        heading %
                        (math.pi /
                         2))))
    else:
        if heading == math.pi:
            ray_x_limit = x1 - ray_range
        else:
            ray_x_limit = (
                x1 -
                abs(
                    ray_range *
                    math.sin(
                        heading %
                        (math.pi /
                         2))))
    if (heading == 0 or heading == math.pi
            or heading == 2 * math.pi):
        ray_y_limit = y1
    else:
        if 0 <= heading <= math.pi:
            ray_y_limit = -(-y1 + abs(
                ray_range * math.cos(heading % (math.pi / 2))))
        else:
            ray_y_limit = -(-y1 - abs(
                ray_range * math.cos(heading % (math.pi / 2))))
    if ray_x_limit < 0:
        if 0 < calculate_ray_y(x1, y1, slope, 0) < gameboard.height:
            ray_x_limit = 0
            ray_y_limit = calculate_ray_y(x1, y1, slope, 0)
    elif ray_x_limit > gameboard.width:
        if 0 < calculate_ray_y(
                x1,
                y1,
                slope,
                gameboard.width) < gameboard.height:
            ray_x_limit = gameboard.width
            ray_y_limit = calculate_ray_y(x1, y1, slope, gameboard.width)
    if ray_y_limit < 0:
        if 0 < calculate_ray_x(x1, y1, slope, 0) < gameboard.width:
            ray_y_limit = 0
            ray_x_limit = calculate_ray_x(x1, y1, slope, 0)
    elif ray_y_limit > gameboard.height:
        if 0 < calculate_ray_x(
                x1,
                y1,
                slope,
                gameboard.height) < gameboard.width:
            ray_y_limit = gameboard.height
            ray_x_limit = calculate_ray_x(x1, y1, slope, gameboard.height)

    return (ray_x_limit, ray_y_limit)


def sort_objects(x1, y1, collidables, max_range):
    # assign distances, discard if out of bounds
    for ray in list(collidables.keys()):
        dist = round(math.sqrt(
            ((ray.endpoint[0] - x1) ** 2) + (
                (-ray.endpoint[1] - -y1) ** 2)))
        if max_range is not math.nan:
            if dist > max_range:
                collidables.pop(ray)
            else:
                collidables[ray] = dist
    # sort collidables by distance
    collidables = sorted(collidables.items(), key=lambda x: x[1])

    return collidables


# Determine which object ray collides with first
def determine_gun_collision(player, gameboard, collidables, slope, ray_endpoint, damage):
    # Ray object used to provide data for visualizer
    ray_y = -player.shooter.hitbox.position[1] - (slope * player.shooter.hitbox.position[0])
    ray_slope = slope
    collisions = {}
    for collidable in collidables.keys():
        # bottom line
        line_slope = ((-collidable.hitbox.bottomLeft[1] -
                -collidable.hitbox.bottomRight[1]) / 
                (collidable.hitbox.bottomLeft[0] -
                    collidable.hitbox.bottomRight[0]))
        line_y = -collidable.hitbox.bottomLeft[1] - (line_slope * collidable.hitbox.bottomLeft[0])
        if (round(ray_slope - line_slope, 4) != 0 and ray_slope is not
                math.nan):
            x_intercept = (line_y - ray_y) / (ray_slope - line_slope)
        else:
            x_intercept = player.shooter.hitbox.position[0]
        if round(line_slope, 4) == 0:
            corr_y = collidable.hitbox.bottomLeft[1]
        else:
            corr_y = calculate_ray_y(collidable.hitbox.bottomLeft[0],
                    -collidable.hitbox.bottomLeft[1], line_slope, x_intercept)

        if (collidable.hitbox.bottomLeft[0] <= x_intercept <=
                collidable.hitbox.bottomRight[0]):
            ray = Ray(player.shooter.hitbox.position, (x_intercept, corr_y),
                collidable, player.shooter.primary_gun.damage)
            collisions[ray] = 0

        # right line
        line_slope = ((-collidable.hitbox.bottomRight[1] -
                -collidable.hitbox.topRight[1]) / 
                (collidable.hitbox.bottomRight[0] -
                    collidable.hitbox.topRight[0]) if
                collidable.hitbox.bottomRight[0] - collidable.hitbox.topRight[0]
                != 0 else math.nan)
        line_y = -collidable.hitbox.bottomRight[1] - (line_slope *
                collidable.hitbox.bottomRight[0])
        if line_slope is math.nan:
            x_intercept = calculate_ray_x(player.shooter.hitbox.position[0],
                    -player.shooter.hitbox.position[1], ray_slope,
                    -collidable.hitbox.bottomRight[1])
            if x_intercept is math.nan:
                x_intercept = max(collidable.hitbox.bottomRight[0],
                        collidable.hitbox.topRight[0])
        elif round(ray_slope - line_slope, 4) != 0:
            x_intercept = (line_y - ray_y) / (ray_slope - line_slope)
        else:
            x_intercept = player.shooter.hitbox.position[0]
        corr_y = calculate_ray_y(player.shooter.hitbox.position[0],
                -player.shooter.hitbox.position[1], ray_slope, x_intercept)
        if corr_y is math.nan:
            corr_y = min(collidable.hitbox.bottomRight[1],
                    collidable.hitbox.topRight[1])
        if (collidable.hitbox.bottomRight[0] <= x_intercept <=
                collidable.hitbox.topRight[0] or collidable.hitbox.bottomRight[0] >
                x_intercept > collidable.hitbox.topRight[0]):
            ray = Ray(player.shooter.hitbox.position, (x_intercept, corr_y),
                collidable, player.shooter.primary_gun.damage)
            collisions[ray] = 0

        # top line
        line_slope = ((-collidable.hitbox.topLeft[1] -
                -collidable.hitbox.topRight[1]) / 
                (collidable.hitbox.topLeft[0] - collidable.hitbox.topRight[0]))
        line_y = -collidable.hitbox.topLeft[1] - (line_slope *
                collidable.hitbox.topLeft[0])

        if (round(ray_slope - line_slope, 4) != 0 and ray_slope is not
                math.nan):
            x_intercept = (line_y - ray_y) / round(ray_slope - line_slope, 4)
        else:
            if line_slope == 0:
                if (player.shooter.hitbox.position[0] -
                        collidable.hitbox.topLeft[0] >
                        player.shooter.hitbox.position[0] -
                        collidable.hitbox.topRight[0]):
                    x_intercept = collidable.hitbox.topLeft[0]
                else:
                    x_intercept = collidable.hitbox.topRight[0]

            else:
                x_intercept = (player.shooter.hitbox.position[0] - line_y /
                        line_slope)

        if round(line_slope, 4) == 0:
            corr_y = collidable.hitbox.topLeft[1]
        else:
            corr_y = calculate_ray_y(player.shooter.hitbox.position[0],
                    -player.shooter.hitbox.position[1], ray_slope, x_intercept)
        if (collidable.hitbox.topLeft[0] <= x_intercept <=
                collidable.hitbox.topRight[0]):
            ray = Ray(player.shooter.hitbox.position, (x_intercept, corr_y),
                collidable, player.shooter.primary_gun.damage)
            collisions[ray] = 0

        # left line
        line_slope = ((-collidable.hitbox.bottomLeft[1] -
                -collidable.hitbox.topLeft[1])/
                (collidable.hitbox.bottomLeft[0] - collidable.hitbox.topLeft[0]) if
                collidable.hitbox.bottomLeft[0] - collidable.hitbox.topLeft[0] != 0
            else math.nan)
        line_y = -collidable.hitbox.bottomLeft[1] - (line_slope *
                collidable.hitbox.bottomLeft[0])
        if line_slope is math.nan:
            x_intercept = calculate_ray_x(player.shooter.hitbox.position[0],
                    -player.shooter.hitbox.position[1], ray_slope,
                    -collidable.hitbox.bottomLeft[1])
            if x_intercept is math.nan:
                x_intercept = min(collidable.hitbox.bottomLeft[0],
                        collidable.hitbox.topLeft[0])
        elif round(ray_slope - line_slope, 4) != 0:
            x_intercept = (line_y - ray_y) / (ray_slope - line_slope)
        else:
            x_intercept = (player.shooter.hitbox.position[0] - line_y /
                    line_slope)
        corr_y = calculate_ray_y(player.shooter.hitbox.position[0],
                -player.shooter.hitbox.position[1], ray_slope, x_intercept)
        if corr_y is math.nan:
            corr_y = min(collidable.hitbox.bottomLeft[1],
                    collidable.hitbox.topLeft[1])


        if (collidable.hitbox.bottomLeft[0] <= x_intercept <=
                collidable.hitbox.topLeft[0] or collidable.hitbox.bottomLeft[0]
                >= x_intercept > collidable.hitbox.topLeft[0]):
            ray = Ray(player.shooter.hitbox.position, (x_intercept, corr_y),
                collidable, player.shooter.primary_gun.damage)
            collisions[ray] = 0

    rays = sort_objects(player.shooter.hitbox.position[0],
            player.shooter.hitbox.position[1], collisions,
            player.shooter.primary_gun.range)
    if len(rays) > 0:
        return rays[0][0]
    else:
        ray = Ray(
                player.shooter.hitbox.position,
                ray_endpoint,
                None,
                player.shooter.primary_gun.damage
                )
        return ray


# Method to be called by controller
def get_ray_collision(player, gameboard):
    slope = calculate_slope(player.shooter.heading)
    ray_endpoint = get_ray_limits(player.shooter.heading,
                                  player.shooter.hitbox.position[0],
                                  player.shooter.hitbox.position[1],
                                  gameboard,
                                  slope,
                                  player.shooter.primary_gun.range)
    collidables = load_collidables_in_ray_range(
            player.shooter.heading,
            player.shooter.hitbox.position[0],
            player.shooter.hitbox.position[1],
            gameboard,
            ray_endpoint,
            [player.shooter]
            )

    ray = determine_gun_collision(
        player,
        gameboard,
        collidables,
        slope,
        ray_endpoint,
        player.shooter.primary_gun.damage
        )

    return ray
