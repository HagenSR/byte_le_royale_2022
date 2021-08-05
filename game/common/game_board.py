from game.common.game_object import GameObject
from game.common.enums import ObjectType
from game.common.stats import GameStats
import math


class GameBoard(GameObject):
    # the width and height parameters have default values to allow them to be
    # set for unit testing purposes
    def __init__(self, width=GameStats.game_board_width,
                 height=GameStats.game_board_height):
        super().__init__()
        self.object_type = ObjectType.game_board

        # pull width and height values from GameStats
        self.width = width
        self.height = height

        # instantiate lists with an empty list
        self.player_list = []
        self.wall_list = []
        self.door_list = []
        self.items_list = []
        self.upgrades_list = []
        self.lethal_list = []

        # this calculates starting radius to totally encompass the map at start
        self.circle_radius = math.sqrt(
            (self.width / 2) ** 2 + (self.height / 2) ** 2)

        # set turn counter to 0, not sure the use for this yet
        self.turn = 0

    def obfuscate(self):
        super().obfuscate()

        self.player_list = None

    def to_json(self):
        data = super().to_json()

        data['width'] = self.width
        data['height'] = self.height

        data['player_list'] = self.player_list
        data['wall_list'] = self.wall_list
        data['door_list'] = self.door_list
        data['items_list'] = self.items_list
        data['upgrades_list'] = self.upgrades_list
        data['lethal_list'] = self.lethal_list

        data['circle_radius'] = self.circle_radius

        data['turn'] = self.turn

        return data

    def from_json(self, data):
        super().from_json(data)

        self.width = data['width']
        self.height = data['height']

        self.player_list = data['player_list']
        self.wall_list = data['wall_list']
        self.door_list = data['door_list']
        self.items_list = data['items_list']
        self.upgrades_list = data['upgrades_list']
        self.lethal_list = data['lethal_list']

        self.circle_radius = data['circle_radius']

        self.turn = data['turn']
