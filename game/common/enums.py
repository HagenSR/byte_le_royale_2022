from enum import Enum


class DebugLevel(int, Enum):
    none = 0
    client = 1
    controller = 2
    engine = 3


class ObjectType(int, Enum):
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
    teleporter = 19


class ActionType(int, Enum):
    none = 0
    move = 1
    shoot = 2
    interact = 3
    reload = 4
    shop = 5
    pickup = 6
    use = 7
    use_teleporter = 8


class Upgrades(int, Enum):
    none = 0
    armor = 1
    movement_boots = 2
    backpack = 3


class DamagingType(int, Enum):
    none = 0
    bullet = 1
    grenade = 2


class GunType(int, Enum):
    none = 0
    handgun = 1
    assault_rifle = 2
    shotgun = 3
    sniper = 4


class GunLevel(int, Enum):
    level_zero = 0
    level_one = 1
    level_two = 2
    level_three = 3


class ShotPattern(int, Enum):
    none = 0
    single = 1
    multi = 2
    spread = 3


class Consumables(int, Enum):
    none = 0
    health_pack = 1
    shield = 2
    speed_boost = 3
    radar = 4
    grenade = 5
