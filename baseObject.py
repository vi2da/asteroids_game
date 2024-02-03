from turtle import RawTurtle

class BaseObject(RawTurtle):
    """
    This class represents our standard object in the game.
    All of your classes (ship,asteroid,torpedo) should inherit from this class.
    """


    def __init__(self,canvas,x,y,speedX,speedY,shape,direction=None,rad=1):
        """
        To instanciate a class that inherits from BaseObject you must call in the
        first line of you __init__ function to:
        super().__init__(<params>) where the parameters are explained below:

        :param canvas: The canvas on which we should draw our object.
        :type canvas: Turtle.ScrolledCanvas
        :param x: The x coordinate of the object.
        :type x: int
        :param y: The y coordinate of the object.
        :type y: int
        :param xSpeed: The current speed on the x direction.
        :type xSpeed: int
        :param ySpeed: The current speed on the y direction.
        :type ySpeed: int
        :param shape: The shape of the object, should be taken from the module objectShapes.
        :type shape: str
        :param direction: The direction (in degrees) we are currently heading.
        :type shape: int
        :param shape: The radius of the object.
        :type shape: int
        """
        super().__init__(canvas)
        self.penup()
        self.goto(x,y)
        self._xPos = x
        self._yPos = y
        if direction:
            self.setheading(direction)

        self.dx = speedX
        self.dy = speedY
        self._radius = rad
        self.shape(shape)

    def set_color(self,clr):
        """
        Sets the object color to the provided clr value

        :param clr: A string specifying the color
        :type clr: str
        """
        self.color(clr)

    def get_radius(self):
        """
        Returns the radius of the object
        """
        return self._radius

    def get_speed_x(self):
        """
        Returns current speed on the x direction.
        """
        return self.dx

    def get_speed_y(self):
        """
        Returns current speed on the y direction.
        """
        return self.dy

    def set_speed_x(self,speedX):
        """
        Sets the current speed on the x direction.

        :param speedX: The speed to set.
        :type speedX: int
        """
        self.dx = speedX

    def set_speed_y(self,speedY):
        """
        Sets the current speed on the y direction.

        :param speedY: The speed to set.
        :type speedY: int
        """
        self.dy = speedY

    def get_x_cor(self):
        """
        Returns current x coordinate.
        """
        return self._xPos

    def get_y_cor(self):
        """
        Returns current y coordinate.
        """
        return self._yPos

    def move(self,x,y):
        """
        Moves the object to the specified (x,y) coordinate.

        :param x: The x coordinate.
        :type x: int
        :param y: The y coordinate.
        :type y: int
        """
        #screen = self.getscreen()
        self.goto(x,y)
        self._xPos = x
        self._yPos = y

    def get_angle(self):
        """
        Returns current angle.
        """
        return self.heading()

    def increase_angle(self):
        """
        Increases the angle of our spaceship by 7 degrees.
        """
        self.setheading(self.get_angle()+7)

    def decrease_angle(self):
        """
        Decreases the angle of our spaceship by 7 degrees.
        """
        self.setheading(self.get_angle()-7)
