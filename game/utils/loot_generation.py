import random
from game.common.stats import GameStats

def generate_chunk(level, density):
    for i in range(random.randint(1, GameStats.density_constant * density)):
        
    # use higher level loot to try to force a winner by making it easier to kill
    # take chunk density from stats and create a representation of the loot