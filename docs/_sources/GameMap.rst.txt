===================
Game Map
===================

The game map is a linked list of nodes. Traveling to the next node requires selecting a valid road from your current node.
please note that whichever road is taken you end up at the same node.

Instance variables
##################

================  =========================== ===================
Name               Type                        Description
================  =========================== ===================
head               :doc:`./Node`                The node the contract starts at
current_node       :doc:`./Node`                The node you are currently at
================  =========================== ===================

Methods
#######

get_next_node() -> get the next node in the game map. also sets your current node to the get_next_node
length() -> returns the number of nodes in the map. Also sets current node to end
reset_current() -> resets your current node to head
