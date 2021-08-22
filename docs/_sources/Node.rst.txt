================
Node
================

Nodes are stops within each GameMap. Each turn your truck will be at a node. Below 
are the listed instance variables.

================  ================== ===================
Name               Type                Description
================  ================== ===================
city_name          String             The name of the Node you are at
roads              :doc:`./Road` []   A list of roads that you can take to travel to the next node
next_node          node               The next node you will travel to. It will be the same regardless of the road you take
gas_price          decimal            The current price of gas at this node
repair_price       decimal            The current price of repairing at this node
================  ================== ===================