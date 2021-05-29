

class GameStats:
    game_board_width = 500
    game_board_height = 500

    player_stats = {
        'starting_health': 10,
        'starting_coordinates': [{'x': 450, 'y': 450}, {'x': 50, 'y': 50}],
        'hitbox': {'width': 10, 'height': 10}
    }

    moving_object_stats = {
        # max speed value is arbitrary at this time and will most likely be changed
        'max_speed': 500
    }

    damaging_object_stats = {
        # This is assuming the player is at the very edge of board and the object 
        # only stops once it hits an object. 
        'max_range': 500
        
        # This determines the max damage an object instance to do, value 
        # is arbitrary for now and will be changed when necessary 
        'max_damage': 100
    }
   
