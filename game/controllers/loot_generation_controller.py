import random
from game.controllers.controller import Controller
from game.common.stats import GameStats
from game.utils.item_gen_utils import place_items


class LootGenerationController(Controller):

    def __init__(self):
         # self.ticks_between_waves (var in game stats) and self.tick must be equal to each other
        self.tick = 200
        self.next_wave = 1

    def handle_actions(self, game_board, kill_boundary_radius):
        if (self.tick % GameStats.ticks_between_waves) == 0 and self.next_wave <= GameStats.num_loot_waves:
            # As more waves spawn, there will be less items per wave
            number_items = random.randrange(20 - (self.next_wave * 2), 35 - (self.next_wave * 2), 1)
            items = place_items(game_board, self.next_wave, kill_boundary_radius, number_items)
            game_board.partition.add_object_list(items)
            self.next_wave += 1
        self.tick += 1
