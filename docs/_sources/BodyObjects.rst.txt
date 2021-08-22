============
Body Objects
============

Body objects occupy the body attribute in the truck object. You can only have one Body object at a time. Aditionally the body object also holds the 
current_gas attribute, which is how much gas remains in your tank, and the max_gas attribute, which defaults to 1.

The Tank Object
###############

The Tank object increases the max_gas attribute. Gas levels are stored as percents, IE level 1 holds 50% more gas than level 0.
Not having the Tank object leaves your truck with a level 0 tank.

The levels are below

=====  ================== =====
Level  Max_Gas_multiplier Cost
=====  ================== =====
0      1                   10
1      1.5                 300
2      2                   900
3      4                   2000
=====  ================== =====

The Sentry Gun Object
#####################

The sentry gun object solves the rockslide event. It will reduce your damage and time penalties 
according to the to the below table 

=====  ================== ======
Level    Negation          Cost
=====  ================== ======
0       0.1                5400
1       0.2                10800
2       0.35               16200
3       0.5                21600
=====  ================== ======

The headlights Object
#####################

The headlights object negates the animal_in_the_road event. Below are the negations

=====  ================== ======
Level    Negation          Cost
=====  ================== ======
0       0.1                5400
1       0.2                10800
2       0.35               16200
3       0.5                21600
=====  ================== ======