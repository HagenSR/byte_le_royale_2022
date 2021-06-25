import unittest 
from game.common.hitbox import Hitbox
from game.utils.collision_detection import checkCollision

class TestCollision(unittest.TestCase):
    
    def setUp(self):
       self.hitOne = Hitbox(10,10,(5,5))
       self.hitTwo = Hitbox(25,25,(10,10))

    
    def test_collision_true(self):
        self.hitOne.position = (5.0,5.0)
        self.hitOne.height = 5
        self.hitOne.width = 8
  
        self.hitTwo.position = (5.0,6.0)
        self.hitTwo.height = 5
        self.hitTwo.width = 8


        self.assertTrue(checkCollision(self.hitOne,self.hitTwo))
    
    print(hitOne.topLeft)

    def test_collision_false(self):
        self.hitOne.position = (5,5)
        self.hitOne.height = 5
        self.hitOne.width = 8

        self.hitTwo.position = (20,20)
        self.hitTwo.height = 5
        self.hitTwo.width = 8

        self.assertFalse(checkCollision(self.hitOne,self.hitTwo))

if __name__ == '__main__':
     unittest.main 