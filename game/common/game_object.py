import uuid

from game.common.enums import ObjectType


class GameObject:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.object_type = ObjectType.none

    def to_json(self):
        # It is recommended call this using super() in child implementations
        data = dict()

        data['id'] = self.id
        data['object_type'] = self.object_type

        return data

    def from_json(self, data):
        # It is recommended call this using super() in child implementations
        self.id = data['id']
        self.object_type = data['object_type']

    def obfuscate(self):
        pass
