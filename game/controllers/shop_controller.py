import random
from game.controllers.controller import Controller
from game.common.stats import GameStats
from game.common.items.consumable import Consumable
from game.common.enums import *


class ShopController(Controller):
    # shop_inventory keeps track of how many of each consumables are in the shop throughout the game
    # Each purchase shrinks the quantity for that consumables object
    shop_inventory = {
        Consumables.speed: {
            'quantity': GameStats.shop_stats[Consumables.speed]['quantity']
        },
        Consumables.health_pack: {
            'quantity': GameStats.shop_stats[Consumables.health_pack]['quantity']
        },
        Consumables.shield: {
            'quantity': GameStats.shop_stats[Consumables.shield]['quantity']
        }
    }

    def __init__(self):
        super().__init__()

    def handle_actions(self, client):
        if client.action._chosen_action is ActionType.shop:
            # selected_object should come from Consumables enum
            self.process_purchase(client, client.action.item_to_purchase)

    # item = client.action.item_to_purchase
    def process_purchase(self, client, item):
        if client.shooter.money >= GameStats.shop_stats[item][
                "cost"] and self.shop_inventory[item]["quantity"] > 0:
            if client.shooter.has_empty_slot('consumables'):
                client.shooter.money = client.shooter.money - \
                    GameStats.shop_stats[item]["cost"]
                # Create consumable object to be appended to inventory.
                # "consumable_enum" will store the the client's selected item.
                bought_item = Consumable(
                    hitbox=None,
                    health=None,
                    consumable_enum=client.action.item_to_purchase)
                client.shooter.append_inventory(bought_item)
                self.shop_inventory[item]["quantity"] = self.shop_inventory[item]["quantity"] - 1
            else:
                raise ValueError("Inventory slots for consumables is full.")

        else:
            raise ValueError(
                "Insufficient funds for item or item is out of stock in shop.")
