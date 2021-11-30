import math


# My work


def check_collision(hitbox_one, hitbox_two):
    return (hitbox_one.top_left[0] < hitbox_two.top_right[0] and
            hitbox_one.top_right[0] > hitbox_two.top_left[0] and
            hitbox_one.top_left[1] < hitbox_two.bottom_left[1] and
            hitbox_one.bottom_right[1] > hitbox_two.top_right[1])


###############################################################################


# def collide_rect_hb(hb1, hb2):
#     p1 = [hb1.topRight, hb1.topLeft, hb1.bottomLeft,
#           hb1.bottomRight]
#     p2 = [hb2.topRight, hb2.topLeft, hb2.bottomLeft,
#           hb2.bottomRight]
#
#     """
#     Return True and the MPV if the shapes collide. Otherwise, return False and
#     None.
#
#     p1 and p2 are lists of ordered pairs, the vertices of the polygons in the
#     counterclockwise direction.
#     """
#
#     # p1 = [np.array(v, 'float64') for v in p1]
#     # p2 = [np.array(v, 'float64') for v in p2]
#
#     edges = edges_of(p1)
#     edges += edges_of(p2)
#     orthogonals = [orthogonal(e) for e in edges]
#
#     push_vectors = []
#     for o in orthogonals:
#         separates, pv = is_separating_axis(o, p1, p2)
#
#         if separates:
#             # they do not collide and there is no push vector
#             return False
#         else:
#             push_vectors.append(pv)
#
#     # they do collide and the push_vector with the smallest length is the MPV
#     mpv = min(push_vectors, key=(lambda v: np.dot(v, v)))
#
#     # assert mpv pushes p1 away from p2
#     d = centers_displacement(p1, p2)  # direction from p1 to p2
#     if np.dot(d, mpv) > 0:  # if it's the same direction, then invert
#         mpv = -mpv
#
#     # return True, mpv
#     return True
#
#
# def centers_displacement(p1, p2):
#     """
#     Return the displacement between the geometric center of p1 and p2.
#     """
#     # geometric center
#     c1 = np.mean(np.array(p1), axis=0)
#     c2 = np.mean(np.array(p2), axis=0)
#     return c2 - c1
#
#
# def edges_of(vertices):
#     """
#     Return the vectors for the edges of the polygon p.
#
#     p is a polygon.
#     """
#     edges = []
#     N = len(vertices)
#
#     for i in range(N):
#         edge = [vertices[(i + 1) % N][j] - vertices[i][j] for j in range(len(vertices[i]))]
#         edges.append(edge)
#
#     return edges
#
#
# def orthogonal(v):
#     """
#     Return a 90 degree clockwise rotation of the vector v.
#     """
#     return np.array([-v[1], v[0]])
#
#
# def is_separating_axis(o, p1, p2):
#     """
#     Return True and the push vector if o is a separating axis of p1 and p2.
#     Otherwise, return False and None.
#     """
#     min1, max1 = float('+inf'), float('-inf')
#     min2, max2 = float('+inf'), float('-inf')
#
#     for v in p1:
#         projection = np.dot(v, o)
#
#         min1 = min(min1, projection)
#         max1 = max(max1, projection)
#
#     for v in p2:
#         projection = np.dot(v, o)
#
#         min2 = min(min2, projection)
#         max2 = max(max2, projection)
#
#     if max1 >= min2 and max2 >= min1:
#         d = min(max2 - min1, max1 - min2)
#         # push a bit more than needed so the shapes do not overlap in future
#         # tests due to float precision
#         d_over_o_squared = d / np.dot(o, o) + 1e-10
#         pv = d_over_o_squared * o
#         return False, pv
#     else:
#         return True, None


##########################################################################


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


# def hitbox_angle(player_center, hitbox)


# def intersect_arc(center, radius, hitbox, heading, arc_len_deg):

def intersect_circle(center, radius, hitbox):
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
