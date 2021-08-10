from game.common.enums import *


class Action:
    def __init__(self):
        self.object_type = ObjectType.action
        self._chosen_action = ActionType.none

    def set_action(self, act):
        if act in [ActionType.none, ActionType.move, ActionType.shoot, ActionType.interact_with_map,
                   ActionType.reload_weapon, ActionType.shop]:
            self._chosen_action = act

    def to_json(self):
        data = dict()
        data['object_type'] = self.object_type

        return data

    def from_json(self, data):
        self.object_type = data['object_type']
        self._example_action = data['example_action']
        return self

    def __str__(self):
        outstring = ''

        return outstring
