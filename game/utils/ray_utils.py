from game.common.ray import Ray
from game.common.teleporter import Teleporter
from game.config import *
from game.common.enums import *

import math


# Get relevant collidables in partitions bounded by furthest x, y and origin
def load_collidables_in_ray_range(
        heading,
        coords,
        gameboard,
        ray_endpoint,
        exclusions=None):
    if exclusions is None:
        exclusions = []
    # starting partition
    heading = (2 * math.pi - heading)
    partition_x = gameboard.partition.find_column(coords[0])
    partition_y = gameboard.partition.find_row(coords[1])
    # ending partition
    end_partition_x = gameboard.partition.find_column(
        ray_endpoint[0])
    end_partition_y = gameboard.partition.find_row(
        ray_endpoint[1])
    collidables = {}
    # angle quadrants, initialize distances to 0
    if math.pi / 2 >= heading >= 0:
        for x in range(partition_x, end_partition_x + 1):
            for y in range(partition_y, end_partition_y - 1, -1):
                for z in gameboard.partition.get_partition_objects_by_index(
                        x, y):
                    if z not in exclusions and z.collidable:
                        collidables[z] = 0
    elif math.pi >= heading > math.pi / 2:
        for x in range(partition_x, end_partition_x - 1, -1):
            for y in range(partition_y, end_partition_y - 1, -1):
                for z in gameboard.partition.get_partition_objects_by_index(
                        x, y):
                    if z not in exclusions and z.collidable:
                        collidables[z] = 0
    elif (3 * math.pi) / 2 >= heading > math.pi:
        for x in range(partition_x, end_partition_x - 1, -1):
            for y in range(partition_y, end_partition_y + 1):
                for z in gameboard.partition.get_partition_objects_by_index(
                        x, y):
                    if z not in exclusions and z.collidable:
                        collidables[z] = 0
    elif (3 * math.pi) / 2 < heading <= 2 * math.pi:
        for x in range(partition_x, end_partition_x + 1):
            for y in range(partition_y, end_partition_y + 1):
                for z in gameboard.partition.get_partition_objects_by_index(
                        x, y):
                    if z not in exclusions and z.collidable:
                        collidables[z] = 0

    return collidables


# get collidables in a cube of partitions bounded by range
def load_collidables_in_range(gameboard, coords, max_range, exclusions=[]):
    collidables = {}
    if coords[0] - max_range >= 0:
        start_partition_x = gameboard.partition.find_column(
            coords[0] - max_range)
    else:
        start_partition_x = gameboard.partition.find_column(0)
    if coords[1] - max_range >= 0:
        start_partition_y = gameboard.partition.find_row(coords[1] - max_range)
    else:
        start_partition_y = gameboard.partition.find_row(0)
    if coords[0] + max_range <= gameboard.width:
        end_partition_x = gameboard.partition.find_column(
            coords[0] + max_range)
    else:
        end_partition_x = gameboard.partition.find_column(gameboard.width)
    if coords[1] + max_range <= gameboard.height:
        end_partition_y = gameboard.partition.find_column(
            coords[1] + max_range)
    else:
        end_partition_y = gameboard.partition.find_column(gameboard.height)
    for x in range(start_partition_x, end_partition_x + 1):
        for y in range(start_partition_y, end_partition_y + 1):
            for z in gameboard.partition.get_partition_objects(x, y):
                if z not in exclusions:
                    collidables[z] = 0

    return collidables


# Calculate slope from player heading
def calculate_slope(heading_in_radians):
    heading_in_radians = (2 * math.pi - heading_in_radians)
    if (heading_in_radians != math.pi / 2
            and heading_in_radians != ((3 * math.pi) / 2)):
        slope = math.tan(heading_in_radians)
    else:
        slope = math.nan

    return slope


# Get y coordinate at x given slope
def calculate_ray_y(coords, slope, x):
    if slope is not math.nan:
        ray_y = -((slope * (x - coords[0])) + -coords[1])
    else:
        ray_y = math.nan

    return ray_y


# Get x coordinate at y given slope
def calculate_ray_x(coords, slope, y):
    if math.isclose(slope, 0, abs_tol=1e-8):
        ray_x = math.nan
    elif slope is not math.nan:
        ray_x = ((y - (-coords[1])) / slope) + coords[0]
    else:
        ray_x = coords[0]

    return ray_x


