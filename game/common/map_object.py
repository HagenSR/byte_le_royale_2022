from game.common.game_object import GameObject
from game.common.enums import *

class MapObject(GameObject):
    def __init__(self, map_object_type=None, health=None, coordinates=None, hitbox=None, collidable=None):
        super().__init__()
        self.health = health
        self.coordinates = coordinates
        self.hitbox = hitbox
        self.collidable = collidable
    
    def to_json(self):
        data = super().__init__()
        data['health'] = self.health
        data['coordinates'] = self.coordinates
        data['hitbox'] = self.hitbox
        data['collidable'] = self.collidable

    def from_json(self, data):
        self.health = data['health']
        self.coordinates = data['coordinates']
        self.hitbox = data['hitbox']
        self.collidable = data['collidable']

