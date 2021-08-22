=============
Taking Action
=============

A critical part of building your bot is taking actions. The actions you can take are listed below.
Only one action can be set per turn. All actions are set by calling

.. code-block:: python

    actions.set_action(ActionType.enum, {option})


Selecting a contract
####################

A list of contracts will be generated every turn. These contracts can be viewed in truck.contract_list
Once you have chosen a contract, pass the select contract enum and the index of the contract which you
wish to select. 

EX:

.. code-block:: python

    actions.set_action(ActionType.select_contract, 0)

Will set your contract to the contract at index 0

Moving
######

Moving requires selecting a road. The list of roads you can select is in truck.current_node.roads. 
Simply pass the road you wish to travel to by passing the index of the road you wish to take. Each
road will lead to the same node.

EX:

.. code-block:: python

    actions.set_action(ActionType.select_route, 0)

Will take your road at index 0


Buying Gas
##########

You can buy gas at every node. Gas prices vary from node to node. There are no arguments passed to the 
buy gas method, it will either fill up your tank or buy the most gas you can afford.

EX:

.. code-block:: python

    actions.set_action(ActionType.buy_gas)

Will fill your tank (or buy the most you can afford


Repairing
##########

Throughout the game your truck will take damage. Similar to buying gas, Repair prices will fluctuate from 
node to node. No arguments are required, and the truck will either fully repair or repair the most you can 
afford.

EX:

.. code-block:: python

    actions.set_action(ActionType.repair)

Will fill your tank (or buy the most you can afford)

Upgrading
#########

Upgrades can negate damage and time penalties from events. There are three upgrade slots (body, addons, and tires) 
which each have three different upgrade types. If you don't have enough money, the upgrade will be ignored. Switching 
from one object to another will result in a complete loss of the former upgrade.

EX:

.. code-block:: python

    actions.set_action(ActionType.upgrade, Objectype.policeScanner)

Will upgrade or switch your add on object to policeScanner

Choosing a speed
################

You can set your trucks speed to an integer value between 1 and 80 MPH. Going faster will allow you to complete more
contracts, but will also increase the probability of events happening. Your speed also affects your miles per gallon 
efficiency.

EX:

.. code-block:: python

    actions.set_action(ActionType.choose_speed, 66)

Will set your trucks speed to 66 mph