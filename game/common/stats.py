from game.common.enums import *
import math


class GameStats:
    game_board_width = 500
    game_board_height = 500

    # The radius that the kill circle will shrink every tick
    circle_shrink_distance = 1
    # Damage circle does each tick
    circle_damage = 1
    # Number of turns before circle encroaches on game map
    circle_delay = 100 * circle_shrink_distance

    # The "margin" inbetween every building plot in game map. Used so players
    # can always navigate between buildings
    corridor_width_height = 20

    default_wall_health = 18

    default_door_health = 18

    player_stats = {
        'starting_health': 10,
        'starting_money': 10,
        'hitbox': [[10, 10, 45, 45], [10, 10, 445, 445]],
        'field_of_view': 90,
        'view_distance': 100,
        'max_distance_per_turn': 50
    }

    # format: 'slot_type': { num_of_slots, slot_obj_type }
    inventory_stats = {
        'guns': {
            'slots': 2
        },
        'upgrades': {
            'slots': 3
        },
        'consumables': {
            'slots': 4
        },
    }

    consumable_stats = {
        "health_pack_heal_amount": 50,
        "speed_increase_percent": .2,
        "radar_range_increase_percent": .2,
    }

    # stats for money located on the gameboard
    min_money_amount = 25
    max_money_amount = 500

    moving_object_stats = {
        # max speed value is arbitrary at this time and will most likely be
        # changed
        'max_speed': 500
    }

    damaging_object_stats = {
        # This is assuming the player is at the very edge of board and the object
        # only stops once it hits an object.
        'max_range': 500,

        # This determines the max damage an object instance to do, value
        # is arbitrary for now and will be changed when necessary
        'max_damage': 100
    }

    max_hitbox = {
        'width': 100,
        'height': 100,
    }

    shop_stats = {
        Consumables.speed: {
            'cost': 20
        },
        Consumables.health_pack: {
            'cost': 25
        },
        Consumables.shield: {
            'cost': 30
        }

    }

    # Placeholder stats, stats may be created for all gun levels
    gun_stats = {
        GunType.none: {
            'pattern': ShotPattern.none,
            'damage': 0,
            'fire_rate': 0,
            'range': 0,
            'mag_size': 0,
            'reload_speed': 0,
            'cooldown': {
                'max': 0,
                'rate': 0},
            'level_mod': 1},
        GunType.handgun: {
            'pattern': ShotPattern.single,
            'damage': 1,
            'fire_rate': 2,
            'range': 30,
            'mag_size': 13,
            'reload_speed': 3,
            'cooldown': {
                'max': 8,
                'rate': 2},
            'level_mod': 1.25},
        GunType.assault_rifle: {
            'pattern': ShotPattern.multi,
            'damage': 1,
            'fire_rate': 5,
            'range': 50,
            'mag_size': 30,
            'reload_speed': 6,
            'cooldown': {
                'max': 15,
                'rate': 5},
            'level_mod': 1.25},
        GunType.shotgun: {
            'pattern': ShotPattern.spread,
            'damage': 8,
            'fire_rate': 1,
            'range': 10,
            'mag_size': 2,
            'reload_speed': 8,
            'cooldown': {
                'max': 1,
                'rate': 1},
            'level_mod': 1.25},
        GunType.sniper: {
            'pattern': ShotPattern.single,
            'damage': 9,
            'fire_rate': 1,
            'range': 100,
            'mag_size': 1,
            'reload_speed': 8,
            'cooldown': {
                'max': 1,
                'rate': 1},
            'level_mod': 1.25}}

    grenade_stats = {
        'range': 40,
        'min_fuse_time': 10,
        'max_fuse_time': 50
    }

    shot_pattern_multi_pellet_count = 9
    shot_pattern_multi_arc = math.pi / 10

    door_opening_speed = 1

    num_loot_waves = 4
    # self.ticks_between_waves and self.tick (var in loot gen controller) must
    # be equal to each other
    ticks_between_waves = 200

    gun_cap = 50
    consumable_cap = 30
    upgrade_cap = 20
    money_cap = 50
