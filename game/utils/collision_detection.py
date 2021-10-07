import math


def check_collision(hitbox_one, hitbox_two):
    return (hitbox_one.topLeft[0] < hitbox_two.topRight[0] and
            hitbox_one.topRight[0] > hitbox_two.topLeft[0] and
            hitbox_one.topLeft[1] < hitbox_two.bottomLeft[1] and
            hitbox_one.bottomRight[1] > hitbox_two.topRight[1])


def intersect_circle(center, radius, hitbox):
    edges = [
        [hitbox.topLeft, hitbox.topRight],
        [hitbox.topRight, hitbox.bottomRight],
        [hitbox.bottomLeft, hitbox.bottomRight],
        [hitbox.topLeft, hitbox.bottomLeft]
    ]
    x3 = center[0]
    y3 = center[1]
    for edge in edges:
        x1 = edge[0][0]
        x2 = edge[1][0]
        y1 = edge[0][1]
        y2 = edge[1][1]

        # check for edge being vertical
        if x1 == x2:
            xi = x1
            yi = y3
            dx4 = math.nan
        # check for edge being horizontal
        elif y1 == y2:
            xi = x3
            yi = y1
            dx4 = 0
        else:
            # calculate x coord of the intercept of the edge and the radius perpendicular to the edge
            # numerator
            xin = (y3 * (x2 - x1) - ((x2 - x1) ** 2 / y1 - y2)
                   * x3 - (x1 * y2 - x2 * y1))
            # denominator
            xid = ((y1 - y2) - ((x2 - x1) ** 2 / (y1 - y2)))
            xi = xin / xid

            # calculate y coord of the intercept of the edge and the radius
            # perpendicular to the edge
            yi = ((x2 - x1) / (y1 - y2)) * x3 - \
                y3 - ((x2 - x1) / (y1 - y2)) * xi

        # calculate length of perpendicular line segment from radius to the
        # edge
        seg_len = distance(xi, yi, x3, y3)

        # if the line segment from the radius perpendicular to the edge is less than the total length of the radius,
        # the rectangle intercepts with the rectangle
        # need to also check that the intersect point is actually between the two endpoints of the edge
        # and to adjust for the arc, need to check the slope of the perp. line is between the two slopes of the bounding
        # lines of the arc
        if (seg_len < radius and ((distance(x1, y1, x3, y3) < radius or distance(
                x2, y2, x3, y3) < radius) or x1 <= xi <= x2 and y1 <= yi <= y2)):

            return True

    return False


def distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1 / 2)


def intersect_arc(center, radius, arc_len_deg, hitbox, heading):
    # define left most point of arc
    a1 = (radius * math.cos(math.radians(heading - arc_len_deg / 2)) + center[0],
          radius * math.sin(math.radians(heading - arc_len_deg / 2)) + center[1])
    # define right most point of arc
    a2 = (radius * math.cos(math.radians(heading + arc_len_deg / 2)) + center[0],
          radius * math.sin(math.radians(heading + arc_len_deg / 2)) + center[1])
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
        r = hitbox.bottomRight
        rect = [hitbox.topLeft, hitbox.topRight, hitbox.bottomLeft, hitbox.bottomRight]
        for pa in arc:
            for pr in rect:
                dilation.add((pa[0] + pr[0], pa[1] + pr[1]))
        r_polar = (
            distance(r[0], r[1], center[0], center[1]),
            math.atan(
                math.fabs(center[1] - r[0]) / math.fabs(center[0] - r[0])
            )
        )
        if is_point_in_path(r[0], r[1], list(dilation)) and r_polar[0] < radius and heading - arc_len_deg / 2 < r_polar[1] < heading + arc_len_deg / 2:
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
