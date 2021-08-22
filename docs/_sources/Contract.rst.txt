===================
Contract
===================

Contracts come in easy, medium and hard versions, which impact their rewards, renown, length and completabiltiy. 
Easy contracts give less renown and reward, but are also shorter. The opposite is true with hard contracts

Instance variables
##################

Below are the listed instance variables for the contract object

================  =========================== ===================
Name               Type                        Description
================  =========================== ===================
name               string                      The name of the current node you are on
region             Region.Enum                 The type of region the contract will be in. Impacts events
game_map           :doc:`./GameMap`            The map you need to traverse to complete the contract
money_reward       int                         The amount of money you will recieve from completing this contract
renown_reward      int                         The amount of renown you will recieve from completing this contract
deadline           int                         The time you must complete the contract by. Decrements Automatically
================  =========================== ===================

