======================
The Game Board
======================

General Layout
-----------------

The map is a continuous cartesian grid with nine subplots separated by a small open margin. In each subplot except the middle
a randomly chosen predefined structure of walls and doors will spawn. Navigating these structures is a task left to the player.
Note that the (X,Y) representation of the map follows "display" logic, where an increase in X represents a movement towards the 
Right but an increase in Y represents a downward movement. Also note the "backwards" degree rotation where an increase in degrees 
moves counter-clockwise (see movement controller). The corridors between structures are 20 units wide
while structures are 140 x 140 plots seperated by the corridors.

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


================ ================= ===========
 Name              Type             Description
================ ================= ===========
 width            int               The width of the game board 
 height           int               The height of the game board
 partition_grid   PartitionGrid     The partition grid object for the entire game 
 ray_list         list of rays      Used in controller logic, not for you!
 center           (int,int) tuple   The (x, y) center of the game board
 cirlce_radius    number            The current radius of the safe zone
================ ================= ===========
