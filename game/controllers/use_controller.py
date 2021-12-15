from game.common.stats import GameStats
from game.controllers.controller import Controller
from game.common.enums import *


class UseController(Controller):
    def __init__(self):
        super().__init__()

    def handle_actions(self, client):
        if client.action._chosen_action is ActionType.use:
            obj = client.shooter.remove_from_inventory(client.action.item_to_use)
            if not obj:
                raise ValueError("Object to use not in inventory")
            if obj.consumable_type == Consumables.health_pack:
                client.shooter.health += GameStats.consumable_stats['health_pack_heal_amount']
            if obj.consumable_type == Consumables.shield:
                client.shooter.shield = True
            if obj.consumable_type == Consumables.speed:
                client.shooter.speed *= 1 + GameStats.consumable_stats['speed_increase_percent']
            if obj.consumable_type == Consumables.radar:
                client.shooter.view_distance *= 1 + GameStats.consumable_stats['radar_range_increase_percent']