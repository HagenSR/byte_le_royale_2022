import random
from game.common.stats import GameStats
from game.common.hitbox import Hitbox
from game.common.items.consumable import Consumable
from game.common.items.upgrade import Upgrade
from game.common.items.gun import Gun
from game.common.items.money import Money
from game.common.enums import *
from game.common.items.item import Item


def placeItems(game_board, loot_wave_num, kill_boundary_radius, number_items):
    item_list = []
    half_width = kill_boundary_radius
    half_height = kill_boundary_radius
    for index in range(number_items):
        # Value is pined between 0 and game board height/width. Values are (somewhat) normally distributed around the center
        potential_x = max(min(random.gauss(half_width, half_width * .3), kill_boundary_radius - 1), 1)
        potential_y = max(min(random.gauss(half_height, half_height * .3), kill_boundary_radius - 1), 1)
        item = pickItem(potential_x, potential_y, loot_wave_num = loot_wave_num)
        # Determine if there is an object in the way
        while game_board.partition.find_object_hitbox(item):
            potential_x = random.gauss(half_width, half_width * .005)
            potential_y = random.gauss(half_height, half_height * .005)
        if item is not None:
            item_list.append(item)
    return item_list


def pickItem(xPos, yPos, loot_wave_num):
    type = random.choice([ObjectType.consumable, ObjectType.consumable, ObjectType.upgrade, ObjectType.gun, ObjectType.money])
    rtnItem = None
    if hasReachedItemCap(type):
        return rtnItem
    if type == ObjectType.consumable:
        conType = random.choice([ type_con for type_con in Consumables.__dir__() if isinstance(type_con, int) ])
        rtnItem = Consumable(Hitbox(5,5, (xPos, yPos)), 1, conType)
    elif type == ObjectType.upgrade:
        upType = random.choice([ up_type for up_type in Upgrades.__dir__() if isinstance(up_type, int) ])
        rtnItem = Upgrade(Hitbox(5,5 (xPos, yPos)), 5, 1, upType)
    elif type == ObjectType.gun:
        gunType = random.choice([ gun_type for gun_type in GunType.__dir__() if isinstance(gun_type, int)])
        rtnItem = Gun(gunType, loot_wave_num, Hitbox(5, 5, (xPos, yPos)))
    elif type == ObjectType.money:
        rtnItem = Money(Hitbox(5, 5, (xPos, yPos)))
    return rtnItem


def hasReachedItemCap(item):
    if item == ObjectType.consumable:
        if GameStats.consumable_count >= GameStats.consumable_cap:
            return True
    elif item == ObjectType.upgrade:
        if GameStats.upgrade_count >= GameStats.upgrade_cap:
            return True
    elif item == ObjectType.gun:
        if GameStats.gun_count >= GameStats.gun_cap:
            return True
    elif item == ObjectType.money:
        if GameStats.money_count >= GameStats.money_cap:
            return True
    return False