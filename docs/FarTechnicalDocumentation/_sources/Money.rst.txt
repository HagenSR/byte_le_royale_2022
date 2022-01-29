=================
Money
=================

Basic Info
------------------

Throughout the game, money will spawn on the map for
the shooter to pick up.

Instance Variables
------------------

Instance variables for Money object:

================  =========================== ====================================================================
 Name              Type                        Description
================  =========================== ====================================================================
 amount            int                         This represents the currency value of the money object.
                                               Each Money object will be initialized with a random amount value
                                               prior to being dropped
                                               on the map. This value can range from 25 to 50.
================  =========================== ====================================================================

Picking up Money
------------------

In order to pick up money, your shooter object must be standing on top of it. You can then
use this command to let the game know you would like to interact with this object.

    **Note: Each player can only perform up to 1 action per turn.**

.. code-block:: python

    actions.set_action(ActionType.interact)





Checking how much Money you Have
----------------------------------

During the game, you'll probably want to keep track of
how much money you've been saving. To do so, you may enter the
following command:

.. code-block:: python

    shooter.money

This will return the money amount as an int value.
