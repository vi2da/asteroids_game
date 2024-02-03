from turtle import *
import tkinter.messagebox
import tkinter
import random
import math
import datetime

from originalGame import *
from torpedo import *
from asteroid import *
from spaceship import *

from objectShapes import ShapesMaster, SHIP_SHAPE

class GameMaster:

    """
    This holds all of the state in the game, including methods to help accessing
    and modifying members (such as torpedos, asteroids etc.)

    You need to instantiate it only onec throughout -
    **This was already done for you, look at the asteroidsMain.py file**

    To control the game you can use your keyboard controllers like so:

    "Left", "Right","Up" - Movement

    " " -(space key) Fire a torpedo

    "q" - Quit the game
    """
    def __init__(self):
        """
        Initializes all of the containers needed for this class to work.
        """
        self.asteroids = []
        self.torpedos = []

        self._upClicks = 0
        self._downClicks = 0
        self._leftClicks = 0
        self._rightClicks = 0
        self._fireClicks = 0
        self._astroidIndex = 0
        self._endGame = False

        self.__screenMinX = -500
        self.__screenMinY = -500
        self.__screenMaxX = 500
        self.__screenMaxY = 500

        self._originalGame = OriginalGame(self)
        self._init_graphics()
        self._bind_keys()
        self.screen.listen()

    def _init_graphics(self):
        self._root = tkinter.Tk()
        self._root.title("Asteroids!")
        self._cv = ScrolledCanvas(self._root,600,600,600,600)
        self._cv.pack(side = tkinter.LEFT)
        self._t = RawTurtle(self._cv)

        self.screen = self._t.getscreen()
        self.screen.setworldcoordinates(
                                        self.get_screen_min_x(),
                                        self.get_screen_min_y(),
                                        self.get_screen_max_x(),
                                        self.get_screen_max_y()
                                        )
        self._shapeMaster = ShapesMaster(self.screen)
        shapes = self._shapeMaster.get_shapes_dict()

        frame = tkinter.Frame(self._root)
        frame.pack(side = tkinter.RIGHT,fill=tkinter.BOTH)

        # add scores frame
        self.scoreVal = tkinter.StringVar()
        self.scoreVal.set("0")
        scoreTitle = tkinter.Label(frame,text="Score")
        scoreTitle.pack()
        scoreFrame = tkinter.Frame(frame,height=2, bd=1, \
            relief=tkinter.SUNKEN)
        scoreFrame.pack()
        score = tkinter.Label(scoreFrame,height=2,width=20,\
            textvariable=self.scoreVal,fg="Yellow",bg="black")

        ################

        score.pack()

        # Add Lives Frame
        livesTitle = tkinter.Label(frame, \
           text="Extra Lives Remaining")
        livesTitle.pack()

        livesFrame = tkinter.Frame(frame, \
            height=30,width=60,relief=tkinter.SUNKEN)
        livesFrame.pack()
        livesCanvas = ScrolledCanvas(livesFrame,150,40,150,40)
        livesCanvas.pack()
        livesTurtle = RawTurtle(livesCanvas)
        livesTurtle.ht()
        livesScreen = livesTurtle.getscreen()
        livesScreen.register_shape(SHIP_SHAPE, shapes[SHIP_SHAPE])

        life1 = SpaceShip(livesCanvas,-35,0,0,0)
        life2 = SpaceShip(livesCanvas,0,0,0,0)
        life3 = SpaceShip(livesCanvas,35,0,0,0)
        self.lives = [life1, life2, life3]

        self._t.ht()

        quitButton = tkinter.Button(frame, text = "Quit", command=self._handle_end)
        quitButton.pack()

        self.screen.tracer(0)

    def _bind_keys(self):

        self._originalGame.bind_key("Left", self._handle_left)
        self._originalGame.bind_key("Right", self._handle_right)
        self._originalGame.bind_key("Up", self._handle_up)
        self._originalGame.bind_key("space", self._handle_fire)
        self._originalGame.bind_key("q", self._handle_end)

    def _handle_end(self):
        self._endGame = True

    def _handle_left(self):
        self._leftClicks += 1

    def _handle_right(self):
        self._rightClicks += 1

    def _handle_up(self):
        self._upClicks += 1

    def _handle_fire(self):
        self._fireClicks += 1

    def get_num_lives(self):
        """
        :returns: int -- The amount of lives we have left, we initially have 3 lives.
        """
        return len(self.lives)

    def ship_down(self):
        """
        Should be called only when a ship is destroyed, this removes one life
        from our available lives.
        """
        deadship = self.lives.pop()
        deadship.ht()

    def get_score(self):
        """
        :returns: int -- The current score of the game
        """
        return int(self.scoreVal.get())

    def add_to_score(self, val):
        """
        Adds the given value into our current score.

        :param val: The amount of scores to add to out current score
        :type val: int
        """
        score = self.get_score()+val
        self.scoreVal.set(str(score))

    def start_game(self):
        """
        This is called to start our game (grphaics-wise).

        .. warning::

            **This method should not be called by you**
        """
        tkinter.mainloop()

    def set_initial_ship_cords(self, xCor,yCor, xSpeed=0,ySpeed=0):
        """
        Sets the initial coordinations for our ship, allows to set a starting
        speed for both x and y directions.

        :param xCor: The x coordinate to start from.
        :param yCor: The y coordinate to start from.
        :param xSpeed: (**OPTIONAL**) Sets the starting speed in the x direction.
        :param ySpeed: (**OPTIONAL**) Sets the starting speed in the y direction.
        :type xCor: int
        :type yCor: int
        :type xSpeed: int
        :type ySpeed: int
        """
        self.ship = SpaceShip(self._cv,xCor,yCor,xSpeed,ySpeed)

    def set_ship(self,ship):
        """
        This method should only be called if you created a ship of your own.

        :param ship: The ship to set as our main ship.
        :type ship: SpaceShip

        .. warning::

            **it should be called INSTEAD of the setInitialShipCords method**
        """
        self.ship = ship

    def get_ship(self):
        """
        :returns: SpaceShip -- Our ship object
        """
        return self.ship

    def get_torpedos(self):
        """
        :returns: The list of live torpedos.
        """
        return self.torpedos

    def remove_asteroid(self, asteroid):
        """
        Removes the given asteroid from our asteroids list

        :param asteroid: The asteroid to remove from our list of asteroids.
        :type asteroid: Asteroid
        """
        try:
            self.asteroids.remove(asteroid)
            asteroid.ht()
            asteroid.goto(self.get_screen_max_x()*2, self.get_screen_max_y()*2)
        except:
            print("didn't find asteroid in list")

    def remove_torpedos(self, deadtorpedos):
        """
        Removes the given list of dead torpedos from our live torpedos list

        :param deadtorpedos: The list of dead torpedos.
        :type deadtorpedos: list
        """
        for torpedo in deadtorpedos:
            try:
                self.torpedos.remove(torpedo)
            except:
                pass#print("didn't find torpedo")

            torpedo.goto(-self.get_screen_min_x()*2, -self.get_screen_min_y()*2)
            torpedo.ht()

    def update_screen(self):
        """
        Asks the screen to update itself **you should not call this method**
        """
        self.screen.update()

    def get_canvas(self):
        """
        This method should not be called by you - unless you implement new
        behaviour in the game.
        By using this canvas you could paint on the game board desired shapes

        :return: ScrolledCanvas --  The canvas on which turtle is painting the game
        """
        return self._cv

    def get_asteroids(self):
        """
        Returns a list of objects of type Asteroid, representing the current
        asteroids still living in our game
        """
        return self.asteroids

    def add_torpedo(self, x,y,xSpeed,ySpeed,angle):
        """
        This adds a torpedo into the game

        :param x: The x coordinate of the torpedo.
        :type x: int
        :param y: The y coordinate of the torpedo.
        :type y: int
        :param xSpeed: The current speed on the x direction.
        :type xSpeed: int
        :param ySpeed: The current speed on the y direction.
        :type ySpeed: int
        :param angle: The angle the torpedo is headed to
        :type angle: int
        """
        torpedo = PhotonTorpedo(self._cv, x,y,xSpeed,ySpeed,angle)
        self.torpedos.append(torpedo)

    def add_asteroid(self,x,y,xSpeed,ySpeed,size):
        """
        This adds an asteroid into the game

        :param x: The x coordinate of the asteroid.
        :type x: int
        :param y: The y coordinate of the asteroid.
        :type y: int
        :param xSpeed: The current speed on the x direction.
        :type xSpeed: int
        :param ySpeed: The current speed on the y direction.
        :type ySpeed: int
        :param size: The size of our asteroid, this is for default asteroids.
            The available sizes are 3(big), 2(medium) and 1(small).
        :type size: int
        """

        self.asteroids.append(Asteroid(self._cv,x,y,xSpeed,ySpeed,size,self._astroidIndex))
        self._astroidIndex += 1

    def add_initial_astroids(self, amnt=3):
        """
        This adds the given amnt of asteroids into the game, this method should
        be called at the beginning of the game

        :param amnt: The amount of asteroids to add, defualts to 3
        :type amnt: int
        """
        for k in range(amnt):
            dx = random.random() * 6 - 3
            dy = random.random() * 6 - 3
            x = random.random() * ( self.get_screen_max_x() - self.get_screen_min_x() ) \
                                    + self.get_screen_min_x()
            y = random.random() * (self.get_screen_max_y() - self.get_screen_min_y() ) \
                                + self.get_screen_min_y()

            self.add_asteroid(x,y,dx,dy,3)

    def should_end(self):
        """
        :returns: True if the game should end or not (if "q" was pressed or not)
        """
        return self._endGame


    def is_left_pressed(self):
        """
        :returns: True if the left key was pressed, else False
        """
        res = self._leftClicks > 0
        self._leftClicks -= 1 if res else 0
        return res

    def is_up_pressed(self):
        """
        :returns: True if the up key was pressed, else False
        """
        res = self._upClicks > 0
        self._upClicks -= 1 if res else 0
        return res

    def is_right_pressed(self):
        """
        :returns: True if the right key was pressed, else False
        """
        res = self._rightClicks > 0
        self._rightClicks -= 1 if res else 0
        return res

    def is_fire_pressed(self):
        """
        :returns: True if the fire key was pressed, else False
        """
        res = self._fireClicks > 0
        self._fireClicks -= 1 if res else 0
        return res

    def ontimer(self, func, milli):
        """
        This method is used to create a repeating action in your game.
	
        .. warning::
        
            **You don't need to call this method, it was already called for you at the end of the main game loop.**

        :param func: The function to repeat after **milli** milliseconds have passed
        :type func: function
        :param milli: The amount of milliseconds to wait before starting the given
            function
        :type milli: int
        """
        self.screen.ontimer(func,milli)

    def end_game(self):
        """
        This ends the current game.
        """
        self._root.destroy()
        self._root.quit()

    def get_original_game_handler(self):
        return self._originalGame

    def intersect(self, object1,object2):
        """
        This method is used to determine if two object have collided.
		
        :param object1: The first object
        :type object1: BaseObject
        :param object2: The second object
        :type object2: BaseObject
        """
        dist = math.sqrt((object1.xcor() - object2.xcor())**2 +
                        (object1.ycor() - object2.ycor())**2)

        radius1 = object1.get_radius()
        radius2 = object2.get_radius()

        return dist <= radius1+radius2

    
    def show_message(self,title, msg):
        """
        This is a method used to show messages in the game.

        :param title: The title of the message box.
        :type title: str
        :param msg: The message to show in the message box.
        :type msg: str
        """
        tkinter.messagebox.showinfo(str(title), str(msg) )

   
    def get_screen_max_x(self):
        """ Get the size of the maximal X coordinate in the active game screen """
        return self.__screenMaxX

    def get_screen_max_y(self):
        """ Get the size of the maximal Y coordinate in the active game screen """
        return self.__screenMaxY

    def get_screen_min_x(self):
        """ Get the size of the minimal X coordinate in the active game screen """
        return self.__screenMinX

    def get_screen_min_y(self):
        """ Get the size of the minimal Y coordinate in the active game screen """
        return self.__screenMinY
