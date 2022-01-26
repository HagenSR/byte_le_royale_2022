from game.common.enums import ObjectType
from game.common.stats import GameStats
from game.common.game_object import GameObject


class Ray(GameObject):
    def __init__(
            self,
            origin=None,
            endpoint=None,
            collision=None,
            damage=None):
        super().__init__()
        self.object_type = ObjectType.ray

        self.origin = origin
        self.endpoint = endpoint
        self.collision = collision
        self.damage = damage

    def obfuscate(self):
        super().obfuscate()
        del self.origin

    def to_json(self):
        data = super().to_json()
        data['origin'] = self.origin
        data['endpoint'] = self.endpoint
        data['collision'] = self.collision.to_json(
        ) if self.collision is not None else None
        data['damage'] = self.damage

        return data

    def from_json(self, data):
        super().from_json(data)
        self.origin = data['origin']
        self.endpoint = data['endpoint']
        # Leaving for now since collision could be any object on the map
        #self.collision = data['collision']
        self.damage = data['damage']

    def __str__(self):
        return f"""
            Origin: {self.origin}
            Endpoint: {self.endpoint}
            Collision: {self.collision}
            Damage: {self.damage}
            """
