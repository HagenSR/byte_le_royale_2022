from game.common.moving.shooter import Shooter
from game.common.wall import Wall
from game.common.door import Door
from game.utils.ray_utils import get_ray_collision
from game.controllers.controller import Controller
from game.common.enums import *


class ShootController(Controller):
    
    def shoot_gun(gun, client, game_board):
        if(client.action.chosen_action is ActionType.shoot):
            collision_object = get_ray_collision(client, game_board, gun)
            if(collision_object == None):
                #no collision
                return
            elif(isinstance(collision_object, Shooter)):
                collision_object.health(collision_object.health - gun.damage)
                if(collision_object.health <= 0):
                    #game over
                    game_board.player_list.remove(collision_object)
            elif(isinstance(collision_object, Wall) and collision_object.collidable is True):
                    collision_object.health(collision_object.health - gun.damage)
                    if(collision_object.health <= 0):
                        game_board.wall_list.remove(collision_object)
            elif(isinstance(collision_object, Door) and collision_object.collidable is True):
                collision_object.health(collision_object.health - gun.damage)
                if(collision_object.health <= 0):
                    game_board.door_list.remove(collision_object)