#TODO: Cleanup
def get_ray_limits(heading, coords, gameboard, slope, ray_range):
    heading = (2 * math.pi - heading)
    # Get final x and y coordinates given gun range and heading
    if ((0 <= heading <= math.pi / 2
            or (3 * math.pi) / 2 <= heading <= 2 * math.pi)
            or math.isclose((3 * math.pi / 2), heading, abs_tol=1e-8)
            or math.isclose((2 * math.pi), heading, abs_tol=1e-8)):
        if math.isclose(heading, 0, abs_tol=1e-8) or math.isclose(heading,
                                                                  2 * math.pi, abs_tol=1e-8):
            ray_x_limit = coords[0] + ray_range
        else:
            if heading < math.pi / 2:
                ray_x_limit = (
                    coords[0] +
                    abs(
                        ray_range *
                        math.sin(
                            ((math.pi / 2) - heading) %
                            (math.pi / 2))))
            else:
                ray_x_limit = (
                    coords[0] +
                    abs(
                        ray_range *
                        math.sin(
                            heading %
                            (math.pi / 2))))

    else:
        if heading == math.pi or math.isclose(math.pi, heading, abs_tol=1e-8):
            ray_x_limit = coords[0] - ray_range
        else:
            if (3 * math.pi / 2) > heading > math.pi:
                ray_x_limit = (
                    coords[0] -
                    abs(
                        ray_range *
                        math.sin(
                            ((3 * math.pi / 2) - heading) % (math.pi / 2))))
            else:
                ray_x_limit = (
                    coords[0] -
                    abs(
                        ray_range *
                        math.sin(
                            heading % (math.pi / 2))))
    if (math.isclose(heading, 0, abs_tol=1e-8)
            or math.isclose(heading, 2 * math.pi, abs_tol=1e-8)
            or math.isclose(math.pi, heading, abs_tol=1e-8)):
        ray_y_limit = coords[1]
    elif (heading == math.pi / 2):
        ray_y_limit = coords[1] - ray_range
    elif math.isclose(heading, (3 * math.pi / 2), abs_tol=1e-8):
        ray_y_limit = coords[1] + ray_range
    else:
        if (0 <= heading <= math.pi
                or math.isclose(heading, 0, abs_tol=1e-8)
                or math.isclose(heading, math.pi, abs_tol=1e-8)):
            if heading < math.pi / 2:
                ray_y_limit = -(-coords[1] + abs(
                    ray_range * math.cos(((math.pi / 2) - heading) % (math.pi / 2))))
            else:
                ray_y_limit = -(-coords[1] + abs(
                    ray_range * math.cos(heading % (math.pi / 2))))
        else:
            if heading < 3 * math.pi / 2:
                ray_y_limit = -(-coords[1] - abs(
                    ray_range * math.cos(((3 * math.pi / 2) - heading) % (math.pi / 2))))
            else:
                ray_y_limit = -(-coords[1] - abs(
                    ray_range * math.cos(heading % (math.pi / 2))))
    limits = [(ray_x_limit, ray_y_limit)]
    if ray_x_limit < 0:
        x_limit = 0
        y_limit = calculate_ray_y(coords, slope, 0)
        limits.append((x_limit, y_limit))
    if ray_x_limit > gameboard.width:
        x_limit = gameboard.width - .001
        y_limit = calculate_ray_y(coords, slope, gameboard.width)
        limits.append((x_limit, y_limit))
    if ray_y_limit < 0:
        y_limit = 0
        x_limit = calculate_ray_x(coords, slope, 0)
        limits.append((x_limit, y_limit))
    if ray_y_limit > gameboard.height:
        y_limit = gameboard.height - .001
        x_limit = calculate_ray_x(coords, slope, gameboard.height)
        limits.append((x_limit, y_limit))

    limits = sort_coords(coords, limits)

    return limits[0][0]


def sort_objects(coords, collidables, max_range):
    # assign distances, discard if out of bounds
    for ray in list(collidables.keys()):
        dist = round(math.sqrt(
            ((ray.endpoint[0] - coords[0]) ** 2) + (
                (-ray.endpoint[1] - -coords[1]) ** 2)))
        if max_range is not math.nan:
            if dist > max_range:
                collidables.pop(ray)
            else:
                collidables[ray] = dist
    # sort collidables by distance
    collidables = sorted(collidables.items(), key=lambda x: x[1])

    return collidables


def sort_coords(coords, limits):
    cd = {}
    for c in limits:
        dist = round(math.sqrt(
            ((c[0] - coords[0]) ** 2) + (
                (-c[1] - -coords[1]) ** 2)))
        cd[c] = dist
    cd = sorted(cd.items(), key=lambda x: x[1])

    return cd


