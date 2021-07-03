from game.common.game_object import GameObject
from game.common.enums import ObjectType
from game.common.stats import GameStats
import math


class GameBoard(GameObject):
    # the width and height parameters have default values to allow them to be set for unit testing purposes
    def __init__(self, width=GameStats.game_board_width, height=GameStats.game_board_height):
        super().__init__()
        self.object_type = ObjectType.game_board
        
        # pull width and height values from GameStats
        self.width = width
        self.height = height

        # instantiate lists with an empty list
        self.player_list = []
        self.wall_list = []
        self.items_list = []
        self.upgrades_list = []
        self.lethal_list = []

        # this calculates starting radius to totally encompass the map at start
        self.__circle_radius = math.sqrt( ( self.width / 2 ) ** 2 + ( self.height / 2 ) ** 2 )

        # set turn counter to 0, not sure the use for this yet
        self.turn = 0
        
    @property
    def circle_radius(self):
        return self.__circle_radius
    
    # setter for heading. Should be degrees between 0 and 360 inclusive
    @circle_radius.setter
    def circle_radius(self, val):
        if val > 0:
            self.__circle_radius = val
        else:
            self.__circle_radius = 0

    def obfuscate(self):
        super().obfuscate()

        self.player_list = None

    def to_json(self):
        data = super().to_json()

        data['width'] = self.width
        data['height'] = self.height

        data['player_list'] = [player.to_json() for player in self.player_list]
        data['wall_list'] = [wall.to_json() for wall in self.wall_list]
        data['items_list'] = [item.to_json() for item in self.items_list]
        data['upgrades_list'] = [upgrade.to_json() for upgrade in self.upgrades_list]
        data['lethal_list'] = [lethal.to_json() for lethal in self.lethal_list]

        data['circle_radius'] = self.circle_radius

        data['turn'] = self.turn

        return data

    def from_json(self, data):
        super().from_json(data)

        self.width =  data['width']
        self.height = data['height']

        self.player_list = data['player_list']
        self.wall_list = data['wall_list']
        self.items_list = data['items_list']
        self.upgrades_list = data['upgrades_list']
        self.lethal_list = data['lethal_list']

        self.circle_radius = data['circle_radius']
        
        self.turn = data['turn']