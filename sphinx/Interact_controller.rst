======================
Interact Controller
======================



Basic Info
-----------------

This controller allows you to interact with object on the game board. The objects shooters can interact with are
consumables, upgrades, money, and doors.
    **NOTE: Items have higher precedence than doors in the interact controller. If
    you want to interact with a door, make sure you are not standing on an item before ending your
    turn.**


Picking up Items
-----------------

Shooters are able to pick up items by standing over them and setting their action to interact.

Opening/Closing Doors
-----------------

To open or close a door, the middle coordinates of the shooter hitbox must be within a distance of 10 units
from the door. Once doors are within range, the interact controller will then interact with the closest door.

Example Code
------------

.. code-block:: python
    actions.set_action(ActionType.interact)

