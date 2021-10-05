import random
from game.common.game_board import GameBoard
from game.common.stats import GameStats
from game.common.hitbox import Hitbox
from game.common.items.consumable import Consumable
from game.common.items.upgrade import Upgrade
from game.common.items.gun import Gun
from game.common.items.money import Money
from game.common.enums import *
from game.common.items.item import Item


def place_items(
        game_board,
        loot_wave_num,
        number_items,
        consumable_count,
        upgrade_count,
        gun_count,
        money_count):
    item_list = []
    half_width = game_board.circle_radius
    half_height = game_board.circle_radius
    for index in range(number_items):
        # Value is pined between 0 and game board height/width. Values are
        # (somewhat) normally distributed around the center
        potential_x = max(
            min(random.gauss(half_width, half_width * .3), game_board.circle_radius - 1), 1)
        potential_y = max(min(random.gauss(
            half_height, half_height * .3), game_board.circle_radius - 1), 1)
        # Determine if there is an object in the way
        dummy_hitbox = Hitbox(5, 5, (potential_x, potential_y))
        # if (x,y) collided with an already existing object too many times, the
        # object will not spawn
        object_collided = 0
        while game_board.partition.find_object_hitbox(dummy_hitbox):
            object_collided += 1
            potential_x = max(min(random.gauss(
                half_width, half_width * .005), game_board.circle_radius - 1), 1)
            potential_y = max(min(random.gauss(
                half_width, half_width * .005), game_board.circle_radius - 1), 1)
            dummy_hitbox = Hitbox(5, 5, (potential_x, potential_y))
            # if item spawns outside kill boundary or there is not enough room,
            # dont spawn it
            if (potential_x - GameStats.game_board_width / 2)**2 + (potential_y - \
                GameStats.game_board_height / 2)**2 > game_board.circle_radius**2 or object_collided > 10:
                break
        if (potential_x - GameStats.game_board_width / 2)**2 + (potential_y - \
            GameStats.game_board_height / 2)**2 > game_board.circle_radius**2 or object_collided > 10:
            continue
        item, consumable_count, upgrade_count, gun_count, money_count = pick_item(
            potential_x, potential_y, consumable_count, upgrade_count, gun_count, money_count, loot_wave_num=loot_wave_num)
        if item is not None:
            item_list.append(item)
    return item_list, consumable_count, upgrade_count, gun_count, money_count


def pick_item(
        xPos,
        yPos,
        consumable_count,
        upgrade_count,
        gun_count,
        money_count,
        loot_wave_num):
    type = random.choice([ObjectType.consumable,
                          ObjectType.consumable,
                          ObjectType.upgrade,
                          ObjectType.gun,
                          ObjectType.money])
    rtnItem = None
    if has_reached_item_cap(
            type,
            consumable_count,
            upgrade_count,
            gun_count,
            money_count):
        return rtnItem
    if type is ObjectType.consumable:
        consumable_count += 1
        conType = random.choice([type_con for type_con in Consumables])
        rtnItem = Consumable(Hitbox(5, 5, (xPos, yPos)), 1, conType)
    elif type is ObjectType.upgrade:
        upgrade_count += 1
        upType = random.choice([up_type for up_type in Upgrades])
        rtnItem = Upgrade(Hitbox(5, 5, (xPos, yPos)), 5, upType)
    elif type is ObjectType.gun:
        gun_count += 1
        gunType = random.choice([gun_type for gun_type in GunType])
        rtnItem = Gun(gunType, loot_wave_num, Hitbox(5, 5, (xPos, yPos)))
    elif type is ObjectType.money:
        money_count += 1
        rtnItem = Money(Hitbox(5, 5, (xPos, yPos)), health=2022)
    return rtnItem, consumable_count, upgrade_count, gun_count, money_count


def has_reached_item_cap(
        item,
        consumable_count,
        upgrade_count,
        gun_count,
        money_count):
    if item == ObjectType.consumable:
        if consumable_count >= GameStats.consumable_cap:
            return True
    elif item == ObjectType.upgrade:
        if upgrade_count >= GameStats.upgrade_cap:
            return True
    elif item == ObjectType.gun:
        if gun_count >= GameStats.gun_cap:
            return True
    elif item == ObjectType.money:
        if money_count >= GameStats.money_cap:
            return True
    return False
