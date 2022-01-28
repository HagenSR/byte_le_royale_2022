======================
Reload Controller
======================

Lore
------

It seems to be an oversight to make a weapon which needs constant maintenance of it's ammunition supply. This is even more confusing as each AI competitor carries 
an infinite supply of ammo on it's person. Why wouldn't one AI simply make a weapon which can spam lethal retribution towards it's competitors? 
Well, you might not find out if you don't reload soon!

Important Notes
-----------------

Reloading will reset your ammunition to the magazine size of the given weapon and level.


Example
------------

.. code-block:: python

    actions.set_action(ActionType.reload)

will reload your currently equipped gun. Note that you have infinite ammo.