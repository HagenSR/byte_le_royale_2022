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
        self.object_target = None

    def handle_actions(self, client, game_board):
        if client.action._chosen_action is ActionType.interact:
            # partition grid checks to see if any objects collide with the player's hitbox
            self.object_target = game_board.partition.find_object_hitbox(client.shooter.hitbox)
            if isinstance(self.object_target, Upgrade) or isinstance(self.object_target, Gun):
                self.interact_item(client, game_board, self.object_target)
            elif isinstance(self.object_target, Money):
                self.interact_money(client, game_board, self.object_target)
            else:
                # if there are no objects beneath the player, the controller checks if there are nearby doors
                # to interact with.
                self.object_target = self.find_doors(client.shooter.hitbox.middle, game_board.partition)
                if isinstance(self.object_target, Door):
                    self.interact_door(game_board.partition, self.object_target)

    # removes upgrade from beneath the player and adds the upgrade to their inventory
    def interact_item(self, client, game_board, item):
        slot_type = None
        if isinstance(item, Upgrade):
            slot_type = 'upgrades'
        else:
            slot_type = 'guns'
        if client.shooter.has_empty_slot(slot_type):
            client.shooter.append_inventory(item)
            game_board.partition.remove_object(item)

    # removes money from beneath the player and adds the money amount to their stats
    def interact_money(self, client, game_board, money):
        client.shooter.money = client.shooter.money + money.amount
        game_board.partition.remove_object(money)

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
        if len(objects) > 0:
            return min(objects,
                       key=lambda obj:
                       collision_detection.distance(player_coords[0],
                                                    player_coords[1],
                                                    obj.hitbox.position[0],
                                                    obj.hitbox.position[1]))
        else:
            return False
