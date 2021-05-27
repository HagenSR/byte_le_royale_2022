from game.common.enums import *

class GameStats:
    game_board_width = 500
    game_board_height = 500

    player_stats = {
        'starting_health': 10,
        'starting_coordinates': [{'x': 450, 'y': 450}, {'x': 50, 'y': 50}],
        'hitbox': {'width': 10, 'height': 10}
    }

# Placeholder stats
    gun_stats = {
        GunType.none: {'damage': 0, 'fire_rate': 0,
            'cooldown': {'max': 0, 'rate': 0}, 'range': 0, 'mag_size': 0,
            'reload_speed': 0},
        GunType.handgun: {'damage': 1, 'fire_rate': 2,
            'cooldown': {'max': 8, 'rate': 2}, 'range': 30, 'mag_size': 13,
            'reload_speed': 3},
        GunType.assault_rifle: {'damage': 1, 'fire_rate': 5,
            'cooldown': {'max': 15, 'rate': 5}, 'range': 50, 'mag_size': 30,
            'reload_speed': 6},
        GunType.shotgun: {'damage': 8, 'fire_rate': 1, 'cooldown': {'max': 1,
            'rate': 1}, 'range': 10, 'mag_size': 2, 'reload_speed': 8},
        GunType.sniper: {'damage': 9, 'fire_rate': 1, 'range': 100,
            'mag_size': 1, 'reload_speed': 8}
    }
