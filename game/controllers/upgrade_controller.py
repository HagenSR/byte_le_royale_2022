from game.common.enums import Upgrades, ObjectType
from game.common.stats import GameStats
from game.controllers.controller import Controller


class UpgradeController(Controller):
    def __init__(self):
        super().__init__()

    def handle_actions(self, client):
        # if the client wants to drop an item, try to do it
        if client.action.item_to_drop != 0 and client.action.item_sub_type_to_drop != 0:
            obj = client.shooter.remove_from_inventory_enum(client.action.item_to_drop)
            if obj and obj.object_type == ObjectType.upgrade:
                if obj.upgrade_enum == Upgrades.armor:
                    client.shooter.armor = 1.0
                if obj.upgrade_enum == Upgrades.movement_boots:
                    client.shooter.max_speed /= 1 + GameStats.upgrade_stats['movement_boost']
                if obj.upgrade_enum == Upgrades.backpack:
                    client.shooter.remove_consumable_slots(GameStats.upgrade_stats["backpack_slot_increase"])

        for upgrade in client.shooter.inventory['upgrades']:
            if upgrade is not None:
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
