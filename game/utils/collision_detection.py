from game.common.hitbox import Hitbox
from game.common.stats import GameStats
from game.common.enums import *

def checkCollision(hitbox_one, hitbox_two):
    if (hitbox_one.topLeft[0] < hitbox_two.topRight[0] and 
            hitbox_one.topRight[0] > hitbox_two.topLeft[0] and 
            hitbox_one.topLeft[1] < hitbox_two.bottomLeft[1] and 
            hitbox_one.bottomRight[1] > hitbox_two.topRight[1]):
        
        # if (RectA.X1 < RectB.X2 && RectA.X2 > RectB.X1 &&
   # RectA.Y1 < RectB.Y2 && RectA.Y2 > RectB.Y1) 
        return True
    else:
        return False
  