# Function written by Paul Draper on Stack Exchange
def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return None

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    return x, y


def determine_ray_collision(
        gameboard,
        collidables,
        ray_start,
        slope,
        ray_endpoint,
        dist,
        damage):
    collisions = {}
    for collidable in collidables.keys():
        intersections = []
        top = line_intersection(
            (collidable.hitbox.top_left, collidable.hitbox.top_right),
            (ray_start, ray_endpoint)
        )
        if top:
            intersections.append(top)
        bottom = line_intersection(
            (collidable.hitbox.bottom_left, collidable.hitbox.bottom_right),
            (ray_start, ray_endpoint)
        )
        if bottom:
            intersections.append(bottom)
        left = line_intersection(
            (collidable.hitbox.top_left, collidable.hitbox.bottom_left),
            (ray_start, ray_endpoint)
        )
        if left:
            intersections.append(left)
        right = line_intersection(
            (collidable.hitbox.top_right, collidable.hitbox.bottom_right),
            (ray_start, ray_endpoint)
        )
        if right:
            intersections.append(right)
        for intersection in intersections:
            ray = Ray(
                ray_start,
                intersection,
                collidable,
                damage
            )
            collisions[ray] = 0

    rays = sort_objects(ray_start,
                        collisions,
                        dist)
    if len(rays) > 0:
        return rays[0][0]
    else:
        ray = Ray(
            ray_start,
            ray_endpoint,
            None,
            damage
        )
        return ray


# Determine which object ray collides with first
def determine_gun_collision(
        player,
        gameboard,
        collidables,
        slope,
        ray_endpoint,
        damage):
    origin = ((player.shooter.hitbox.position[0] + (player.shooter.hitbox.width / 2)),
              (player.shooter.hitbox.position[1] + (player.shooter.hitbox.height / 2)))
    # Ray object used to provide data for visualizer
    collisions = {}
    for collidable in collidables.keys():
        intersections = []
        top = line_intersection(
            (collidable.hitbox.top_left, collidable.hitbox.top_right),
            (origin, ray_endpoint)
        )
        if top:
            intersections.append(top)
        bottom = line_intersection(
            (collidable.hitbox.bottom_left, collidable.hitbox.bottom_right),
            (origin, ray_endpoint)
        )
        if bottom:
            intersections.append(bottom)
        left = line_intersection(
            (collidable.hitbox.top_left, collidable.hitbox.bottom_left),
            (origin, ray_endpoint)
        )
        if left:
            intersections.append(left)
        right = line_intersection(
            (collidable.hitbox.top_right, collidable.hitbox.bottom_right),
            (origin, ray_endpoint)
        )
        if right:
            intersections.append(right)
        for intersection in intersections:
            ray = Ray(
                origin,
                intersection,
                collidable,
                player.shooter.primary_gun.damage
            )
            collisions[ray] = 0

    rays = sort_objects(origin,
                        collisions,
                        player.shooter.primary_gun.range)
    if len(rays) > 0:
        return rays[0][0]
    else:
        ray = Ray(
            origin,
            ray_endpoint,
            None,
            player.shooter.primary_gun.damage
        )
        return ray


def get_ray_collision(gameboard, ray_start, heading, dist, damage, exclusions):
    radians = (2*math.pi) - math.radians(heading)
    slope = calculate_slope(radians)
    ray_endpoint = get_ray_limits(radians,
                                  ray_start,
                                  gameboard,
                                  slope,
                                  dist)
    collidables = load_collidables_in_ray_range(
        radians,
        ray_start,
        gameboard,
        ray_endpoint,
        exclusions
    )

    ray = determine_ray_collision(
        gameboard,
        collidables,
        ray_start,
        slope,
        ray_endpoint,
        dist,
        damage
    )

    return ray


def get_gun_ray_collision(player, gameboard):
    radians = math.radians(player.shooter.heading)
    radians = (2 * math.pi - radians)
    slope = calculate_slope(radians)
    origin = ((player.shooter.hitbox.position[0] + (player.shooter.hitbox.width / 2)),
              (player.shooter.hitbox.position[1] + (player.shooter.hitbox.height / 2)))
    ray_endpoint = get_ray_limits(radians,
                                  origin,
                                  gameboard,
                                  slope,
                                  player.shooter.primary_gun.range)
    collidables = load_collidables_in_ray_range(
        radians,
        origin,
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
