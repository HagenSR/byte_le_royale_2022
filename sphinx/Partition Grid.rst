========
Partition Grid
========
What is it?
-----------
The partition grid is an internal data structure used by the game board to make finding objects
on the map easy and efficient.

It works by splitting up the map of 500x500 game units into squares that are each 20x20 units.
This means that the map consists of 25x25 partitions.

Your client is passed in a PartitionGrid object within the GameBoard object by default named game_board.
You can access the PartitionGrid object by calling ``game_board.partition``

Obfuscation
-------

The partition grid given to your client isn't the same partition grid used by the engine,
instead it is a deepcopy of the internal one.

During this process of deep copying, it is also filtered to remove any players or items that are outside of your
client's view. See the page on what your client can see to learn more.

How to use it
-------------
The partition grid is meant to make it easy for you to find all the objects you need, however, if your team
decides it is too complex, buggy, or not right for you, there is another option.

Instead of using the partitions you can get a list of all the objects in the map.
To do this, you can use this method:

.. code-block:: python

    partition_grid.get_all_objects() -> list

This will return a list of all objects contained in a python list object.

-----------

If you do want to use the partition as the partition grid object, there are a number of helpful methods to allow
you to efficiently find objects in particular locations.

The PartitionGrid is a 3 dimensional list, with the most interior list containing a subset of the objects within the map.

Properties
=======
The partition grid has a couple of properties:

.. code-block:: python

    partition_grid.partition_width

Width of a single partition in game units

.. code-block:: python

    partition_grid.partition_height

Height of a single partition in game units

.. code-block:: python

    partition_grid.partitions_tall

How many partitions tall the grid is

.. code-block:: python

    partition_grid.partitions_wide

How many partitions wide the grid is

Methods
=======
get_partition_objects
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   partition_grid.get_partition_objects(x: float, y: float) -> list

This method returns all objects within the partition that encompasses point (x, y)

get_partition_objects_by_index
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    partition_grid.get_partition_objects_by_index(row: int, column: int) -> list

This method returns all objects at the partition at the given row and column.

find_object_coordinates
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    partition_grid.find_object_coordinates(x: float, y: float) -> obj, bool

Returns the object at point (x, y) if there is an object at those coordinates, false otherwise

find_objects_hitbox
^^^^^^^^^

.. code-block:: python

    partition_grid.find_object_hitbox(hitbox: Hitbox) -> obj, bool

Returns the object if there is an object on the map that collides with the given hitbox, false otherwise

find_object_object
^^^^^^^

.. code-block:: python

    partition_grid.find_object_object(given_obj: MapObject) -> obj, bool

Returns object if there is an object that collides with the given object, false otherwise

remove_object
^^^^^^

.. code-block:: python

    partition_grid.remove_object(obj: MapObject) -> None

Removes a given object from the structure. Note, because the client has it's own copy of the partition grid, it will not
remove it from the game entirely. Will most likely not be useful to you, but it's here if you want to use it.
