from game.common.map_object import MapObject

class Item(MapObject):
    def __init__(self, coordinates, hitbox, health=None, count = 1):
        super().__init__(health, coordinates, hitbox, True)
        self.object_type = ObjectType.item
        self.count = count
    
    def to_json(self):
        data = super().to_json()
        data['count'] = self.count
        return data

    def from_json(self, data):
        super().from_json(data)
        self.count = data['count']
