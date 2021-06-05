from game.common.enums import *

class GameStats:
    game_board_width = 500
    game_board_height = 500
    
    default_wall_health = 50

    player_stats = {
        'starting_health': 10,
        'starting_money': 10,
        'starting_coordinates': [{'x': 450, 'y': 450}, {'x': 50, 'y': 50}],
        'hitbox': {'width': 10, 'height': 10},
        'view_radius': 10,
        'move_speed': 10,
    }
    
    moving_object_stats = {
        # max speed value is arbitrary at this time and will most likely be changed
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
   
# Placeholder stats, stats may be created for all gun levels
    gun_stats = {
        GunType.none: {'pattern': ShotPattern.none, 'damage': 0,
            'fire_rate': 0, 'range': 0, 'mag_size': 0, 'reload_speed': 0,
            'cooldown': {'max': 0, 'rate': 0}, 'level_mod': 1},
        GunType.handgun: {'pattern': ShotPattern.single, 'damage': 1,
            'fire_rate': 2, 'range': 30, 'mag_size': 13, 'reload_speed': 3,
            'cooldown': {'max': 8, 'rate': 2}, 'level_mod': 1.25},
        GunType.assault_rifle: {'pattern': ShotPattern.multi, 'damage': 1,
            'fire_rate': 5, 'range': 50, 'mag_size': 30, 'reload_speed': 6,
            'cooldown': {'max': 15, 'rate': 5}, 'level_mod': 1.25},
        GunType.shotgun: {'pattern': ShotPattern.spread, 'damage': 8,
            'fire_rate': 1, 'range': 10, 'mag_size': 2, 'reload_speed': 8,
            'cooldown': {'max': 1, 'rate': 1}, 'level_mod': 1.25},
        GunType.sniper: {'pattern': ShotPattern.single, 'damage': 9,
            'fire_rate': 1, 'range': 100, 'mag_size': 1, 'reload_speed': 8,
            'cooldown': {'max': 1, 'rate': 1}, 'level_mod': 1.25}
    }

    grenade_stats = {
        'min_fuse_time': 10,
        'max_fuse_time': 50
    }
