from game.common.map_object import MapObject


class Teleporter(MapObject):

    def __init__(self, hitbox, cooldown = 20, health = 10):
        super().__init__(health=health, hitbox=hitbox, collidable=False)
        # cooldown is in terms of seconds
        self.cooldown = cooldown

    def to_json(self):
        data = super().to_json()
        data['cooldown'] = self.cooldown
        return data

    def from_json(self, data):
        data = super().from_json()
        self.cooldown = data['cooldown']
        return self
