================
Road
================

Roads are paths that connect :doc:`./Node` s. 

Instance variables
##################

================  ================== ===================
Name               Type                Description
================  ================== ===================
road_name          String             The name of the road
road_type          RoadType.Enum      The type of the road. Affects event probabilties
length             decimal            The length of the road
================  ================== ===================

Road Type Modifiers
###################

There are 6 Roadtypes, mountain_road, forest_road, tundra_road, city_road, highway, and interstate.

**Length Modifiers**

road types modify the potential lengths of a road. Below are the roads listed in order of the magnitude
of their modifier, with position 0 being the smallest. Road type enumerations can be accessed by RoadType.<RoadType>

========== ==============
Position      Road Type
========== ==============
 0          montain_road
 1          forest_road
 2          tundra_road
 3          city_road
 4          highway
 5          interstate
========== ==============

**Potential Events**

The potential events that can happen on a given road type are listed below. More on events can be seen at :doc:`./Events` 

============= ==============
Road          Events
============= ==============
montain_road  rock_slide, animal_in_road, icy_road, police, none
forest_road   animal_in_road, police, rock_slide, icy_road, None
tundra_road   icy_road, police, rock_slide, none
city_road     bandits, police, traffic, none
highway       police, traffic, none
interstate    traffic, police, none
============= ==============