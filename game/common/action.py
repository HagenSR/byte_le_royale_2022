from game.common.enums import *


class Action:
    def __init__(self):
        self.object_type = ObjectType.action
        self._chosen_action = None
        self.selected_object = None
        self.action_parameter = None

    def set_action(self, action):
        self._chosen_action = action

    def select_object(self, obj):
        if isinstance(obj, int) and obj in Consumables.__dict__.values():
            # if act in [ActionType.none, ActionType.move, ActionType.shoot, ActionType.pickup_item,
            # ActionType.reload_weapon, ActionType.shop, ActionType.use_item]:
            self.selected_object = obj
        else:
            raise ValueError(
                "value entered does not retrieve consumable enum.")

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
