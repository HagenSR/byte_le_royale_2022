import random

from game.common.hitbox import Hitbox
from game.controllers.controller import Controller
from game.common.stats import GameStats
from game.common.items.consumable import Consumable
from game.common.moving.damaging.grenade import Grenade
from game.common.enums import *


class ShopController(Controller):

    def __init__(self):
        super().__init__()

    def handle_actions(self, client):
        if client.action._chosen_action is ActionType.shop:
            if client.action.item_to_purchase is None:
                return
            # selected_object should come from Consumables enum
            item = client.action.item_to_purchase
            if client.shooter.money >= GameStats.shop_stats[item][
                "cost"]:
                if client.shooter.has_empty_slot('consumables'):
                    client.shooter.money = client.shooter.money - \
                                           GameStats.shop_stats[item]["cost"]
                    # Create consumable object to be appended to inventory.
                    # "consumable_enum" will store the the client's selected item.
                    if client.action.item_to_purchase is not Consumables.grenade:
                        bought_item = Consumable(
                            hitbox=Hitbox(1, 1, (1, 1), 0),
                            health=None,
                            consumable_enum=client.action.item_to_purchase)
                    else:
                        bought_item = Grenade(Hitbox=(1, 1, (1, 1)), health=5,
                                              fuse_time=GameStats.grenade_fuse_time, damage=40)
                    client.shooter.append_inventory(bought_item)
                else:
                    pass
