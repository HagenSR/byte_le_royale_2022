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
    shooter = 4
    map_object = 5
    item = 6
    gun = 7

class DamagingType:
    none = 0
    bullet = 1
    grenade = 2  

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
