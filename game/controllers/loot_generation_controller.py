import random
from game.controllers.controller import Controller
from game.common.stats import GameStats
from game.utils.item_gen_utils import placeItems


class LootGenerationController(Controller):
    
    def set_up(self):
        self.num_loot_waves = 4
        self.next_wave = 1
        # self.ticks_between_waves and self.tick must be equal to each other
        self.ticks_between_waves = 200
        self.tick = 200

    def handle_actions(self, game_board, kill_boundry_radius):
        if (self.tick % 200) == 0 and self.next_wave <= self.num_loot_waves:
            number_items = random.randrange(20 - (self.next_wave * 2), 35 - (self.next_wave * 2), 1)
            placeItems(game_board, self.next_wave, kill_boundry_radius, number_items)