==============================
Item Generation Utils Methods
==============================

remove_items_from_map
---------------------

Removes all items from the map. Is called before spawning a new wave of loot.

has_reached_item_cap
--------------------

Determines if too many of a type of item (gun, upgrade, money) spawns on the map and prevents another from spawning if there are too many.

pick_item
---------
Picks what item to spawn. 60% chance of money, 20% chance of a gun, and 20% chance of an upgrade.

place_item
----------
Places an item randomly on the map, will not spawn an item on top of another item. Items are placed on a standard distribution with the highest chance of spawning at the center of the map.






