from game.common.enums import Upgrades
from game.common.stats import GameStats
from game.controllers.controller import Controller


class UpgradeController(Controller):
    def __init__(self):
        super().__init__()

    def handle_actions(self, client):
        for upgrade in client.shooter.inventory['upgrades']:
            if upgrade.applied:
                continue
            if upgrade.upgrade_enum == Upgrades.armor:
                client.shooter.armor = GameStats.upgrade_stats["armor_damage_reduction"]
            elif upgrade.upgrade_enum == Upgrades.movement_boots:
                client.shooter.max_speed *= 1 + GameStats.upgrade_stats["movement_boost"]
            elif upgrade.upgrade_enum == Upgrades.backpack:
                for i in range(GameStats.upgrade_stats["backpack_slot_increase"]):
                    client.shooter.add_new_slot("consumables")
            upgrade.applied = True
