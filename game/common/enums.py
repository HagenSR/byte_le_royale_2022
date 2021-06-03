class DebugLevel:
    none = 0
    client = 1
    controller = 2
    engine = 3


class ObjectType:
    none = 0
    action = 1
    player = 2
    game_board = 3
<<<<<<< HEAD
    shooter = 4
    map_object = 5
    item = 6
    gun = 7

class DamagingType:
    none = 0
    bullet = 1
    grenade = 2  
=======
    map_object = 4
    damaging_object = 5
    moving_object = 6
    shooter = 7
    item = 8
    gun = 9
    wall = 10
    
>>>>>>> 56777947cd75f560937fd2892c5f9c0a2502d6b9

class GunType:
    none = 0
    handgun = 1
    assault_rifle = 2
    shotgun = 3
    sniper = 4

    
class GunLevel:
    level_zero = 0
    level_one = 1
    level_two = 2
    level_three = 3

    
class ShotPattern:
    none = 0
    single = 1
    multi = 2
    spread = 3
