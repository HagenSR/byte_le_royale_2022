from game.common.game_object import GameObject
from game.common.enums import *


class MapObject(GameObject):
    def __init__(self, health=None, hitbox=None, collidable=None):
        super().__init__()
        self.object_type = ObjectType.map_object
        self.health = health
        self.hitbox = hitbox
        self.collidable = collidable

    def to_json(self):
        data = super().to_json()
        data['health'] = self.health
        data['coordinates'] = self.coordinates
        data['hitbox'] = self.hitbox
        data['collidable'] = self.collidable

        return data

    def from_json(self, data):
        super().from_json(data)
        self.health = data['health']
        self.coordinates = data['coordinates']
        self.hitbox = data['hitbox']
        self.collidable = data['collidable']

    def __str__(self):
        return f"""
             Health: {self.health}
             Coordinates: {self.coordinates}
             Hitbox: {self.hitbox}
             Collidable: {self.collidable}
             """
