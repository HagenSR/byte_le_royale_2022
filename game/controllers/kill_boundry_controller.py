from game.common.game_board import GameBoard
from game.common.hitbox import Hitbox
from game.common.stats import GameStats
from game.controllers.controller import Controller
import math


class KillBoundryController(Controller):
    # Determine damage to player based on distance from edge of circle
    # If distance to center > Current size
    # damage = player_distance - current_radius
    def handle_actions(self, client, radius):
        shooter = client.shooter
        self.player_distance = math.sqrt(
            ((GameBoard.width / 2) - Hitbox.middle[0]) ** 2 + (
                (GameBoard.height / 2) - Hitbox.middle[1]) ** 2)
        if self.player_distance > radius:
            shooter.Health = shooter.Health - GameStats.circle_damage
