ASTEROID_BASE_SHAPE = "asteroid"
SHIP_SHAPE = "ship"
TORPEDO_SHAPE = "torpedo"

class ShapesMaster:
    ASTEROIDS_TYPES = 3

    ASTEROID_3_LAYOUT = ((-20, -16),(-21, 0), (-20,18),(0,27),(17,15),
                            (25,0),(16,-15),(0,-21))

    ASTEROID_2_LAYOUT = ((-15, -10),(-16, 0), (-13,12),(0,19),(12,10),
                            (20,0),(12,-10),(0,-13))

    ASTEROID_1_LAYOUT = ((-10,-5),(-12,0),(-8,8),(0,13),(8,6),(14,0),(12,0),(8,-6),(0,-7))

    ASTEROIDS_LAYOUTS = [ASTEROID_1_LAYOUT, ASTEROID_2_LAYOUT, ASTEROID_3_LAYOUT]

    SHIP_LAYOUT = ((-10,-10),(0,-5),(10,-10),(0,10))

    TORPEDO_LAYOUT = ((-2,-4),(-2,4),(2,4),(2,-4))

    def __init__(self, screen):
        """
        This initializes the shapes controller, the screen passed is the screen
        controling the game, you should not call this method anywhere in your
        code.
        """
        self.screen = screen
        self._shapes = {}
        self._updated = False
        self._add_base_shapes()

    def add_shape(self,name,cords,override = False):
        if override or name not in self._shapes:
            self._shapes[name] = cords
            self.screen.register_shape(name,cords)

    def _add_base_shapes(self):
        for i in range(ShapesMaster.ASTEROIDS_TYPES):
            self.add_shape(ASTEROID_BASE_SHAPE+str(i+1), \
                        ShapesMaster.ASTEROIDS_LAYOUTS[i])

        self.add_shape(SHIP_SHAPE, ShapesMaster.SHIP_LAYOUT)
        self.add_shape(TORPEDO_SHAPE, ShapesMaster.TORPEDO_LAYOUT)

    def get_shapes_dict(self):
        """
        Returns a dictionary of all the shapes in the game in the format of
        (name, coordinates).
        You have no reason of calling this method anywhere in your code...
        """
        return self._shapes
