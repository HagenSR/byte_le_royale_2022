==========
Gun
==========

The gun is an archaic weapon that propels small bits of metal by explosions. Why do our alien overlords choose to use these weapons against robots? Because
their military industrial complex was geared towards defeating humans, and then the gun manufacturers used lobbying to outlaw more advanced forms of weaponry
so they could keep reaping those sweet profits. Anyway, the gun object has the following properties.

Instance Variables
---------------------

Instance variables for the Gun object

================  =========================== ===================
 Name              Type                        Description
================  =========================== ===================
 gun_type           GunType enums               An enum that describes what type of gun this is
 level              number                      The level of the gun
 damage             number                      How much damage the gun does per hit
 fire_rate          number                      If greater than zero, how many bullets are shot at the same time
 range              number                      How far the gun can shoot, in game board units
 mag_size           number                      How many shots you can make before needing to reload
 mag_ammo           number                      How many bullets are currently loaded in the magazine
 __str__            string                      returns a string describing the gun
================  =========================== ===================

Gun type enum
---------------

The following are the enums described above

================  =========================== 
 Gun Type              number            
================  =========================== 
  None                0
  handgun             1
  assault_rifle       2
  shotgun             3
  sniper              4
================  =========================== 

Gun stats
----------

Below are the stats for each gun type, for each level

level 1
=========

================  ========== =========== =========== =========== 
 Gun_              damage     fire rate   range        mag size   
================  ========== =========== =========== =========== 
 handgun            25          n/a           30         5
 assault_rifle      15          3             50         12
 shotgun            10          4             10         1
 sniper             50          n/a           100        1
================  ========== =========== =========== ===========  

level 2
=========

================  ========== =========== =========== =========== 
 Gun_              damage     fire rate   range        mag size   
================  ========== =========== =========== =========== 
 handgun            40          n/a           35         7
 assault_rifle      15          5             60         20
 shotgun            10          6             20         3
 sniper             80          n/a           200        2
================  ========== =========== =========== ===========  


level 3
=========

================  ========== =========== =========== =========== 
 Gun_              damage     fire rate   range        mag size   
================  ========== =========== =========== =========== 
 handgun            60          n/a           50         11
 assault_rifle      20          5             60         25
 shotgun            20          8             30         5
 sniper             100         n/a           300        2
================  ========== =========== =========== =========== 