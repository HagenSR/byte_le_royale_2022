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
    map_object = 4
    damaging_object = 5
    moving_object = 6
    grenade = 7
    shooter = 8
    item = 9
    gun = 10
    wall = 11
    hitbox = 12
    door = 13
    upgrade = 14
    consumable = 15
    

class Upgrades:
    none = 0
    gun_upgrades = 1
    movement_upgrades = 2
    sight_upgrades = 3
    
    
class DamagingType:
    none = 0
    #note that bullet object has not been added yet
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


class Consumables:
    none = 0
    speed_boost = 1
    health_pack = 2
    armor_pack = 3