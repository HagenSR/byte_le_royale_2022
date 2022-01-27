=====
Door
=====

The door is an object that will open if the player is nearby (look at interact controller for more information) The door is 10 x 3, so the player must be lined up with the door to pass through (player is 10 x 10). You cannot collide with a door if it is open, only if it is closed.

Instance Variables
------------------

================  =========================== ===================
 Name              Type                        Description
================  =========================== ===================
Hitbox             Hitbox                      The doors hitbox
Health             int                         How much health the door has
Open Speed         int                         Speed at which door opens (opens instantly)
Open State         boolean                     Determines if door is open
Collidable         boolean                     Determines if door is collidable
================  =========================== ===================
