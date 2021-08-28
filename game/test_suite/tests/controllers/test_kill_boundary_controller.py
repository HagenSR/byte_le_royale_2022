import unittest
from game.common.stats import GameStats
from game.common.hitbox import Hitbox
from game.common.player import Player
from game.common.moving.shooter import Shooter
from game.controllers.kill_boundary_controller import KillBoundaryController


class TestKillBoundary(unittest.TestCase):

    def setUp(self):
        self.killBoundaryControl = KillBoundaryController()
        self.players = [Player(shooter=Shooter(0, 0, Hitbox(10, 10, (0, 0))))]

    def test_within_radius(self):
        self.killBoundaryControl.handle_actions(self.players, 1000)
        self.assertEqual(
            self.players[0].shooter.health,
            GameStats.player_stats["starting_health"])

    def test_outside_radius(self):
        self.killBoundaryControl.handle_actions(self.players, 0)
        self.assertEqual(
            self.players[0].shooter.health,
            GameStats.player_stats["starting_health"] -
            GameStats.circle_damage)

    def test_inside_close(self):
        middle_x = GameStats.game_board_width / 2
        middle_y = GameStats.game_board_height / 2
        self.players[0].shooter.hitbox.position = (middle_x, middle_y)
        self.killBoundaryControl.handle_actions(self.players, 10)
        self.assertEqual(
            self.players[0].shooter.health,
            GameStats.player_stats["starting_health"])

    def test_outside_close(self):
        middle_x = (GameStats.game_board_width / 2) + 5
        middle_y = (GameStats.game_board_height / 2) + 5
        self.players[0].shooter.hitbox.position = (middle_x, middle_y)
        self.killBoundaryControl.handle_actions(self.players, 10)
        self.assertEqual(
            self.players[0].shooter.health,
            GameStats.player_stats["starting_health"] -
            GameStats.circle_damage)


if __name__ == '__main__':
    unittest.main
