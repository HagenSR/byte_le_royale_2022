=======================
Calculate New Location
=======================

Important Notes
-----------------

The calculate_new_location util is a method used in the movement controller. Given a starting location, speed and angle it calculates the next position.



Code
------------

.. code-block:: python

    def calculate_location(origin, speed, direction):
        new_x = origin[0] + (speed * math.cos(direction))
        new_y = origin[1] + (speed * math.sin(direction))

        return new_x, new_y
