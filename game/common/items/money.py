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


<< << << < HEAD
   self.__amount = randint(
    GameStats.min_money_amount,
     GameStats.max_money_amount)
== == == =
   self._amount = randint(
        GameStats.min_money_amount,
        GameStats.max_money_amount)
>>>>>> > 4902036bf800b3063f693cf800436ced3f934852

   def get_amount(self):
        return self.__amount

    def to_json(self):
        data = super().to_json()
        data['amount'] = self.amount
        return data

    def from_json(self, data):
        super().from_json(data)
        self.amount = data['amount']
        return self
