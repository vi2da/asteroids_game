import math
from baseObject import BaseObject
from objectShapes import TORPEDO_SHAPE

class PhotonTorpedo(BaseObject):
    
    RADIUS = 4
    TORPEDO_LIFESPAN = 200
    
    def __init__(self,canvas,x,y,dx,dy,direction):
        super().__init__(canvas,x,y,dx,dy,TORPEDO_SHAPE,direction,PhotonTorpedo.RADIUS)
        self.set_color("Green")
        self.lifespan = PhotonTorpedo.TORPEDO_LIFESPAN 

    def get_life_span(self):
        return self.lifespan

    def move(self,x,y):
        self.lifespan = self.lifespan - 1
        super().move(x,y)
