from game.common.items.consumable import Consumable
from game.common.items.gun import Gun
from game.controllers.controller import Controller

from game.common.stats import GameStats
from game.common.items.upgrade import Upgrade
from game.common.door import Door
from game.common.items.money import Money
from game.utils import collision_detection
from game.utils.collision_detection import check_collision
from game.common.moving.shooter import Shooter
from game.common.enums import *


class InteractController(Controller):

    def __init__(self):
        super().__init__()

    def handle_actions(self, client, world):
        if client.action._chosen_action is ActionType.interact:
            # partition grid checks to see if any objects collide with the player's hitbox
            object_target = world["game_board"].partition.find_object_hitbox(client.shooter.hitbox)
            if isinstance(object_target, Upgrade) or isinstance(object_target, Gun):
                self.interact_item(client, world, object_target)
            elif isinstance(object_target, Money):
                self.interact_money(client, world, object_target)
            else:
                # if there are no objects beneath the player, the controller checks if there are nearby doors
                # to interact with.
                object_target = self.find_doors(client.shooter.hitbox.middle, world["game_board"].partition)
                if isinstance(object_target, Door):
                    self.interact_door(world["game_board"].partition, object_target)

    # removes upgrade from beneath the player and adds the upgrade to their inventory
    def interact_item(self, client, world, item):
        slot_type = None
        if isinstance(item, Upgrade):
            slot_type = 'upgrades'
        else:
            slot_type = 'guns'
        if client.shooter.has_empty_slot(slot_type):
            client.shooter.append_inventory(item)
            world["game_board"].partition.remove_object(item)

    # removes money from beneath the player and adds the money amount to their stats
    def interact_money(self, client, world, money):
        client.shooter.money = client.shooter.money + money.amount
        world["game_board"].partition.remove_object(money)

    # inverses door state and allows the users to walk through it
    def interact_door(self, partition, door):
        in_door_obj = partition.find_object_hitbox(door.hitbox)
        if not in_door_obj and isinstance(in_door_obj, Shooter):
            return
        door.open_state = not door.open_state
        door.collidable = not door.collidable

    def find_doors(self, player_coords, partition):
        objects = []
        for x in range(0, GameStats.game_board_width, partition.partition_width):
            for y in range(0, GameStats.game_board_height, partition.partition_height):
                if collision_detection.intersect_circle(
                        player_coords,
                        GameStats.max_allowed_dist_from_door,
                        partition.get_partition_hitbox(x, y)):

                    objects.extend(partition.get_partition_objects(x, y))

        objects = list(filter(lambda obj: isinstance(obj, Door), objects))
        return min(objects,
                   key=lambda obj:
                   collision_detection.distance(player_coords[0],
                                                player_coords[1],
                                                obj.hitbox.position[0],
                                                obj.hitbox.position[1]))
