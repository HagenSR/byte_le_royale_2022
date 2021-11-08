from game.common.game_object import GameObject


class Teleporter(GameObject):

    def __init__(self, hitbox, cooldown = 20):
        super().__init__()
        self.hitbox = hitbox
        # cooldown is in terms of seconds
        self.cooldown = cooldown

    def to_json(self):
        data = super().to_json()
        data['hitbox'] = self.hitbox
        data['cooldown'] = self.cooldown
        return data

    def from_json(self, data):
        data = super().from_json()
        self.hitbox = data['hitbox']
        self.cooldown = data['cooldown']
        return self
