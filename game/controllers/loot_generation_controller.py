import random
from game.controllers.controller import Controller
from game.common.stats import GameStats
from game.utils.item_gen_utils import placeItems


class LootGenerationController(Controller):

    def handle_actions(self, game_board, curr_tick, kill_boundry_radius):
        if curr_tick is GameStats.initial_wave:
            number_items = random.randrange(10, 30, 1)
            placeItems(game_board, 1, kill_boundry_radius, number_items)
        if curr_tick is GameStats.loot_wave_1_tick:
            number_items = random.randrange(10, 20, 1)
            placeItems(game_board, 2, kill_boundry_radius, number_items)
        if curr_tick is GameStats.loot_wave_2_tick:
            number_items = random.randrange(5, 15, 1)
            placeItems(game_board, 3, kill_boundry_radius, number_items)
        if curr_tick is GameStats.loot_wave_3_tick:
            number_items = random.randrange(5, 10, 1)
            placeItems(game_board, 4, kill_boundry_radius, number_items)