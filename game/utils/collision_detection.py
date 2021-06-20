from game.common.hitbox import Hitbox
from game.common.stats import GameStats
from game.common.enums import *

checkCollision(hitbox_one, hitbox_two):
    if (hitbox_one.topLeft[0] < hitbox_two.topRight[0] and hitbox_one.topRight[0] > hitbox_two.topLeft[0]
        and hitbox_one.bottomLeft[1] < hitbox_two.bottomLeft[1] 
        and hitbox_one.bottomRight[1] > hitbox_two.bottomRight[1]):
        return False
    else:
        return True 
    #RectA.X1 < RectB.X2 && RectA.X2 > RectB.X1 && RectA.Y1 < RectB.Y2 && RectA.Y2 > RectB.Y1

    #Cond1. If A's left edge is to the right of the B's right edge, - then A is Totally to right Of B
    #Cond2. If A's right edge is to the left of the B's left edge, - then A is Totally to left Of B
    #Cond3. If A's top edge is below B's bottom edge, - then A is Totally below B
    #Cond4. If A's bottom edge is above B's top edge, - then A is Totally above B
    #So condition for Non-Overlap is #Cond1 Or Cond2 Or Cond3 Or Cond4 

 