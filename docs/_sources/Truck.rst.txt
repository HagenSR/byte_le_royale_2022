================
The Truck Object
================

The truck object holds everything related to the game. It should be noted that contract_list holds three
contracts with varying dificulty, with index 0 being the easy contract and index 2 holding the hard contract.

Instance variables
##################

================  =========================== ===================
Name               Type                        Description
================  =========================== ===================
current_node       :doc:`./Node`               The current node you are on
contract_list      :doc:`./Contract` []         A list of contracts you can pick from
active_contract    :doc:`./Contract` or None   The current contract you are working to complete
body               :doc:`./BodyObjects`        Your current body Object. Default is a BaseBodyObject 
addons             :doc:`./AddonObjects`       Your current addon object. Default is a BaseUpgradeObject
tires              int                         The TireEnum you are currently equiped with. Default is tire_normal
speed              int                         The speed your truck is currently traveling at
renown             int                         Your score. The game is won by having the most renown
================  =========================== ===================

Please note that the BaseBodyObject gives you the default max_gas attribute. You can't switch back to the base objects once you upgrade