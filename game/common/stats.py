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
        Consumables.speed_boost: {
            'cost': 20,
            'quantity': 5
        },
        Consumables.health_pack: {
            'cost': 25,
            'quantity': 5
        },
        Consumables.shield: {
            'cost': 30,
            'quantity': 5
        },
        Consumables.Radar: {
             'cost': 40
        },
        Consumables.Grenade: {
            'cost': 55
        }
    }

    # Placeholder stats, stats may be created for all gun levels
    gun_stats = {
        0: {
            GunType.none: {
                'pattern': ShotPattern.none,
                'damage': 0,
                'fire_rate': 0,
                'range': 0,
                'mag_size': 0,
            },
            GunType.handgun: {
                'pattern': ShotPattern.single,
                'damage': 0,
                'fire_rate': 0,
                'range': 0,
                'mag_size': 0,
            },
            GunType.assault_rifle: {
                'pattern': ShotPattern.multi,
                'damage': 0,
                'fire_rate': 0,
                'range': 0,
                'mag_size': 0,
            },
            GunType.shotgun: {
                'pattern': ShotPattern.spread,
                'damage': 0,
                'fire_rate': 0,
                'range': 0,
                'mag_size': 0,
            },
            GunType.sniper: {
                'pattern': ShotPattern.single,
                'damage': 0,
                'fire_rate': 0,
                'range': 0,
                'mag_size': 0,
            }
        },
        1: {
            GunType.none: {
                'pattern': ShotPattern.none,
                'damage': 0,
                'fire_rate': 0,
                'range': 0,
                'mag_size': 0,
            },
            GunType.handgun: {
                'pattern': ShotPattern.single,
                'damage': 25,
                'fire_rate': 0,
                'range': 30,
                'mag_size': 5,
            },
            GunType.assault_rifle: {
                'pattern': ShotPattern.multi,
                'damage': 15,
                'fire_rate': 3,
                'range': 50,
                'mag_size': 12,
            },
            GunType.shotgun: {
                'pattern': ShotPattern.spread,
                'damage': 10,
                'fire_rate': 4,
                'range': 10,
                'mag_size': 2,
            },
            GunType.sniper: {
                'pattern': ShotPattern.single,
                'damage': 50,
                'fire_rate': 0,
                'range': 100,
                'mag_size': 1,
            }
        },
        2: {
            GunType.none: {
                'pattern': ShotPattern.none,
                'damage': 0,
                'fire_rate': 0,
                'range': 0,
                'mag_size': 0,
            },
            GunType.handgun: {
                'pattern': ShotPattern.single,
                'damage': 40,
                'fire_rate': 0,
                'range': 35,
                'mag_size': 7,
            },
            GunType.assault_rifle: {
                'pattern': ShotPattern.multi,
                'damage': 15,
                'fire_rate': 5,
                'range': 60,
                'mag_size': 20,
            },
            GunType.shotgun: {
                'pattern': ShotPattern.spread,
                'damage': 10,
                'fire_rate': 6,
                'range': 20,
                'mag_size': 3,
            },
            GunType.sniper: {
                'pattern': ShotPattern.single,
                'damage': 80,
                'fire_rate': 0,
                'range': 200,
                'mag_size': 2,
            }
        },
        3: {
            GunType.none: {
                'pattern': ShotPattern.none,
                'damage': 0,
                'fire_rate': 0,
                'range': 0,
                'mag_size': 0,
            },
            GunType.handgun: {
                'pattern': ShotPattern.single,
                'damage': 60,
                'fire_rate': 0,
                'range': 50,
                'mag_size': 11,
            },
            GunType.assault_rifle: {
                'pattern': ShotPattern.multi,
                'damage': 20,
                'fire_rate': 5,
                'range': 60,
                'mag_size': 25,
            },
            GunType.shotgun: {
                'pattern': ShotPattern.spread,
                'damage': 20,
                'fire_rate': 8,
                'range': 30,
                'mag_size': 5
            },
            GunType.sniper: {
                'pattern': ShotPattern.single,
                'damage': 100,
                'fire_rate': 0,
                'range': 300,
                'mag_size': 2
            }
        }
    }

    grenade_stats = {
        'range': 40,
        'min_fuse_time': 10,
        'max_fuse_time': 50
    }

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

    # this distance goes from middle of player hitbox to coord within door hitbox
    max_allowed_dist_from_door = 10
