import unittest
from game.controllers.grenade_controller import *
from game.common.moving.damaging.grenade import Grenade
from game.common.wall import Wall
from game.common.moving.shooter import Shooter
from game.common.game_board import GameBoard
from game.common.player import Player
from game.common.items.money import Money


class TestGrenadeController(unittest.TestCase):
    def setUp(self):
        self.gCont = GrenadeController()

    def test_grenade_damages_object(self):
        wall = Wall(Hitbox(100, 100, (399, 399)), 1000)
        player = Player(shooter=Shooter(0, 0, Hitbox(10, 10, (380, 450))))
        player.action.set_action(ActionType.throw_grenade)
        grenade = Grenade(
            hitbox=Hitbox(
                5,
                5,
                (player.shooter.hitbox.position[0],
                 player.shooter.hitbox.position[1])),
            health=10,
            fuse_time=10,
            damage=50)
        player.shooter.grenade_distance = 50
        player.shooter.append_inventory(grenade)
        game_board = GameBoard()
        game_board.partition.add_object(wall)
        game_board.partition.add_object(player.shooter)
        wall_start_health = wall.health
        for i in range(20):
            self.gCont.handle_actions(player, game_board)
        self.assertEqual(wall.health, wall_start_health - grenade.damage)

    def test_grenade_fuse(self):
        wall = Wall(Hitbox(100, 100, (399, 399)), 1000)
        player = Player(shooter=Shooter(0, 0, Hitbox(10, 10, (380, 450))))
        player.action.set_action(ActionType.throw_grenade)
        grenade = Grenade(hitbox=Hitbox(5, 5, (player.shooter.hitbox.position[0], player.shooter.hitbox.position[1])),
                          health=10, fuse_time=10, damage=50)
        player.shooter.grenade_distance = 50
        player.shooter.append_inventory(grenade)
        game_board = GameBoard()
        game_board.partition.add_object(wall)
        game_board.partition.add_object(player.shooter)
        wall_start_health = wall.health
        for i in range(5):
            self.gCont.handle_actions(player, game_board)
        self.assertEqual(wall.health, wall_start_health)

    def test_no_health_object(self):
        money = Money(Hitbox(100, 100, (399, 399)), health=None)
        player = Player(shooter=Shooter(0, 0, Hitbox(10, 10, (380, 450))))
        player.action.set_action(ActionType.throw_grenade)
        grenade = Grenade(hitbox=Hitbox(5, 5, (player.shooter.hitbox.position[0], player.shooter.hitbox.position[1])),
                          health=10, fuse_time=10, damage=50)
        player.shooter.grenade_distance = 50
        player.shooter.append_inventory(grenade)
        game_board = GameBoard()
        game_board.partition.add_object(money)
        game_board.partition.add_object(player.shooter)
        money_start_health = money.health
        for i in range(20):
            self.gCont.handle_actions(player, game_board)
        self.assertEqual(money.health, money_start_health)

    def test_no_collisions(self):
        player = Player(shooter=Shooter(0, 0, Hitbox(10, 10, (380, 450))))
        player.action.set_action(ActionType.throw_grenade)
        grenade = Grenade(hitbox=Hitbox(5, 5, (player.shooter.hitbox.position[0], player.shooter.hitbox.position[1])),
                          health=10, fuse_time=10, damage=50)
        player.shooter.grenade_distance = 50
        player.shooter.append_inventory(grenade)
        game_board = GameBoard()
        game_board.partition.add_object(player.shooter)
        start_health = player.shooter.health
        for i in range(20):
            self.gCont.handle_actions(player, game_board)
        self.assertEqual(player.shooter.health, start_health)

    def test_throw_beyond_map(self):
        player = Player(shooter=Shooter(0, 0, Hitbox(10, 10, (490, 490))))
        player.action.set_action(ActionType.throw_grenade)
        grenade = Grenade(hitbox=Hitbox(5, 5, (player.shooter.hitbox.position[0], player.shooter.hitbox.position[1])),
                          health=10, fuse_time=10, damage=5)
        player.shooter.grenade_distance = 50
        player.shooter.append_inventory(grenade)
        game_board = GameBoard()
        game_board.partition.add_object(player.shooter)
        start_health = player.shooter.health
        for i in range(20):
            self.gCont.handle_actions(player, game_board)
        self.assertEqual(player.shooter.health, start_health - grenade.damage)


if __name__ == '__main__':
    unittest.main()
