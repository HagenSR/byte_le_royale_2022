from game.common.enums import *

class GameStats:
    game_board_width = 500
    game_board_height = 500

    player_stats = {
        'starting_health': 10,
        'starting_coordinates': [{'x': 450, 'y': 450}, {'x': 50, 'y': 50}],
        'hitbox': {'width': 10, 'height': 10}
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
