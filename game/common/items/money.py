from random import randint
from game.common.enums import *
from game.common.items.item import Item
from game.common.stats import GameStats


class Money(Item):

    def __init__(
            self,
            hitbox,
            health,
            count):
        super().__init__(hitbox, health, count)
        self.object_type = ObjectType.money
        self.amount = randint(GameStats.min_money_amount, GameStats.max_money_amount)

    def to_json(self):
        data = super().to_json()
        data['amount'] = self.amount
        return data

    def from_json(self, data):
        super().from_json(data)
        self.amount = data['amount']
        return self
