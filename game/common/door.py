from game.common.enums import ObjectType
from game.common.map_object import MapObject
from game.common.stats import GameStats


class Door(MapObject):
    def __init__(
            self,
            hitbox,
            health=GameStats.default_wall_health,
            open_speed=GameStats.door_opening_speed):
        super().__init__(health, hitbox, collidable=True)
        self.opening_speed = open_speed
        self.open_state = False
        self.object_type = ObjectType.door

    def to_json(self):
        data = super().to_json()
        data['opening_speed'] = self.opening_speed
        data['open_state'] = self.open_state
        return data

    def from_json(self, data):
        super().from_json(data)
        self.opening_speed = data['opening_speed']
        self.open_state = data['open_state']
        return self
