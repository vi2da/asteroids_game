from baseObject import BaseObject
import math
from objectShapes import SHIP_SHAPE

class SpaceShip(BaseObject):
    def __init__(self,canvas,x,y,dx,dy):
        super().__init__(canvas,x,y,dx,dy,SHIP_SHAPE)
        self.set_color("purple")
