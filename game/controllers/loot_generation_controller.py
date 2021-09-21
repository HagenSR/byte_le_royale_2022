import random
from game.controllers.controller import Controller
from game.common.stats import GameStats
from game.utils.item_gen_utils import place_items


class LootGenerationController(Controller):

    def handle_actions(self, game_board, kill_boundary_radius):
        if (GameStats.tick % GameStats.ticks_between_waves) == 0 and GameStats.next_wave <= GameStats.num_loot_waves:
            # As more waves spawn, there will be less items per wave
            number_items = random.randrange(20 - (GameStats.next_wave * 2), 35 - (GameStats.next_wave * 2), 1)
            items = place_items(game_board, GameStats.next_wave, kill_boundary_radius, number_items)
            game_board.partition.add_object_list(items)
            GameStats.next_wave += 1
        GameStats.tick += 1
