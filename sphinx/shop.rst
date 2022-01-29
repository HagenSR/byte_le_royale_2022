==========
Shop
==========

Lore
----------------------

In this era, Amazon (ABSOLUTELY NO RELATION TO THE COLLECTION OF TREES IN BRAZIL) controls everything. 
They feed off the capitalism produced by the animatronic warfare.
In order to truly maximize their profits, they introduced their own air-drop delivery system for animatronics
to purchase fun consumables and prolong their suffering even more! Use your hard earned cash so that the funny delivery people
can airdrop your items Hunger Games style!


Basic Info
----------------------

The shop is where you can use money that you have picked up to purchase one-use items.
Once the items are purchased, they will be placed in one of your shooter object's consumables inventory slot.
**NOTE: Items cannot be purchased if the shooter's inventory for consumables is full.**

Shop Contents
------------------

(Description for each consumable is located in the consumables doc)

============   ============
 Item            Cost
============   ============
 speed boost   20
 health pack   25
 shield        30
 radar         40
 grenade       55
============   ============

Example Code
-------------

 **NOTE: Make sure you select what item you want to buy prior to buying from the shop**

.. code-block:: python

    actions.select_item_to_buy(Consumables.health_pack)
    actions.set_action(ActionType.shop)

