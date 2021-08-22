from game.common.enums import *


class Action:
    def __init__(self):
        self.object_type = ObjectType.action
        self._chosen_action = ActionType.none

    def set_action(self, act):

        if isinstance(act, int) and act in ActionType.__dict__.values():
            #if act in [ActionType.none, ActionType.move, ActionType.shoot, ActionType.pickup_item,
                       #ActionType.reload_weapon, ActionType.shop, ActionType.use_item]:
            self.chosen_action = act

    def to_json(self):
        data = dict()
        data['object_type'] = self.object_type

        return data

    def from_json(self, data):
        self.object_type = data['object_type']
        return self


    def __str__(self):
        outstring = ''

        return outstring
