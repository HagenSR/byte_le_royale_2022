=====================
Player Utilities
=====================

Important Notes
================

Basic functions have been provided to help you create your AI.

Function List
===============

check_collision
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   player_utils.check_collision(hitbox_one: Hitbox, hitbox_two: Hitbox) -> bool

Method that returns if two hitbox objects overlap

distance
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   player_utils.distance(x1: float, y1: float, x2: float, y2: float) -> float

Returns how far the given points are from each other


distance_tuples
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   player_utils.distance(x1: float, y1: float, x2: float, y2: float) -> float

Returns how far the given points are from each other


angle_to_point
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   player_utils.angle_to_point(player, coord_tuple: tuple) -> int

Returns the angle you need to travel in to go from one point to another
(Not considering any obstacle)

**NOTE: if the angle measurement is a fraction, it will be truncated and returned
as an int. This should still point you close to the desired direction.**


code
======

Below is the code for each method

.. code-block:: python

    import math
    from game.common.hitbox import Hitbox


    def check_collision(hitbox_one: Hitbox, hitbox_two: Hitbox) -> bool:
        return (hitbox_one.top_left[0] < hitbox_two.top_right[0] and
                hitbox_one.top_right[0] > hitbox_two.top_left[0] and
                hitbox_one.top_left[1] < hitbox_two.bottom_left[1] and
                hitbox_one.bottom_right[1] > hitbox_two.top_right[1])


    def distance(x1: float, y1: float, x2: float, y2: float) -> float:
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1 / 2)


    def distance_tuples(coord_tuple1: tuple, coord_tuple2: tuple) -> float:
        return distance(coord_tuple1[0], coord_tuple1[1], coord_tuple2[0], coord_tuple2[1])


    def angle_to_point(player, coord_tuple: tuple) -> float:
            # Yoinked from
        # https://stackoverflow.com/questions/2676719/calculating-the-angle-between-a-line-and-the-x-axis/27481611#27481611
        deltaY = coord_tuple[1] - player.hitbox.position[1]
        deltaX = coord_tuple[0] - player.hitbox.position[0]
        result = math.degrees(math.atan2(deltaY, deltaX))
        return result + 360 if result < 0 else result
