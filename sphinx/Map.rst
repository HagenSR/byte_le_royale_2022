======================
The Game Map
======================

General Layout
-----------------

The map is a continuous cartesian grid with nine subplots separated by a small open margin. In each subplot except the middle
a randomly chosen predefined structure of walls and doors will spawn. Navigating these structures is a task left to the player.

Item loot generation
---------------------

Loot will be spawned at the start of the game and in three waves after the game starts. This loot spawns with the following probabilities.

================= =======================
  Object           Spawn Chance
================= =======================
  Money            60%
  Upgrade          20%
  Gun              20%
================= ======================= 

This loot will spawn randomly into unoccupied locations within the death circle.

The Partition Grid is a data structure built to help players efficiently find objects within the game map near the player.
