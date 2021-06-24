from game.common.enums import ObjectType
from game.common.stats import GameStats

class Ray(GameObject):
    def __init__(self, origin, endpoint, collision=None, damage=None):
        super().__init__()
        self.object_type = ObjectType.ray

        self.origin = origin
        self.endpoint = endpoint
        self.collision = collision
        self.damage = damage

    def to_json(self):
        data = super().to_json()
        data['origin'] = self.origin
        data['endpoint'] = self.endpoint
        data['collision'] = self.collision
        data['damage'] = self.damage

    def from_json(self, data):
        super().from_json(data)
        self.origin = data['origin']
        self.endpoint = data['endpoint']
        self.collision = data['collision']
        self.damage = data['damage']

    def __str__(self):
        return f"""
            Origin: {self.origin}
            Endpoint: {self.endpoint}
            Collision: {self.collision}
            Damage: {self.damage}
            """
