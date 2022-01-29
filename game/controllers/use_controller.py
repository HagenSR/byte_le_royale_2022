from game.common.stats import GameStats
from game.controllers.controller import Controller
from game.common.enums import *


class UseController(Controller):
    def __init__(self):
        super().__init__()

    def handle_actions(self, client):
        if client.shooter.speed_boost_cooldown <= 0:
            client.shooter.max_speed = GameStats.player_stats['max_distance_per_turn']
            for upgrade in client.shooter.inventory['upgrades']:
                if upgrade and upgrade.upgrade_enum == Upgrades.movement_boots:
                    upgrade.applied = False
        else:
            client.shooter.speed_boost_cooldown -= 1
        if client.shooter.radar_cooldown <= 0:
            client.shooter.view_distance = GameStats.player_stats['view_distance']
        else:
            client.shooter.radar_cooldown -= 1

        # if the client wants to drop an item, try to do it
        if client.action.item_to_drop:
            client.shooter.remove_from_inventory_enum(client.action.item_to_drop)

        # player action
        if client.action._chosen_action is ActionType.use:
            obj = client.shooter.remove_from_inventory(client.action.item_to_use)
            if not obj:
                raise ValueError("Object to use not in inventory")
            if obj.consumable_type == Consumables.health_pack:
                if client.shooter.health + GameStats.consumable_stats['health_pack_heal_amount'] > 100:
                    client.shooter.health = 100
                else:
                    client.shooter.health += GameStats.consumable_stats['health_pack_heal_amount']
            if obj.consumable_type == Consumables.shield:
                client.shooter.shield = True
            if obj.consumable_type == Consumables.speed and client.shooter.speed_boost_cooldown <= 0:
                client.shooter.max_speed *= 1 + GameStats.consumable_stats['speed_increase_percent']
                client.shooter.speed_boost_cooldown = GameStats.consumable_stats['speed_cooldown_turns']
            if obj.consumable_type == Consumables.radar and client.shooter.radar_cooldown <= 0:
                client.shooter.view_distance *= 1 + GameStats.consumable_stats['radar_range_increase_percent']
                client.shooter.radar_cooldown = GameStats.consumable_stats['radar_cooldown_turns']
