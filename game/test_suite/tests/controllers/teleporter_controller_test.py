import time
import unittest
from game.controllers.teleporter_controller import TeleporterController
from game.utils.generate_game import *
from game.common.stats import GameStats
from game.common.moving.shooter import Shooter
from game.common.player import Player
from game.common.action import Action


class TestTeleporterController(unittest.TestCase):

    def test_teleporters_generate(self):
        teleporter_list = TeleporterController.game_board_teleporters(self)
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
        tel_controller = TeleporterController()
        shooter = Shooter(hitbox=tel_controller.teleporter_list[0].hitbox)
        player = Player(shooter=shooter)
        player.action._chosen_action = ActionType.use_teleporter
        start_tel = tel_controller.teleporter_list[0]
        tel_controller.handle_actions(player)
        tel_controller.teleporter_list.remove(start_tel)
        self.assertIn(shooter.hitbox.position,
                      [teleporter.hitbox.position for teleporter in tel_controller.teleporter_list])

    def test_player_spam_teleport(self):
        tel_controller = TeleporterController()
        shooter = Shooter(hitbox=tel_controller.teleporter_list[0].hitbox)
        player = Player(shooter=shooter)
        player.action._chosen_action = ActionType.use_teleporter
        tel_controller.handle_actions(player)
        new_position = player.shooter.hitbox.position
        tel_controller.handle_actions(player)
        self.assertEqual(player.shooter.hitbox.position, new_position)

    def test_cooldown_works(self):
        tel_controller = TeleporterController()
        shooter = Shooter(hitbox=tel_controller.teleporter_list[0].hitbox)
        player = Player(shooter=shooter)
        player.action._chosen_action = ActionType.use_teleporter
        tel_controller.handle_actions(player)
        cooldown_tel_position = player.shooter.hitbox.position
        for i in range(8):
            tel_controller.handle_actions(player)
        self.assertNotEqual(player.shooter.hitbox.position, cooldown_tel_position)


if __name__ == '__main__':
    unittest.main()
