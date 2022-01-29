=========================
Teleporter Controller
=========================

The teleporter controller contains the logic when the player wants to use a teleporter. Two conditions must be met if a player wants to use a teleporter. First, their hitbox must be colliding with that of the teleporter. Secondly, the teleporter must not have been used in the past five turns (in other words it is enabled). When used, a teleporter will teleport the player at random to one of the other four teleporters on the map. Deactivating both for five turns.

Example
-------
.. code-block:: python

    actions.set_action(ActionType.use_teleporter)




