============
Using Items
============

The use controller controls using consumable items.

By calling the action 

.. code-block:: python

    actions.select_item_to_use(obj)

you can select what item you want to use. Make sure that obj is the consumable object from your inventory.

Speed boost and radar will last for 10 turns each and cannot be applied again until after those 10 turns.

Shield is set as a boolean in the shooter object, and will go away after one shot hits you.

Health pack will increase your shooter health.