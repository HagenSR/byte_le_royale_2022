from enum import Enum

class DebugLevel(Enum):
    none = 0
    client = 1
    controller = 2
    engine = 3


class ObjectType(Enum):
    none = 0
    action = 1
    player = 2
    game_board = 3
    map_object = 4
    damaging_object = 5
    moving_object = 6
    grenade = 7
    ray = 8
    bullet = 9
    shooter = 10
    item = 11
    gun = 12
    wall = 13
    hitbox = 14
    door = 15
    upgrade = 16
    consumable = 17
    money = 18


class ActionType(Enum):
    none = 0
    move = 1
    shoot = 2
    pickup = 3
    reload = 4
    shop = 5
    use_item = 6


class Upgrades(Enum):
    none = 0
    gun_upgrades = 1
    movement_upgrades = 2
    sight_upgrades = 3


class DamagingType(Enum):
    none = 0
    bullet = 1
    grenade = 2


class GunType(Enum):
    none = 0
    handgun = 1
    assault_rifle = 2
    shotgun = 3
    sniper = 4


class GunLevel(Enum):
    level_zero = 0
    level_one = 1
    level_two = 2
    level_three = 3


class ShotPattern(Enum):
    none = 0
    single = 1
    multi = 2
    spread = 3


class Consumables(Enum):
    none = 0
    speed_boost = 1
    health_pack = 2
    armor_pack = 3
