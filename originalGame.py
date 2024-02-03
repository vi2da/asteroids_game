from gameMaster import *

class OriginalGame:
    def __init__(self, game):
        self._game = game
        self._boundKeys = []

    def add_original_torpedo(self, torpedo):
        """
        This function allows you to add specaily crafted torpedos.

        :param torpedo: The new torpedo to add
        :type torpedo: BaseObject
        """
        self._game.get_torpedos().append(torpedo)

    def add_shape(self,name,cords,override=False):
        """
        Adds a shape, and binds it into the screen so we could paint it later on.
        If this shape was previously defined than it won't be changed.

        :param name: The name of the shape.
        :type name: str
        :param cords: The coordinates of the shape, for example our ship is
            defined like so '((-10,-10),(0,-5),(10,-10),(0,10))' -

            our first line will go from (-10,-10) towards (0,-5) then
            the next line to (10,-10) and from there to (0,10) - this
            is the last point so it will also close the picture.
        :type cords: tuple of tuples of ints
        """
        self._game._shapeMaster.add_shape(name,cords,override)

    def bind_key(self, key, func):
        """
        This method is to allow you to add some functionality of your own,
        it allows you to bind the provided function to the desired input key.

        If there is already a function bound to this key it will do nothing.

        :param key: A key to bind.
        :type key: str
        :param func: The function to bind
        :type func: function
        """

        if key not in self._boundKeys:
            self._game.screen.onkeypress(func,key)
            self._boundKeys.append(key)
