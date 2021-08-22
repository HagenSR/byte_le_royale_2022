from game.common.game_board import GameBoard
from game.common.hitbox import Hitbox
from game.common.stats import GameStats
from game.controllers.controller import Controller
import math


class KillBoundaryController(Controller):
    # Determine damage to player based on distance from edge of circle
    # If distance to center > Current size
    # damage = player_distance - current_radius
    def handle_actions(self, client, radius):
        shooter = client.shooter
        player_distance = math.sqrt(
            (((GameStats.game_board_width / 2) - shooter.hitbox.middle[0]) ** 2) +
            (((GameStats.game_board_height / 2) - shooter.hitbox.middle[1]) ** 2)
        )
        if player_distance > radius:
            shooter.health -= GameStats.circle_damage
