from game.common.moving.moving_object import MovingObject
from game.common.stats import GameStats
from game.common.enums import *


class Shooter(MovingObject):
    def __init__(self, heading=0, speed=0, coordinates=GameStats.player_stats['starting_coordinates']):
        super().__init__(
            heading,
            speed,
            GameStats.player_stats['starting_health'],
            coordinates,
            GameStats.player_stats['hitbox'],
            collidable = True
        )
        self.object_type = ObjectType.shooter
        self.inventory = []
        self.money = GameStats.player_stats['starting_money']
        self.armor = None
        self.visible = []
        self.view_radius = GameStats.player_stats['view_radius']
        self.moving = False

    # set the heading and direction in a controlled way, might need to add distance attribute later
    def move(self, heading):
        super().set_heading(heading)
        super().set_speed(GameStats.player_stats['move_speed'])
        self.moving = True

    def stop(self):
        super().set_speed(0)
        self.moving = False

    def to_json(self):
        data = super().to_json()

        data['inventory'] = [item.to_json() for item in self.inventory]
        data['visible'] = [obj.to_json() for obj in self.visible]

        data['money'] = self.money
        data['armor'] = self.armor
        data['view_radius'] = self.view_radius
        data['moving'] = self.moving

        return data

    def from_json(self, data):
        super().from_json(data)
        self.inventory = data['inventory']
        self.money = data['money']
        self.armor = data['armor']
        self.visible = data['visible']
        self.view_radius = data['view_radius']
        self.moving = data['moving']
