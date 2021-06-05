# temp class to be able to use Upgrade before it's made
from game.common.enums import *
from game.common.items.item import Item


class Upgrade(Item):
    def __init__(self):
        super().__init__(None, None)

