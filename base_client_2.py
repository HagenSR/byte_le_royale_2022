from game.client.user_client import UserClient
from game.common.enums import *

######################################################
# imports for type hints
from game.common.action import Action
from game.common.moving.shooter import Shooter
from game.utils.partition_grid import PartitionGrid
######################################################

from game.utils.player_utils import *


class Client(UserClient):
    # Variables and info you want to save between turns go here
    def __init__(self):
        super().__init__()
        self.prev_location = (0, 0)
        self.topleft = True
        self.checkpoint = 1
        self.shield_bought = False
        self.shield_ready = False
        self.radar_ready = False

    def team_name(self):
        """""
        Allows the team to set a team name.
        :return: Your team name
        """""
        return 'Double D'
    
    
    def better_gun_in_range(self, shooter, guns):
        # Get lists of guns in range
        handguns = [i for i in guns if i.gun_type == 1]
        assault_rifles = [i for i in guns if i.gun_type == 2]
        shotguns = [i for i in guns if i.gun_type == 3]
        snipers = [i for i in guns if i.gun_type == 4 and i.level != 1]

        # Pick up the best gun
        best_gun = shooter.primary_gun
        if len(assault_rifles) != 0:
            for gun in assault_rifles:
                if (best_gun.gun_type == 2) and (best_gun.level < gun.level):
                    best_gun = gun
                elif (best_gun.gun_type == 4) and (best_gun.level <= gun.level):
                    best_gun = gun
        if len(snipers) != 0:
            for gun in snipers:
                if (best_gun.gun_type == 2) and (best_gun.level < gun.level):
                    best_gun = gun
                elif (best_gun.gun_type == 4) and (best_gun.level < gun.level):
                    best_gun = gun   
        if best_gun != shooter.primary_gun:
            return best_gun
        else:
            return None
        
        

    # This is where your AI will decide what to do
    def take_turn(self, turn, actions: Action, game_board, partition_grid: PartitionGrid, shooter: Shooter) -> None:
        """""
        This is where your AI will decide what to do.
        :param partition_grid: This is the representation of the game map divided into partitions
        :param turn:        The current turn of the game.
        :param actions:     This is the actions object that you use to declare your intended actions.
        :param world:       Generic world information
        :param shooter:      This is your in-game character object
        """""

        # This is the list that contains all the objects on the map your player can see
        map_objects = partition_grid.get_all_objects()

        #first check to see what starting position the player is at
        if(turn == 1):
            if(angle_to_point(shooter, (250,250)) - 45 < 100):
                self.topleft = True
            else:
                self.topleft = False
            

        if self.topleft:
            if self.checkpoint == 1:
                # Get the shooter in clear hallway
                if shooter.hitbox.top_left[1] < 150:
                    actions.set_move(90, int(shooter.max_speed))
                elif shooter.hitbox.top_left[1] < 160:
                    actions.set_move(90, 10)
                elif shooter.hitbox.bottom_right[1] > 180:
                    actions.set_move(270, 10)
                else:
                    self.checkpoint = 2

            elif self.checkpoint == 2:
                # Get the shooter in clear hallway
                if shooter.hitbox.top_left[0] < 150:
                    actions.set_move(0, int(shooter.max_speed))
                elif shooter.hitbox.top_left[0] < 160:
                    actions.set_move(0, 10)
                elif shooter.hitbox.bottom_right[0] > 180:
                    actions.set_move(180, 10)
                else:
                    self.checkpoint = 3

            elif self.checkpoint == 3:
                # This is the list that contains all the objects on the map your player can see
                map_objects = partition_grid.get_all_objects()
                shooters = list(filter(lambda obj: obj.object_type == ObjectType.shooter, map_objects))
                guns = list(filter(lambda obj: obj.object_type == ObjectType.gun, map_objects))
                other_gun = self.better_gun_in_range(shooter, guns)
                if shooter.primary_gun.mag_ammo == 0:
                    actions.set_action(ActionType.reload)
                elif len(shooters) > 0 and distance_tuples(shooter.hitbox.middle, shooters[0].hitbox.middle) <= 30:
                    actions.set_shoot(round(angle_to_point(shooter, shooters[0].hitbox.middle)))
                # If there is no opponent, try and find a better weapon
                elif other_gun != None:
                    if check_collision(shooter.hitbox, other_gun.hitbox):
                        actions.set_action(ActionType.interact)
                    else:
                        actions.set_move(angle_to_point(shooter, other_gun.hitbox.middle), min(int(shooter.max_speed), round(distance_tuples(shooter.hitbox.middle, other_gun.hitbox.middle))))
                # If nothing to go to, go towards the middle
                else:
                    actions.set_move(angle_to_point(shooter, game_board.center), min(int(shooter.max_speed), round(distance_tuples(shooter.hitbox.middle, game_board.center))))
                    


        else:
            if self.checkpoint == 1:
                if shooter.hitbox.top_left[1] > 500 - 150:
                    actions.set_move(270, int(shooter.max_speed))
                elif shooter.hitbox.top_left[1] > 500 - 160:
                    actions.set_move(270, 10)
                elif shooter.hitbox.bottom_right[1] < 500 - 180:
                    actions.set_move(90, 10)
                else:
                    self.checkpoint = 2
            elif self.checkpoint == 2:
                # Get the shooter in clear hallway
                if shooter.hitbox.top_left[0] > 500 - 150:
                    actions.set_move(180, int(shooter.max_speed))
                elif shooter.hitbox.top_left[0] > 500 - 160:
                    actions.set_move(180, 10)
                elif shooter.hitbox.bottom_right[0] < 500 - 180:
                    actions.set_move(0, 10)
                else:
                    self.checkpoint = 3
            elif self.checkpoint == 3:
                # This is the list that contains all the objects on the map your player can see
                map_objects = partition_grid.get_all_objects()
                shooters = list(filter(lambda obj: obj.object_type == ObjectType.shooter, map_objects))
                guns = list(filter(lambda obj: obj.object_type == ObjectType.gun, map_objects))
                other_gun = self.better_gun_in_range(shooter, guns)
                if shooter.primary_gun.mag_ammo == 0:
                    actions.set_action(ActionType.reload)
                elif len(shooters) > 0 and distance_tuples(shooter.hitbox.middle, shooters[0].hitbox.middle) <= 30:
                    actions.set_shoot(round(angle_to_point(shooter, shooters[0].hitbox.middle)))
                # If there is no opponent, try and find a better weapon
                elif other_gun != None:
                    if check_collision(shooter.hitbox, other_gun.hitbox):
                        actions.set_action(ActionType.interact)
                    else:
                        actions.set_move(angle_to_point(shooter, other_gun.hitbox.middle), min(int(shooter.max_speed), round(distance_tuples(shooter.hitbox.middle, other_gun.hitbox.middle))))
                # If nothing to go to, go towards the middle
                else:
                    actions.set_move(angle_to_point(shooter, game_board.center), min(int(shooter.max_speed), round(distance_tuples(shooter.hitbox.middle, game_board.center))))