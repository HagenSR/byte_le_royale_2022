import unittest
from game.controllers.teleporter_controller import TeleporterController
from game.utils.generate_game import *
from game.common.stats import GameStats


class TestTeleporterController(unittest.TestCase):

    def setUp(self):
        # generate()
        # Based on the moste recentely generated game map
        with open('./logs/game_map.json') as fl:
            self.gameboard = GameBoard()
            obj = json.load(fl)['game_map']
            for thing in obj:
                print(type(thing))
            self.gameboard = self.gameboard.from_json(obj)

    def test_teleporters_generate(self):
        game_board = self.gameboard
        print(game_board.partition.get_partition_objects(250, 250))
        teleporter_list = TeleporterController.game_board_teleporters(self, game_board = game_board)
        flag = False
        corridor_size = GameStats.corridor_width_height
        plot_size = GameStats.plot_width_height
        for teleporter in teleporter_list:
            x_pos = teleporter.hitbox.position[0]
            y_pos = teleporter.hitbox.position[1]
            # Validate that (X,Y) position is in a corridor area, not building area
            if 0 <= x_pos <= corridor_size\
                or corridor_size + plot_size <= x_pos <= corridor_size * 2 + plot_size\
                or corridor_size * 2 + plot_size * 2 <= x_pos <= corridor_size * 3 + plot_size * 2\
                or corridor_size * 3 + plot_size * 3 <= x_pos <= GameStats.game_board_width\
                and \
                    0 <= y_pos <= corridor_size\
                or corridor_size + plot_size <= y_pos <= corridor_size * 2 + plot_size \
                or corridor_size * 2 + plot_size * 2 <= y_pos <= corridor_size * 3 + plot_size * 2 \
                or corridor_size * 3 + plot_size * 3 <= y_pos <= GameStats.game_board_width:
                flag = True
            else:
                flag = False
                break
        self.assertTrue(flag)




if __name__ == '__main__':
    unittest.main()
