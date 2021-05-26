
from game.common.map_object import MapObject


class walls(MapObject):
    def __init__(self, health = None, destructable = None):
        super.__init__()
        self.health = health
        self.destructable = destructable
        
    def to_json(self):
        data = super().to_json()
        
        data['health'] = self.health
        data['destructable'] = self.destructable
        
        return data
    
    def from_json(self, data):
        super().from_json(data)
        
        self.health = data['health']
        self.destructable = data['destructable']
    
        