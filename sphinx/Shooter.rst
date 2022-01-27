=========
Shooter
=========
The shooter object represents your character in the game.
In contains information on location, inventory, view stats, etc.

================ =========== ===========
Name             Type        Description
================ =========== ===========
hitbox           Hitbox      Hitbox of where the shooter is on the map
view_distance    int         Radius of circle that represents your field of view
max_speed        int         Max speed a player can move in a turn
money            int         Amount of money the player has each turn
armor            int         percentage of damage that will be done to the player, will change if the player picks up armor
shield           bool        whether the player has a shield active or not
inventory        dictionary  contains inventory objects referenced by slot type
================ =========== ===========

The shooter starts with a level one handgun in the inventory

Inventory
---------

The player inventory contains all the objects the player is currently holding.

Here is a representation of the default inventory structure:

.. code-block:: python

    inventory = {
        'guns': [Handgun, None],
        'upgrades': [None, None, None]
        'consumables': [None, None, None]
    }

It has 3 types of slots: guns, upgrades, and consumables

By default, the player has 2 slots for guns, 3 slots for upgrades, and 3 slots for consumables.

Empty slots are represented by none objects

Changing selected primary gun can be done in the action object.

Methods
--------

has_empty_slot
^^^^^^^^^^^^^^^^

.. code-block:: python

    shooter.has_empty_slot(slot_type: string) -> bool

check if there's an empty slot of a particular type in the inventory

primary_gun
^^^^^^^^^^^^^

.. code-block:: python

    shooter.primary_gun()

Returns the Gun object of the currently equipped gun
