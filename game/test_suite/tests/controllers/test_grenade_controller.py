import unittest
from game.controllers.grenade_controller import *
from game.common.moving.damaging.grenade import Grenade
from game.common.wall import Wall
from game.common.moving.shooter import Shooter
from game.common.game_board import GameBoard
from game.common.player import Player


class TestGrenadeController(unittest.TestCase):
    def setUp(self):
        self.gCont = GrenadeController()

    def test_grenade_damages_object(self):
        wall = Wall(Hitbox(100, 100, (400, 400)), 1000)
        player = Player(shooter = Shooter(0, 0, Hitbox(10, 10, (380, 450))))
        player.action.set_action(ActionType.throw_grenade)
        grenade = Grenade(hitbox=Hitbox(5,5,(player.shooter.hitbox.position[0], player.shooter.hitbox.position[1])), health=10, fuse_time=10, damage=50)
        player.shooter.grenade_distance = 50
        player.shooter.append_inventory(grenade)
        game_board = GameBoard()
        game_board.partition.add_object(wall)
        game_board.partition.add_object(player.shooter)
        wall_start_health = wall.health
        for i in range(20):
            #breakpoint()
            self.gCont.handle_actions(player, game_board)
        self.assertTrue(wall.health == wall_start_health - grenade.damage)


if __name__ == '__main__':
    unittest.main()
