from game.common.enums import *


class Action:
    def __init__(self):
        self.object_type = ObjectType.action
        self._example_action = None

    def set_action(self, action):
        self._example_action = action

    def to_json(self):
        data = dict()

        data['object_type'] = self.object_type
        data['example_action'] = self._example_action

        return data

    def from_json(self, data):
        self.object_type = data['object_type']
        self._example_action = data['example_action']
        return self

    def __str__(self):
        outstring = ''
        outstring += f'Example Action: {self._example_action}\n'

        return outstring
