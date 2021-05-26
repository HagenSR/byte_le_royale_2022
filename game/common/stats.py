

class GameStats:
    game_board_width = 500
    game_board_height = 500
    
    default_wall_health = 50

    player_stats = {
        'starting_health': 10,
        'starting_coordinates': [{'x': 450, 'y': 450}, {'x': 50, 'y': 50}],
        'hitbox': {'width': 10, 'height': 10}
    }
