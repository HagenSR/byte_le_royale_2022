import math
from game.common.hitbox import Hitbox
from game.common.stats import GameStats
from game.common.enums import *


def check_collision(hitbox_one, hitbox_two):
    return (hitbox_one.topLeft[0] < hitbox_two.topRight[0] and
            hitbox_one.topRight[0] > hitbox_two.topLeft[0] and
            hitbox_one.topLeft[1] < hitbox_two.bottomLeft[1] and
            hitbox_one.bottomRight[1] > hitbox_two.topRight[1])


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
    return (hitbox.bottomLeft[0] <= x <= hitbox.topRight[0] and
            hitbox.topRight[1] <= y <= hitbox.bottomLeft[1])


def intersect_arc(center, radius, hitbox, heading, arc_len_deg):
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
            xin = (y3 * (x2 - x1) - ((x2 - x1) ** 2 / y1 - y2) * x3 - (x1 * y2 - x2 * y1))
            # denominator
            xid = ((y1 - y2) - ((x2 - x1) ** 2 / (y1 - y2)))
            xi = xin / xid

            # calculate y coord of the intercept of the edge and the radius
            # perpendicular to the edge
            yi = ((x2 - x1) / (y1 - y2)) * x3 - y3 - ((x2 - x1) / (y1 - y2)) * xi

            dx4 = -1 * ((y1 - y2) / (x2 - x1))

        # calculate length of perpendicular line segment from radius to the
        # edge
        seg_len = distance(xi, yi, x3, y3)

        d_arc1 = math.tan(heading + arc_len_deg / 2)
        d_arc2 = math.tan(heading - arc_len_deg / 2)

        # if the line segment from the radius perpendicular to the edge is less than the total length of the radius,
        # the rectangle intercepts with the rectangle
        # need to also check that the intersect point is actually between the two endpoints of the edge
        # and to adjust for the arc, need to check the slope of the perp. line is between the two slopes of the bounding
        # lines of the arc
        if (seg_len < radius and
                ((distance(x1, y1, x3, y3) < radius or distance(x2, y2, x3, y3) < radius) or
                 x1 <= xi <= x2 and y1 <= yi <= y2)):
            # TODO add check for arc, currently only checks circle
            return True

    return False


def distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1 / 2)
