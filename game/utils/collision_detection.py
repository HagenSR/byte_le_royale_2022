import numpy as np


def check_collision(hitbox_one, hitbox_two):
    return (hitbox_one.top_left[0] < hitbox_two.top_right[0] and
            hitbox_one.top_right[0] > hitbox_two.top_left[0] and
            hitbox_one.top_left[1] < hitbox_two.bottom_left[1] and
            hitbox_one.bottom_right[1] > hitbox_two.top_right[1])


def point_in_hitbox(x, y, hitbox):
    return (hitbox.bottom_left[0] <= x <= hitbox.top_right[0] and
            hitbox.top_right[1] <= y <= hitbox.bottom_left[1])


def intersect_circle(center, radius, hitbox):
    # check if the center is entirely inside the circle
    if point_in_hitbox(center[0], center[1], hitbox):
        return True

    edges = [
        [hitbox.top_left, hitbox.top_right],
        [hitbox.top_right, hitbox.bottom_right],
        [hitbox.bottom_left, hitbox.bottom_right],
        [hitbox.top_left, hitbox.bottom_left]
    ]
    x3 = center[0]
    y3 = center[1]
    for edge in edges:
        x1 = edge[0][0]
        x2 = edge[1][0]
        y1 = edge[0][1]
        y2 = edge[1][1]

        # setup vectors for a, b on line L
        a = np.array([x1, y1])
        b = np.array([x2, y2])
        # direction vector m
        m = b - a
        # independent point p
        p = np.array([x3, y3])

        # running parameter t at the orthogonal intersection t0
        t0 = m.dot(p - a) / m.dot(m)

        # intersection point
        intersect_pnt = a + t0 * m

        # find distance d accounting for line segment
        if t0 <= 0:
            d = p - a
        elif 0 < t0 < 1:
            d = p - (a + t0 * m)
        else:
            d = p - b
        seg_len = np.linalg.norm(d)

        # if the line segment from the radius perpendicular to the edge is less than the total length of the radius,
        # the rectangle intersects the circle
        if seg_len < radius:
            return True

    return False


def distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1 / 2)


def distance_tuples(coord_tuple1, coord_tuple2):
    return distance(coord_tuple1[0], coord_tuple1[1], coord_tuple2[0], coord_tuple2[1])


def is_point_in_path(x: int, y: int, poly) -> bool:
    # Determine if the point is in the polygon.
    # Taken from: https://wrf.ecse.rpi.edu/Research/Short_Notes/pnpoly.html#License%20to%20Use
    #
    # Args:
    #   x -- The x coordinates of point.
    #   y -- The y coordinates of point.
    #   poly -- a list of tuples [(x, y), (x, y), ...]
    #
    # Returns:
    #   True if the point is in the path or is a corner or on the boundary

    num = len(poly)
    j = num - 1
    c = False
    for i in range(num):
        if (x == poly[i][0]) and (y == poly[i][1]):
            # point is a corner
            return True
        if (poly[i][1] > y) != (poly[j][1] > y):
            slope = (x - poly[i][0]) * (poly[j][1] - poly[i][1]) - \
                    (poly[j][0] - poly[i][0]) * (y - poly[i][1])
            if slope == 0:
                # point is on boundary
                return True
            if (slope < 0) != (poly[j][1] < poly[i][1]):
                c = not c
        j = i
    return c
