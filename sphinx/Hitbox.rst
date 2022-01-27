==========
Hitbox
==========

Every map object has a Hitbox. This Hitbox is a rectangle of varying sizes. Collisions on the game map are determined by overlapping Hitboxes.

Properties
-------------

The Hitbox object has the following properties.

================  =========================== ===================
 Name              Type                        Description
================  =========================== ===================
 width              number                      The width of the bounding Hitbox
 height             number                      The height of the bounding Hitbox
 rotation           degrees                     The rotation of the Hitbox, in degrees
 position           (number, number) tuple      The x, y position of the top left corner of the Hitbox
 top_left           (number, number) tuple      The x, y position of the top left corner of the Hitbox
 top_right          (number, number) tuple      The x, y position of the top right corner of the Hitbox
 bottom_left        (number, number) tuple      The x, y position of the bottom left corner of the Hitbox
 bottom_right       (number, number) tuple      The x, y position of the bottom right corner of the Hitbox
 middle             (number, number) tuple      The x, y position of the middle of the Hitbox
 __str__            string                      Outputs height, width, x, y
================  =========================== ===================