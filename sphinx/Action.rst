=====================
Taking Action
=====================

The Action Object
------------------

Taking actions is managed by an action object passed to the player each turn.
This comes in as "actions" in the take_turns() method in your client.

Available Actions
------------------

Each turn you can take one action.
If you take multiple actions your client will do the last one that is set.

Moving
======

.. code-block:: python

    actions.set_move(heading: int, speed: int) -> None

This will set your movement in the direction of heading (in degrees)
and speed (in game units).
Check out documentation on moving to learn more.

Shooting
========

.. code-block:: python

    actions.set_shoot(heading: int) -> None

This will set your intent to shoot in the direction of heading (in degrees).
If you're not currently holding a gun, this will throw an error.
Check out the documentation on shooting and guns to learn more.

Interact
========

.. code-block:: python

    actions.set_action(ActionType.interact) -> None

This will set your intent to interact with items on the map, including opening doors and picking up items.
Remember that ActionType.interact is an enum!
(So you need to make sure you leave in the import for enums in the given client)

Reload
======

.. code-block:: python

    actions.set_action(ActionType.reload) -> None

This will use your action to reload your gun. You have infinite ammo, but a limited magazine.
This means your gun will run out of ammo in it's magazine, but you can reload as many times as you like.

Shop
====

.. code-block:: python

    actions.select_item_to_buy(consumable_enum: Enum) -> None

This will set your intention to buy an object from the shop. You pass in the enum of the consumable you want to buy.
If you have enough money, it will add the object to your inventory and subtract the amount it costs from your money.
Check out the consumables page and list of consumable enums to see your options!

Use Consumable Item
====================

.. code-block:: python

    actions.select_item_to_use(consumable_enum: Enum) -> None

This will set your intention to use a consumable object from your inventory.
You pass in the enum of the type of object you want to use, and if there is one of that type in your inventory,
it will be used. Checkout the list of consumables to see the items and enums!


Note: This is not used for grenades, if you try to pass the Consumables.grenade it will throw an error

Throw Grenade
=============

.. code-block:: python

    actions.set_throw_grenade(heading: int, distance_to_throw: int) -> None

This will set your intent to throw a grenade.
Heading is in degrees, distance_to_throw must be less than the max throwing distance
which is 75 game units.

Use Teleporter
==============

.. code-block:: python

    actions.set_action(ActionType.use_teleporter) -> None

This will set your intent to use a teleporter. You must be standing on a teleporter for this to work, and
you will then be teleported to a random different teleporter. Both of these teleporters will be disabled for
a short delay, then re-enabled.

Cycle Primary Gun
==================

.. code-block:: python

    actions.cycle_primary()

This will cycle your selected gun in your shooter's inventory to the next one in the inventory.
Note: this does not use up your action for the turn!

Drop Item
==========

.. code-block:: python

    actions.drop_item(enum: Enum, sub_enum: Enum)

This will drop an item of a specific enum. Pass it one of the ObjectType enums or
it might drop the wrong thing. It will search for the first match in your inventory of that
type and remove it.

sub_enum should be the corresponding type of the object you want to drop.
For example, gun should be enum GunType, upgrade should be enum Upgrades, consumable should
be enum Consumables

Due to the Amazon return policy, the item does not go on the map but
gets sent back to Amazon returns with no refund.

If you drop a backpack upgrade, this will also remove slots in your inventory.
It removes the last slots in your inventory first, so make sure you don't have any items there
or you will lose them!

Note: this does not use up your action for the turn!