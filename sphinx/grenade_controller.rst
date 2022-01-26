=====================
Grenade Controller
=====================

Important Notes
---------------

The grenade controller will allow a player to throw a grenade in a specified direction a specified distance. There is nothing that can impede a grenade throw (i.e. you can throw over walls, doors, players, etc...).

The grenade explodes with a fixed radius of 40 units, and the maximum distance thrown is 75 units.

Example
-------
.. code-block:: python

    actions.set_throw_grenade(heading = int(90), distance_to_throw = int(60))

Will throw a grenade straight below the player, a distance of 60 units.
