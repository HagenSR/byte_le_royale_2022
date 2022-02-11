from game.client.user_client import UserClient
from game.common.enums import *
import math

######################################################
# imports for type hints
from game.common.action import Action
from game.common.moving.shooter import Shooter
from game.utils.partition_grid import PartitionGrid
######################################################

from game.utils.player_utils import *


class Client(UserClient):
    dict = {"Money": 0.3, "Backpack": 0.1, "Boots": 0.5, "GunLv1": 0.75, "GunLv2": 1, "GunLv3": 1.5, "Teleport": 0,
            "Speed Boost": 0.2, "Health Pack": 0, "Shield": 0.7, "Radar": 0.8, "Grenade": 0.4}
    prev_pos = {"prev1": (0, 0), "prev2": (1, 1), "prev3": (2, 2), "prev4": (3, 3)}
    hitMid = False

    # Variables and info you want to save between turns go here
    def __init__(self):
        super().__init__()
        self.prev_location = (0, 0)

    def team_name(self):
        """""
        Allows the team to set a team name.
        :return: Your team name
        """""
        return '$10 EBay Bot'

    def get_enemy_health(self, enemy):
        return enemy.health

    def get_enemy_primary(self, enemy):
        return enemy.primary_gun

    def get_enemy_armor(self, enemy):
        return enemy.armor

    def check_threat(self, shooter, enemy):
        return shooter.health * (shooter.armor ** -1) - self.get_ememy_health(enemy) * (
                    self.get_enemy_armor(enemy) ** -1) + shooter.primary_gun.damage * max(shooter.primary_gun.fire_rate,
                                                                                          1) - self.get_enemy_primary(
            enemy).damage * max(self.get_enemy_primary(enemy).fire_rate, 1)

    def reload_needed(self, shooter: Shooter):
        try:
            return shooter.primary_gun.mag_ammo <= 1
        except:
            return False

    def attack_mode(self, shooter: Shooter, actions: Action, enemy):
        range = shooter.primary_gun.range
        distance = distance_tuples(shooter.hitbox.middle, enemy.hitbox.middle)
        if distance > range:
            actions.set_move(round(angle_to_point(shooter, enemy.hitbox.middle)), round(min(distance - range,shooter.max_speed)))
        else:
            self.reload_or_shoot(shooter, actions, enemy)
        return

    def reload_or_shoot(self, shooter: Shooter, actions: Action, enemy):

        if self.reload_needed(shooter):
            actions.set_action(ActionType.reload)
        else:
            actions.set_shoot(round(angle_to_point(shooter, enemy.hitbox.middle)))
        return

    # def reload_or_shoot(self, shooter: Shooter, actions: Action, enemy):
    #     d1=0
    #     r1=0
    #     if shooter.primary_gun != None:
    #         r1=shooter.primary_gun.range
    #         d1=min(shooter.primary_gun.mag_ammo * (shooter.primary_gun.fire_rate if shooter.primary_gun.gun_type==3 else 1), shooter.primary_gun.fire_rate)*shooter.primary_gun.damage
    #     actions.cycle_primary()
    #     d2=0
    #     r2=0
    #     if shooter.primary_gun != None:
    #         r2 = shooter.primary_gun.range
    #         d2 = min(shooter.primary_gun.mag_ammo * (shooter.primary_gun.fire_rate if shooter.primary_gun.gun_type == 3 else 1), shooter.primary_gun.fire_rate) * shooter.primary_gun.damage
    #     rt = distance_tuples(shooter.hitbox.middle, enemy.hitbox.middle)
    #     if r1 <= rt: d1 = 0
    #     if r2 <= rt: d2 = 0
    #     if d1 > d2:actions.cycle_primary()
    #     if self.reload_needed(shooter):
    #         actions.set_action(ActionType.reload)
    #     elif max(d1,d2)>0:
    #         actions.set_shoot(round(angle_to_point(shooter, enemy.hitbox.middle)))
    #     return

    def find_items(self, shooter: Shooter, actions, map_objects,game_board):
        gunlevel = shooter.primary_gun.level

        guns = list(filter(lambda obj: obj.object_type == ObjectType.gun, map_objects))
        if guns[0] != None and guns[0].level >= gunlevel:
            indexOfInRange = 0
            for i in range(len(guns)):
                  # print(distance_tuples( game_board.center, guns[i].hitbox.middle))
                  if( distance_tuples( game_board.center, guns[i].hitbox.middle) < game_board.circle_radius ):
                      indexOfInRange = i
                      break
                  indexOfInRange = -1

            if not indexOfInRange != -1:

                self.update_prev(shooter)
                actions.set_move(round(angle_to_point(shooter, guns[0].hitbox.middle)), min(round(distance_tuples(shooter.hitbox.middle, guns[indexOfInRange].hitbox.middle)),shooter.max_speed))
                # print(""moved"")
                return
        if shooter.has_empty_slot("upgrades"):
            upgrades = list(filter(lambda obj: obj.object_type == ObjectType.upgrade, map_objects))
            if upgrades[0] != None:
                indexOfInRange = 0
                for i in range(len(upgrades)):
                      # print(distance_tuples( game_board.center, upgrades[i].hitbox.middle))
                      if( distance_tuples( game_board.center, upgrades[i].hitbox.middle) < game_board.circle_radius ):
                          indexOfInRange = i
                          break
                      indexOfInRange = -1
                if not indexOfInRange != -1:
                    self.update_prev(shooter)

                    actions.set_move(round(angle_to_point(shooter, upgrades[0].hitbox.middle)),min(round(distance_tuples(shooter.hitbox.middle, upgrades[indexOfInRange].hitbox.middle)),shooter.max_speed))
                    # print(""moved"")
                    return

        money = list(filter(lambda obj: obj.object_type == ObjectType.money, map_objects))
        if money[0] != None:
            indexOfInRange = 0
            for i in range(len(money)):
                  # print(distance_tuples( game_board.center, money[i].hitbox.middle))
                  if( distance_tuples( game_board.center, money[i].hitbox.middle) < game_board.circle_radius ):
                      indexOfInRange = i
                      break
                  indexOfInRange = -1
            if not indexOfInRange != -1:
                self.update_prev(shooter)
                actions.set_move(round(angle_to_point(shooter, money[0].hitbox.middle)),min(round(distance_tuples(shooter.hitbox.middle, money[indexOfInRange].hitbox.middle)),shooter.max_speed))
                # print(""moved"")
                return


    def idle_tasks(self, shooter: Shooter, actions, partition_grid, game_board):
        # Stuff to do if there's no clear and present danger
        # Reload?
        # Shield?
        # Find Items?
        map_objects = partition_grid.get_all_objects()
        # if partition_grid.find_object_coordinates(shooter.hitbox.middle[0], shooter.hitbox.middle[1]):
        #     if partition_grid.find_object_coordinates(shooter.hitbox.middle[0], shooter.hitbox.middle[1]) == ObjectType.gun:
        #         if not shooter.has_empty_slot(""guns""):
        #             actions.drop_item(12, shooter.primary_gun.gun_type)
        #             actions.set_action(ActionType.interact)
        #         actions.set_action(ActionType.interact)
        #         return
        if partition_grid.find_object_coordinates(shooter.hitbox.middle[0], shooter.hitbox.middle[1]) == ObjectType.money:
                # and \
                # partition_grid.find_object_coordinates(shooter.hitbox.middle[0], shooter.hitbox.middle[1]) != ObjectType.shooter:

            #(partition_grid.find_object_coordinates(shooter.hitbox.middle[0], shooter.hitbox.middle[1]))
            # print(""Interacting"")
            actions.set_action(ActionType.interact)
            return

            # if shooter.health < 60 and (
            #         actions.select_item_to_use(1)
            #     return
            # shooter.inventory[""consumables""][0] == Consumables.health_pack or shooter.inventory[""consumables""][1] == Consumables.health_pack or
            #         shooter.inventory[""consumables""][2] == Consumables.health_pack):
            #
            #
            # if (shooter.inventory[""consumables""][0] == Consumables.radar or shooter.inventory[""consumables""][1] == Consumables.radar or
            #         shooter.inventory[""consumables""][2] == Consumables.radar):
            #     actions.select_item_to_use(4)
            #     return
            # if shooter.money >= 25 and shooter.health < 70:
            #     actions.select_item_to_buy(Consumables.health_pack)
            #     actions.set_action(ActionType.shop)
            #     return
            # elif shooter.money > 39:
            #     actions.select_item_to_buy(Consumables.radar)
            #     actions.set_action(ActionType.shop)

        # print(""Finding Items"")
        self.find_items(shooter, actions,map_objects,game_board)

        return


    def get_items(self):
        return


    def calculate_location(self, origin, speed, direction):
        new_x = origin[0] + (speed * math.cos(direction))
        new_y = origin[1] + (speed * math.sin(direction))
        return new_x, new_y


    def move_distance(self, heading, speed, map, shooter):
        if heading == 0:
            x = 0
            y = -1
        elif heading == 90:
            x = 1
            y = 0
        elif heading == 180:
            x = -1
            y = 0
        else:
            x = 0
            y = 1
        for i in range(speed):
            try:
                type = map.find_object_coordinates(shooter.hitbox.middle[0] + i * x, shooter.hitbox.middle[1] + i * y)
                if type == ObjectType.wall or type == ObjectType.door:
                    return i
            except:
                return i
        return speed


    def update_prev(self, shooter):
        self.prev_pos['prev4'] = self.prev_pos['prev3']
        self.prev_pos['prev3'] = self.prev_pos['prev2']
        self.prev_pos['prev2'] = self.prev_pos['prev1']
        self.prev_pos['prev1'] = shooter.hitbox.middle
        return

    def mov_dist(self):
        return

    path = None

    def go_to_mid(self, shooter, actions, board, map):
        if self.path is None:
            #build path
            self.path = []
            x, y = shooter.hitbox.middle
            tx, ty = board.center
            while((x-tx)**2+(y-ty)**2)**.5>shooter.max_speed:
                heading = 90
                speed = 25
                self.path.append((heading, speed))
        else:
            actions.set_move(path[0][0], path[0][1])
            self.path=self.path[1:]
            if len(self.path)==0:
                self.hitMid=True

    def cardinal_move(self, heading, speed, actions, map, shooter):
        self.update_prev(shooter)

        aim = round(heading / 90) * 90
        secondary = math.ceil(heading / 90) * 90 if round(heading / 90) * 90 == math.floor(
            heading / 90) * 90 else math.floor(heading / 90) * 90
        if (secondary == aim): secondary += 90
        aim%=360
        secondary%=360
        first = self.move_distance(aim, speed, map, shooter)
        second = self.move_distance(secondary, speed, map, shooter)
        if self.prev_pos['prev1'] == self.prev_pos['prev3'] or self.prev_pos['prev1'] == self.prev_pos['prev4']:
            # print(str(heading)+"": I""+str(aim)+"" ""+str(secondary))
            actions.set_move(((aim if first < second else secondary) + 180) % 360, speed)
        else:
            # print(str(heading)+"": S""+str(aim)+"" ""+str(secondary))
            actions.set_move(aim, speed)#if first >= second else secondary, speed)
        return

    def in_front(self, heading):
        if heading == 0:
            x = 0
            y = -10
        elif heading == 90:
            x = 10
            y = 0
        elif heading == 180:
            x = -10
            y = 0
        else:
            x = 0
            y = 10
        return (x,y)

    def move_to_mid(self, shooter, turn, actions):
        if turn <= 6:
            actions.set_move(270 if shooter.hitbox.middle[1] > 250 else 90, 22)
        elif turn == 7:
            actions.set_move(270 if shooter.hitbox.middle[1] > 250 else 90, 23)
        elif turn <= 14:
            actions.set_move(0 if shooter.hitbox.middle[0] < 250 else 180, 22)
        else:
            actions.set_move(round(angle_to_point(shooter, (250, 250))), round(min(distance_tuples(shooter.hitbox.middle, (250,250)),shooter.max_speed)))

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
        # This is a tuple that represents the position 1 unit in front of where the player
        forward_position = (shooter.hitbox.middle[0] + shooter.hitbox.width + math.cos(math.radians(shooter.heading)),
                            shooter.hitbox.middle[1] + shooter.hitbox.height + math.sin(math.radians(shooter.heading)))
        # print(shooter.heading)
        facing = self.in_front(shooter.heading)
        object_in_front = None
        shooters = list(filter(lambda obj: obj.object_type == ObjectType.shooter, map_objects))
        self.move_to_mid(shooter, turn, actions)
        if distance_tuples(shooter.hitbox.middle,game_board.center) < 50 and len(shooters) > 0:
            self.attack_mode(shooter,actions,shooters[0])