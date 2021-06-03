from game.common.enums import Upgrades


class Upgrade:
    bullet_speed_increase = {
        Upgrades.gun_upgrades: 20,
    }
    player_speed_increase = {
        Upgrades.movement_upgrades: 20,
    }
    player_sight_increase = {
        Upgrades.sight_upgrades: 20,
    }