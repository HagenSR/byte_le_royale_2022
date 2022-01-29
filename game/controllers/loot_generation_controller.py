import random
from game.controllers.controller import Controller
from game.common.stats import GameStats
from game.utils.item_gen_utils import ItemGenUtils


class LootGenerationController(Controller):

    def __init__(self):
        super().__init__()
        # self.ticks_between_waves (var in game stats) and self.tick must be
        # equal to each other
        self.tick = 0
        self.next_wave = 1
        self.item_gen_utils = ItemGenUtils()
        self.uuids = []

    def handle_actions(self, game_board):
        if (self.tick % GameStats.ticks_between_waves) == 0 and self.next_wave <= GameStats.num_loot_waves:
            self.item_gen_utils.remove_items_from_map(game_board.partition)
            # As more waves spawn, there will be less items per wave
            number_items = random.randrange(
                200 - (self.next_wave * 20), 350 - (self.next_wave * 20), 1)
            for i in range(number_items):
                item = self.item_gen_utils.place_item(
                    game_board, self.next_wave)
                if item is None:
                    continue
                if item.id in self.uuids:
                    print("ARG")
                self.uuids.append(item.id)
                game_board.partition.add_object(item)
            self.next_wave += 1
        self.tick += 1
