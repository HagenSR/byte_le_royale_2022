import math

from game.controllers.controller import Controller
from game.common.stats import GameStats
from game.common.items.upgrade import Upgrade
from game.common.door import Door
from game.common.items.money import Money
from game.utils.collision_detection import check_collision
from game.common.moving.shooter import Shooter
from game.common.enums import *


class InteractController(Controller):

    def __init__(self):
        super().__init__()

    def handle_actions(self, client, world):
        object_target = False
        if client.action._chosen_action is ActionType.interact:

            # gets list of objects in the same partition as the player
            object_list = world["game_board"].partition.get_partition_objects(client.shooter.hitbox.position[0],
                                                                              client.shooter.hitbox.position[1])

            # partition grid checks to see if any objects collide with the player's hitbox
            object_target = world["game_board"].partition.find_object_hitbox(client.shooter.hitbox)
            if isinstance(object_target, Upgrade):
                self.interact_upgrade(client, world, object_target)
            elif isinstance(object_target, Money):
                self.interact_money(client, world, object_target)
            else:
                # if there are no objects beneath the player, the controller checks if there are nearby doors
                # to interact with.
                object_target = self.find_doors(client.shooter, world["game_board"].partition)
                if isinstance(object_target, Door):
                    self.interact_door(object_target)
                else:
                    raise ValueError("There is no object to interact with.")

    # removes upgrade from beneath the player and adds the upgrade to their inventory
    def interact_upgrade(self, client, world, upgrade):
        if client.shooter.has_empty_slot('upgrades'):
            client.shooter.append_inventory(upgrade)
            world["game_board"].partition.remove_object(upgrade)

    # removes money from beneath the player and adds the money amount to their stats
    def interact_money(self, client, world, money):
        client.shooter.money = client.shooter.money + money.amount
        world["game_board"].partition.remove_object(money)

    # changes door state to open and allows the users to walk through it
    def interact_door(self, door):
        if not door.open_state:
            door.open_state = True
            door.collidable = False

    # method used to find the closest door to interact with
    def find_doors(self, shooter, partition_grid):
        middle = shooter.hitbox.middle
        end_value = GameStats.max_allowed_dist_from_door
        door_dist_list = []
        # checks for doors in range from the right
        for x in range(int(middle[0]), int(middle[0] + end_value + 1)):
            obj = partition_grid.find_object_coordinates(x, middle[1])
            if isinstance(obj, Door) and (
                    len(door_dist_list) == 0 or obj is not door_dist_list[len(door_dist_list) - 1][0]):
                distance = math.dist((middle[0], middle[1]), (x, obj.hitbox.middle[1]))
                door_dist_list.append((obj, distance))
        # checks for doors in range from the left
        for x in range(int(middle[0] - end_value), int(middle[0] + 1)):
            obj = partition_grid.find_object_coordinates(x, middle[1])
            if isinstance(obj, Door):
                distance = math.dist((middle[0], middle[1]), (x, middle[1]))
                if len(door_dist_list) == 0 or (obj is not door_dist_list[len(door_dist_list) - 1][0]):
                    door_dist_list.append((obj, distance))
                if obj is door_dist_list[len(door_dist_list) - 1][0] and \
                        distance < door_dist_list[len(door_dist_list) - 1][1]:
                    door_dist_list.pop()
                    door_dist_list.append((obj, distance))
        # checks for doors in range from the bottom
        for x in range(int(middle[1]), int(middle[1] + end_value + 1)):
            obj = partition_grid.find_object_coordinates(middle[0], x)
            if isinstance(obj, Door) and (
                    len(door_dist_list) == 0 or obj is not door_dist_list[len(door_dist_list) - 1][0]):
                distance = math.dist((middle[0], middle[1]), (obj.hitbox.middle[0], x))
                door_dist_list.append((obj, distance))
        # checks for doors in range from the top
        for x in range(int(middle[1] - end_value), int(middle[1] + 1)):
            obj = partition_grid.find_object_coordinates(middle[0], x)
            if isinstance(obj, Door):
                distance = math.dist((middle[0], middle[1]), (obj.hitbox.middle[0], x))
                if len(door_dist_list) == 0 or (obj is not door_dist_list[len(door_dist_list) - 1][0]):
                    door_dist_list.append((obj, distance))
                if obj is door_dist_list[len(door_dist_list) - 1][0] and \
                        distance < door_dist_list[len(door_dist_list) - 1][1]:
                    door_dist_list.pop()
                    door_dist_list.append((obj, distance))
        if len(door_dist_list) > 0:
            # sort the doors that are in range by distance
            sorted_list = sorted(door_dist_list, key=lambda z: z[1])
            # returns closest door
            return sorted_list[0][0]
        else:
            return False
