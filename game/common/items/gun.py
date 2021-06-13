from game.common.enums import *
import game.common.stats as stats
from game.common.items.item import Item


class Gun(Item):
    def __init__(self, gun_type, level, coordinates=None, hitbox=None):
        super().__init__(coordinates, hitbox)
        self.object_type = ObjectType.gun

        self.gun_type = gun_type
        # Leveling subject to change
        self.level = level
        self.pattern = stats.GameStats.gun_stats[gun_type]['pattern']
        self.damage = (round(stats.GameStats.gun_stats[gun_type]['damage']
            * (stats.GameStats.gun_stats[gun_type]['level_mod'] ** self.level), 1)
            if self.level > GunLevel.level_zero else 0)
        self.fire_rate = (round(stats.GameStats.gun_stats[gun_type]['fire_rate']
            * (stats.GameStats.gun_stats[gun_type]['level_mod'] ** self.level))
            if self.level > GunLevel.level_zero else 0)
        self.range = (round(stats.GameStats.gun_stats[gun_type]['range']
            * (stats.GameStats.gun_stats[gun_type]['level_mod'] ** self.level))
            if self.level > GunLevel.level_zero else 0)
        self.mag_size = (round(stats.GameStats.gun_stats[gun_type]['mag_size']
            * (stats.GameStats.gun_stats[gun_type]['level_mod'] ** self.level))
            if self.level > GunLevel.level_zero else 0)
        self.reload_speed = (round(stats.GameStats.gun_stats[gun_type]['reload_speed']
            * (stats.GameStats.gun_stats[gun_type]['level_mod'] ** self.level))
            if self.level > GunLevel.level_zero else 0)
        if self.level > GunLevel.level_zero:
            self.cooldown = stats.GameStats.gun_stats[gun_type]['cooldown']
            self.cooldown['max'] = round(self.cooldown['max']
                    * (stats.GameStats.gun_stats[gun_type]['level_mod'] ** self.level))
        else:
            self.cooldown = {'max': 0, 'rate': 0}

    def to_json(self):
        data = super().to_json()
        data['gun_type'] = self.gun_type
        data['level'] = self.level
        data['pattern'] = self.pattern
        data['damage'] = self.damage
        data['fire_rate'] = self.fire_rate
        data['range'] = self.range
        data['mag_size'] = self.mag_size
        data['reload_speed'] = self.reload_speed
        data['cooldown'] = self.cooldown

        return data

    def from_json(self, data):
        super().from_json(data)
        self.gun_type = data['gun_type']
        self.level = data['level']
        self.pattern = data['pattern']
        self.damage = data['damage']
        self.fire_rate = data['fire_rate']
        self.range = data['range']
        self.mag_size = data['mag_size']
        self.reload_speed = data['reload_speed']
        self.cooldown = data['cooldown']

    def __str__(self):
        return f"""
            Gun Type: {self.gun_type}
            Level: {self.level}
            Pattern: {self.pattern}
            Damage: {self.damage}
            Fire Rate: {self.fire_rate}
            Range: {self.range}
            Mag Size: {self.mag_size}
            Reload Speed: {self.reload_speed}
            Cooldown: {self.cooldown}
            """
