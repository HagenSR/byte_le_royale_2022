import time
import unittest
from game.controllers.teleporter_controller import TeleporterController
from game.utils.generate_game import *
from game.common.stats import GameStats
from game.common.moving.shooter import Shooter
from game.common.player import Player
from game.common.action import Action


class TestTeleporterController(unittest.TestCase):

    def setUp(self):
        # generate()
        # Based on the moste recentely generated game map
        with open('./logs/game_map.json') as fl:
            self.gameboard = GameBoard()
            obj = json.load(fl)['game_map']
            self.gameboard = self.gameboard.from_json(obj)

    def test_teleporters_generate(self):
        game_board = self.gameboard
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

    def test_players_teleport(self):
        shooter = Shooter(hitbox=Hitbox(10, 10, (5, 5)))
        player = Player(action=Action(), shooter=shooter)
        player.action._chosen_action = ActionType.use_teleporter
        tel_one = Teleporter(hitbox=Hitbox(10, 10, (5, 5)))
        tel_two = Teleporter(hitbox=Hitbox(10, 10, (20, 20)))
        local_game_board = GameBoard()
        local_game_board.partition.add_object(player.shooter)
        local_game_board.partition.add_object(tel_one)
        local_game_board.partition.add_object(tel_two)
        tel_controller = TeleporterController(local_game_board)
        tel_controller.handle_actions(player)
        self.assertEqual(shooter.hitbox.position, tel_two.hitbox.position)

    def test_player_spam_teleport(self):
        shooter = Shooter(hitbox=Hitbox(10, 10, (5, 5)))
        player = Player(action=Action(), shooter=shooter)
        player.action._chosen_action = ActionType.use_teleporter
        tel_one = Teleporter(hitbox=Hitbox(10, 10, (5, 5)))
        tel_two = Teleporter(hitbox=Hitbox(10, 10, (20, 20)))
        local_game_board = GameBoard()
        local_game_board.partition.add_object(player.shooter)
        local_game_board.partition.add_object(tel_one)
        local_game_board.partition.add_object(tel_two)
        tel_controller = TeleporterController(local_game_board)
        tel_controller.handle_actions(player)
        tel_controller.handle_actions(player)
        self.assertEqual(shooter.hitbox.position, tel_two.hitbox.position)

    def test_cooldown_works(self):
        shooter = Shooter(hitbox=Hitbox(10, 10, (5, 5)))
        player = Player(action=Action(), shooter=shooter)
        player.action._chosen_action = ActionType.use_teleporter
        tel_one = Teleporter(hitbox=Hitbox(10, 10, (5, 5)), turn_cooldown=5)
        tel_two = Teleporter(hitbox=Hitbox(10, 10, (20, 20)), turn_cooldown=5)
        local_game_board = GameBoard()
        local_game_board.partition.add_object(player.shooter)
        local_game_board.partition.add_object(tel_one)
        local_game_board.partition.add_object(tel_two)
        tel_controller = TeleporterController(local_game_board)
        tel_controller.handle_actions(player)
        player.action._chosen_action = ActionType.none
        for i in range(6):
            tel_controller.handle_actions(player)
        player.action._chosen_action = ActionType.use_teleporter
        tel_controller.handle_actions(player)
        self.assertEqual(shooter.hitbox.position, tel_one.hitbox.position)


if __name__ == '__main__':
    unittest.main()
