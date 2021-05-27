from game.common.game_object import GameObject
from game.common.enums import *
from game.common.stats import GameStats

class Gun(GameObject):
    def __init__(self, gun_type): 
        super().__init__()
        self.gun_type = gun_type
        self.damage = GameStats.gun_stats[gun_type]['damage']
        self.fire_rate = GameStats.gun_stats[gun_type]['fire_rate']
        self.cooldown = GameStats.gun_stats[gun_type]['cooldown']
        self.range = GameStats.gun_stats[gun_type]['range']
        self.mag_size = GameStats.gun_stats[gun_type]['mag_size']
        self.reload_speed = GameStats.gun_stats[gun_type]['reload_speed']

    def to_json(self):
        data = super().to_json()
        data['gun_type'] = self.gun_type
        data['damage'] = self.damage
        data['fire_rate'] = self.fire_rate
        data['cooldown'] = self.cooldown
        data['range'] = self.range
        data['mag_size'] = self.mag_size
        data['reload_speed'] = self.reload_speed

        return data

    def from_json(self, data):
        super().from_json(data)
        self.gun_type = data['gun_type']
        self.damage = data['damage']
        self.fire_rate = data['fire_rate']
        self.cooldown = data['cooldown']
        self.range = data['range']
        self.mag_size = data['mag_size']
        self.reload_speed= data['reload_speed']

    def __str__(self):
        return f"""
            Gun Type: {self.gun_type}
            Damage: {self.damage}
            Fire Rate: {self.fire_rate}
            Cooldown: {self.cooldown}
            Range: {self.range}
            Mag Size: {self.mag_size}
            Reload Speed: {self.reload_speed}
            """
