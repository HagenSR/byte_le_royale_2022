from game.common.enums import *
from game.common.items.consumable import Consumable


class Action:
    def __init__(self):
        self.object_type = ObjectType.action

        # _chosen_action should be set using the ActionType enum
        self._chosen_action = None

        # these should be set using the Consumables enum
        self.item_to_purchase = None
        self.item_to_use = None

        self.heading = 0
        self.speed = 0

    @property
    def heading(self):
        return self.__heading

    @heading.setter
    def heading(self, heading):
        if not isinstance(heading, int):
            raise ValueError(f"Heading is type {type(heading)} must be of type int")
        self.__heading = heading

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, speed):
        if not isinstance(speed, int):
            raise ValueError(f"Speed is type {type(speed)} must be of type int")
        self.__speed = speed

    def set_action(self, act: int):
        """Sets a general action. NOTE: For actions that require additional data,
        please use other methods in action object"""
        if not isinstance(act, int) or act not in ActionType.__dict__.values():
            raise ValueError("Values passed to action object methods must be of correct type")
        self._chosen_action = act

    def set_move(self, heading: int, speed: int):
        """Sets movement intent and parameters"""
        if not isinstance(heading, int) or not isinstance(speed, int):
            raise ValueError("Values passed to action object methods must be of correct type")
        self._chosen_action = ActionType.move
        self.heading = heading
        self.speed = speed

    def set_shoot(self, heading: int):
        if not isinstance(heading, int):
            raise ValueError("Values passed to action object methods must be of correct type")
        self._chosen_action = ActionType.shoot
        self.heading = heading

    def select_item_to_buy(self, obj):
        """Sets item to buy from shop"""
        if not isinstance(obj, int) and obj in Consumables.__dict__.values():
            raise ValueError("Values passed to action object methods must be of correct type")
        self.item_to_purchase = obj

    def select_item_to_use(self, obj):
        """Sets item to use and action to use. Must be same object reference as is in player inventory"""
        if not isinstance(obj, Consumable):
            raise ValueError("Values passed to action object methods must be of correct type")
        self._chosen_action = ActionType.use
        self.item_to_use = obj

    def to_json(self):
        data = dict()
        data['object_type'] = self.object_type
        data['chosen_action'] = self._chosen_action

        return data

    def from_json(self, data):
        self.object_type = data['object_type']
        self._chosen_action = data['chosen_action']

        return self

    def __str__(self):
        outstring = ''
        outstring += f'Chosen Action: {self._chosen_action}\n'
        return outstring
