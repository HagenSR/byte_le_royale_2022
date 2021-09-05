from game.common.hitbox import Hitbox
from game.common.stats import GameStats
from game.common.enums import *


def check_collision(hitbox_one, hitbox_two):
    return (hitbox_one.topLeft[0] < hitbox_two.topRight[0] and
            hitbox_one.topRight[0] > hitbox_two.topLeft[0] and
            hitbox_one.topLeft[1] < hitbox_two.bottomLeft[1] and
            hitbox_one.bottomRight[1] > hitbox_two.topRight[1])


def arc_intersect(center, radius, arc_len_degree, hitbox, heading):
    # TODO implement this for arcs, currently calculates for an entire circle around the player
    return point_in_hitbox(
        center[0],
        center[1],
        hitbox) or intersect_circle(
        center,
        radius,
        hitbox)


def point_in_hitbox(x, y, hitbox):
    return (hitbox.bottomLeft[0] < x < hitbox.topRight[0] and
            hitbox.bottomLeft[1] < y < hitbox.topRight[1])


def intersect_circle(center, radius, hitbox):
    edges = [
        [hitbox.topleft, hitbox.topright],
        [hitbox.topRight, hitbox.bottomRight],
        [hitbox.bottomRight, hitbox.bottomLeft],
        [hitbox.bottomLeft, hitbox.topLeft]
    ]
    x3 = center[0]
    y3 = center[1]
    for edge in edges:
        x1 = edge[0][0]
        x2 = edge[1][0]
        y1 = edge[0][1]
        y2 = edge[1][1]

        # calculate x coord of the intercept of the edge and the radius perpendicular to the edge
        # numerator
        xin = (y3 * (x2 - x1) - ((x2 - x1) ** 2 / y1 - y2)
               * x3 - (x1 * y2 - x2 * y1))
        # denominator
        xid = ((y1 - y2) - ((x2 - x1) ** 2 / (y1 - y2)))
        xi = xin / xid

        # calculate y coord of the intercept of the edge and the radius
        # perpendicular to the edge
        yi = ((x2 - x1) / (y1 - y2)) * x3 - y3 - ((x2 - x1) / (y1 - y2)) * xi

        # calculate length of perpendicular line segment from radius to the
        # edge
        seg_len = ((xi - y3) ** 2 + (yi - y3) ** 2) ** (1 / 2)

        # if the line segment from the radius perpendicular to the edge is less than the total length of the radius,
        # the rectangle intercepts with the rectangle
        # need to also check that the intersect point is actually between the two endpoints of the edge
        # and to adjust for the arc, need to check the slope of the perp. line is between the two slopes of the bounding
        # lines of the arc
        if seg_len < radius and x1 <= xi <= x2 and y1 <= yi <= y2:
            return True

    return False
