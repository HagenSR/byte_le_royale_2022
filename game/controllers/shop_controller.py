from game.controllers.controller import Controller
from game.common.stats import GameStats
from game.common.items.consumable import Consumable
from game.common.enums import *


class ShopController(Controller):

    def __init__(self):
        super().__init__()
        self.current_world_data = None

    def handle_actions(self, client, world):
        if client.action.chosen_action is ActionType.shop:
            self.process_purchase(client, client.action.selected_object)

    def process_purchase(self, client, item):
        if client.shooter.money >= GameStats.shop_stats[item]['cost']:
            if client.shooter.has_empty_slot(item):
                client.shooter.money = client.shooter.money - GameStats.shop_stats[item]['cost']
                client.shooter.append_inventory(item)
            else:
                raise ValueError("Inventory slots for consumables is full.")

        else:
            raise ValueError("Insufficient funds for item.")
