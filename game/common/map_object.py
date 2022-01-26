from game.common.game_object import GameObject
from game.common.enums import ObjectType
from game.common.hitbox import Hitbox


class MapObject(GameObject):
    def __init__(self, health=None, hitbox=None, collidable=True):
        super().__init__()
        self.object_type = ObjectType.map_object
        self.health = health
        self.hitbox = hitbox
        self.collidable = collidable

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, val):
        self.__health = val

    def to_json(self):
        data = super().to_json()
        data['health'] = self.health
        data['hitbox'] = self.hitbox.to_json()
        data['collidable'] = self.collidable

        return data

    def from_json(self, data):
        super().from_json(data)
        self.health = data['health']
        self.hitbox = Hitbox(1, 1, (0, 0))
        self.hitbox.from_json(data['hitbox'])
        self.collidable = data['collidable']
        return self

    def __str__(self):
        return f"""
             ObjectType: {type(self)}
             Health: {self.health}
             Hitbox: {self.hitbox.__str__()}
             Collidable: {self.collidable}
             """
