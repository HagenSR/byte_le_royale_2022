
# origin is xy tuple; direction must be in radians
import math


def calculate_location(origin, speed, direction):
    new_x = origin[0] + (speed * math.cos(direction))
    new_y = origin[1] + (speed * math.sin(direction))

    return new_x, new_y
