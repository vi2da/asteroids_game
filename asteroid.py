from baseObject import BaseObject
from objectShapes import ASTEROID_BASE_SHAPE

class Asteroid(BaseObject):
    def __init__(self, canvas, x, y, dx, dy, size, index):
        super().__init__(canvas,x,y,dx,dy,ASTEROID_BASE_SHAPE + str(size))
        self.size = size
    
    def get_size(self):
        return self.size

    def get_radius(self):
        return self.size * 10 - 5
