import math


def check_collision(hitbox_one, hitbox_two):
    return (hitbox_one.top_left[0] < hitbox_two.top_right[0] and
            hitbox_one.top_right[0] > hitbox_two.top_left[0] and
            hitbox_one.top_left[1] < hitbox_two.bottom_left[1] and
            hitbox_one.bottom_right[1] > hitbox_two.top_right[1])


def arc_intersect_rect(center, radius, arc_len_degree, hitbox, heading):
    return point_in_hitbox(
        center[0],
        center[1],
        hitbox) or intersect_arc(
        center,
        radius,
        hitbox,
        heading,
        arc_len_degree)


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

        b = distance(x1, y1, x3, y3)
        d = distance(x3, y3, x2, y2)
        ac = distance(x1, y1, x2, y2)
        a = (b**2 - d**2) / (2 * ac) + ac / 2

        angle = math.acos((b**2 + ac**2 - d**2) / (2 * b * ac))

        xi = x1 + math.cos(angle) * a
        yi = y1 + math.sin(angle) * a

        # calculate length of perpendicular line segment from radius to the
        # edge
        seg_len = distance(xi, yi, x3, y3)

        # if the line segment from the radius perpendicular to the edge is less than the total length of the radius,
        # the rectangle intercepts with the rectangle
        # need to also check that the intersect point is actually between the two endpoints of the edge
        # and to adjust for the arc, need to check the slope of the perp. line is between the two slopes of the bounding
        # lines of the arc
        if (seg_len < radius and ((distance(x1, y1, x3, y3) < radius or distance(
                x2, y2, x3, y3) < radius) or (x1 <= xi <= x2 and y1 <= yi <= y2))):
            return True

    return False


def distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1 / 2)


def distance_tuples(coord_tuple1, coord_tuple2):
    return distance(coord_tuple1[0], coord_tuple1[1], coord_tuple2[0], coord_tuple2[1])


def intersect_arc(center, radius, arc_len_deg, hitbox, heading):
    # This method checks intersection with an arc
    # However, for simplification it cuts the chord off and assumes it's a
    # triangle instead.

    # define left most point of arc
    a1 = (
        radius *
        math.cos(
            math.radians(
                heading -
                arc_len_deg /
                2)) +
        center[0],
        radius *
        math.sin(
            math.radians(
                heading -
                arc_len_deg /
                2)) +
        center[1])
    # define right most point of arc
    a2 = (
        radius *
        math.cos(
            math.radians(
                heading +
                arc_len_deg /
                2)) +
        center[0],
        radius *
        math.sin(
            math.radians(
                heading +
                arc_len_deg /
                2)) +
        center[1])
    # define left half of arc
    arc1 = [
        center,
        (radius * math.cos(math.radians(heading)) + center[0],
         radius * math.sin(math.radians(heading)) + center[1]),
        a1
    ]
    # define right half of arc
    arc2 = [
        center,
        (radius * math.cos(math.radians(heading)) + center[0],
         radius * math.sin(math.radians(heading)) + center[1]),
        a2
    ]
    arcs = [arc1, arc2]

    for arc in arcs:
        dilation = set()
        r = hitbox.bottom_right
        rect = [
            hitbox.top_left,
            hitbox.top_right,
            hitbox.bottom_left,
            hitbox.bottom_right]
        for pa in arc:
            for pr in rect:
                dilation.add((pa[0] + pr[0], pa[1] + pr[1]))
        r_polar = (
            distance(r[0], r[1], center[0], center[1]),
            math.degrees(math.atan(
                math.fabs(center[1] - r[0]) / math.fabs(center[0] - r[0])
            ))
        )
        # print('START')
        # print(is_point_in_path(r[0], r[1], list(dilation)))
        # print(r_polar[0] < radius)
        # print(heading -
        #       arc_len_deg / 2 < r_polar[1] < heading + arc_len_deg / 2)
        if is_point_in_path(r[0], r[1], list(dilation)) and r_polar[0] < radius and heading - \
                arc_len_deg / 2 < r_polar[1] < heading + arc_len_deg / 2:
            # to do something is screwy with this polar coord checking
            return True
    return False


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
