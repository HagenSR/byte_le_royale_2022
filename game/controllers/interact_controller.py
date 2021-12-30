import math

from game.controllers.controller import Controller
from game.common.stats import GameStats
from game.common.items.upgrade import Upgrade
from game.common.door import Door
from game.common.items.money import Money
from game.utils.collision_detection import check_collision
from game.common.moving.shooter import Shooter
from game.common.action import Action
from game.common.game_board import GameBoard
from game.common.enums import *


class InteractController(Controller):

    def __init__(self):
        super().__init__()

    def handle_actions(self, client, world):
        object_target = False
        if client.action._chosen_action is ActionType.interact:
            object_list = world["game_board"].partition.get_partition_objects(client.shooter.hitbox.position[0],
                                                                              client.shooter.hitbox.position[1])
            for obj in object_list:
                if check_collision(client.shooter.hitbox, obj.hitbox) and not isinstance(obj, Shooter):
                    object_target = obj
            if isinstance(object_target, Upgrade):
                self.interact_upgrade(client, world, object_target)
            elif isinstance(object_target, Money):
                self.interact_money(client, world, object_target)
            else:
                object_target = self.find_doors(client, world)
                if isinstance(object_target, Door):
                    self.interact_door(object_target)
                else:
                    raise ValueError("There is no object to interact with.")

    def interact_upgrade(self, client, world, upgrade):
        if client.shooter.has_empty_slot('upgrades'):
            client.shooter.append_inventory(upgrade)
            world["game_board"].partition.remove_object(upgrade)

    def interact_money(self, client, world, money):
        client.shooter.money = client.shooter.money + money.amount
        world["game_board"].partition.remove_object(money)

    def interact_door(self, door):
        if not door.open_state:
            door.open_state = True
            door.collidable = False

    def find_doors(self, client, world):
        middle = client.shooter.hitbox.middle
        door_dist_list = []
        for x in range(int(middle[0]), int(middle[0] + GameStats.max_allowed_dist_from_door)):
            obj = world["game_board"].partition.find_object_coordinates(x, middle[1])
            if isinstance(obj, Door):
                distance = math.dist((middle[0], middle[1]), (obj.hitbox.middle[0], obj.hitbox.middle[1]))
                door_dist_list.append((obj, distance))
        for x in range(int(middle[0] - GameStats.max_allowed_dist_from_door), int(middle[0])):
            obj = world["game_board"].partition.find_object_coordinates(x, middle[1])
            if isinstance(obj, Door):
                distance = math.dist((middle[0], middle[1]), (obj.hitbox.middle[0], obj.hitbox.middle[1]))
                door_dist_list.append((obj, distance))
        for x in range(int(middle[1]), int(middle[1] + GameStats.max_allowed_dist_from_door)):
            obj = world["game_board"].partition.find_object_coordinates(middle[0], x)
            if isinstance(obj, Door):
                distance = math.dist((middle[0], middle[1]), (obj.hitbox.middle[0], obj.hitbox.middle[1]))
                door_dist_list.append((obj, distance))
        for x in range(int(middle[1] - GameStats.max_allowed_dist_from_door), int(middle[1])):
            obj = world["game_board"].partition.find_object_coordinates(middle[0], x)
            if isinstance(obj, Door):
                distance = math.dist((middle[0], middle[1]), (obj.hitbox.middle[0], obj.hitbox.middle[1]))
                door_dist_list.append((obj, distance))
        if len(door_dist_list) > 0:
            sorted_list = sorted(door_dist_list, key=lambda z: z[1])
            return sorted_list[0][0]
        else:
            return False

        # obj = False
        # position = client.shooter.hitbox.middle
        # if world["game_board"].partition.find_object_coordinates(position[0], position[1] + 6):
        #     obj = world["game_board"].partition.find_object_coordinates(position[0], position[1] + 6)
        #     return obj
        # elif world["game_board"].partition.find_object_coordinates(position[0], position[1] - 6):
        #     obj = world["game_board"].partition.find_object_coordinates(position[0], position[1] - 6)
        #     return obj
        # elif world["game_board"].partition.find_object_coordinates(position[0] + 6, position[1]):
        #     obj = world["game_board"].partition.find_object_coordinates(position[0] + 6, position[1])
        #     return obj
        # elif world["game_board"].partition.find_object_coordinates(position[0] - 6, position[1]):
        #     obj = world["game_board"].partition.find_object_coordinates(position[0] - 6, position[1])
        #     return obj
        # else:
        #     return obj
