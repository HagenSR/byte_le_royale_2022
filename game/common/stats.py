from game.common.enums import *

class GameStats:
    game_board_width = 500
    game_board_height = 500

    player_stats = {
        'starting_health': 10,
        'starting_coordinates': [[450, 450], [50, 50]],
        'hitbox': {'width': 10, 'height': 10}
    }
