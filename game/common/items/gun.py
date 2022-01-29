from game.common.enums import *
import game.common.stats as stats
from game.common.items.item import Item


class Gun(Item):
    def __init__(self, gun_type=GunType.none, level=0, hitbox=None):
        super().__init__(hitbox)
        self.object_type = ObjectType.gun

        self.gun_type = gun_type
        self.level = level
        self.pattern = stats.GameStats.gun_stats[self.level][gun_type]['pattern']
        self.damage = stats.GameStats.gun_stats[self.level][gun_type]['damage']
        self.fire_rate = stats.GameStats.gun_stats[self.level][gun_type]['fire_rate']
        self.range = stats.GameStats.gun_stats[self.level][gun_type]['range']
        self.mag_size = stats.GameStats.gun_stats[self.level][gun_type]['mag_size']
        self.mag_ammo = self.mag_size

    def reload(self):
        self.mag_ammo = self.mag_size

    def to_json(self):
        data = super().to_json()
        data['gun_type'] = self.gun_type
        data['level'] = self.level
        data['pattern'] = self.pattern
        data['damage'] = self.damage
        data['fire_rate'] = self.fire_rate
        data['range'] = self.range
        data['mag_size'] = self.mag_size

        return data

    def from_json(self, data):
        super().from_json(data)
        self.level = data['level']
        self.gun_type = data['gun_type']
        self.pattern = data['pattern']
        self.damage = data['damage']
        self.fire_rate = data['fire_rate']
        self.range = data['range']
        self.mag_size = data['mag_size']
        return self

    def __str__(self):
        return f"""
            Gun Type: {self.gun_type}
            Level: {self.level}
            Pattern: {self.pattern}
            Damage: {self.damage}
            Fire Rate: {self.fire_rate}
            Range: {self.range}
            Mag Size: {self.mag_size}
            """
