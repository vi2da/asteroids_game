# David Ohayon - 1 January 2015 - Happy New Year!
from torpedo import *
from asteroid import *
from spaceship import *
from gameMaster import *
import math
class GameRunner:
    # Score added when hitting Small, Medium and Big asteroid respectively
    LIST_SCORE   = [100, 50, 20]
    # Sizes of asteroids (Small, Medium and Big)
    LIST_SIZE    = [1, 2, 3]
    # Maximum torpedo that can be used during the game
    MAX_TORPEDO = 20
    # Minimum value allowed after countdown (for torpedo, life, etc.)
    MIN_PERMITED = 0
    def __init__(self, amnt = 3):
        self.game = GameMaster()
        self.screenMaxX = self.game.get_screen_max_x()
        self.screenMaxY = self.game.get_screen_max_y()
        self.screenMinX = self.game.get_screen_min_x()
        self.screenMinY = self.game.get_screen_min_y()
        shipStartX = (self.screenMaxX-self.screenMinX) / 2 + self.screenMinX
        shipStartY = (self.screenMaxY-self.screenMinY) / 2 + self.screenMinY
        self.game.set_initial_ship_cords( shipStartX, shipStartY )
        self.game.add_initial_astroids(amnt)
    def run(self):
        self._do_loop()
        self.game.start_game()
    def _do_loop(self):
        self.game.update_screen()
        self.game_loop()
        # Set the timer to go off again
        self.game.ontimer(self._do_loop,5)
    def game_loop(self):
        self.move_asteroid()
        self.move_ship()
        self.shoot_torpedo()
        self.move_torpedos()
        self.check_end()
        self.asteroid_explosion()
        self.ship_collision()
    def move_object(self, object1):
        """
        Get an object and move it according to its location and speed
        """
        screen_range_x = self.screenMaxX - self.screenMinX
        # New x cordinate based relative to the screen size
        new_cord_x = (object1.get_speed_x() + object1.get_x_cor() -
                        self.screenMinX) % screen_range_x + self.screenMinX
        screen_range_y = self.screenMaxY - self.screenMinY
        # New y cordinate based relative to the screen size
        new_cord_y = (object1.get_speed_y() + object1.get_y_cor() -
                        self.screenMinY) % screen_range_y + self.screenMinY
        object1.move(new_cord_x, new_cord_y)
    def move_asteroid(self):
        """
        For all the asteroids on the screen, move to their next position
        """
        for asteroid in self.game.get_asteroids():
            self.move_object(asteroid)
    def move_ship(self):
        """
        Decide if need to change angle and to accelerate, based on the
        keys pressed
        """
        # Get the ship object to reuse it more easily in the function
        ship = self.game.get_ship()
        if self.game.is_right_pressed():
            ship.decrease_angle()
        if self.game.is_left_pressed():
            ship.increase_angle()
        # If the key pressed is the up key, increase the speed in the same
        # direction the ship is oriented
        if self.game.is_up_pressed():
            angle_rad = math.radians(ship.get_angle())
            ship.set_speed_x(ship.get_speed_x() + math.cos(angle_rad))
            ship.set_speed_y(ship.get_speed_y() + math.sin(angle_rad))
        # Move the ship according to the new direction and speed
        self.move_object(ship)
    def shoot_torpedo(self):
        ship = self.game.get_ship()
        if self.game.is_fire_pressed():
            # if more than a predefined number of torpedos on the screen
            # don’t shoot
            if len(self.game.get_torpedos()) <= self.MAX_TORPEDO:
                # Get the current position - It will be the first position
                # of the torpedo
                x = ship.get_x_cor()
                y = ship.get_y_cor()
                #
                # Speed of the torpedo based on ship speed and angle
                angle_rad = math.radians(ship.get_angle())
                speed_x = ship.get_speed_x() + (2 * math.cos(angle_rad))
                speed_y = ship.get_speed_y() + (2 * math.sin(angle_rad))
                # Adds a torpedo into the game with those parameters
                self.game.add_torpedo(x ,y ,speed_x, speed_y, ship.get_angle())
    def move_torpedos(self):
        """
        Move the torpedos to their new position and remove from the screen
        all the torpedos that exceeded lifetime
        """
        # List of torpedos to remove from the screen
        dead_torpedos = []
        for torpedo in self.game.get_torpedos():
            # If the current torpedo used all its time, add to list for removal
            if torpedo.get_life_span() <= self.MIN_PERMITED:
                dead_torpedos.append(torpedo)
            # else, move the torpedo to its next position
            else:
                self.move_object(torpedo)
        # Remove all the torpedos with expired lifetime
        self.game.remove_torpedos(dead_torpedos)
    def new_two_asteroids(self, torpedo, asteroid):
        """
        Get the torpedo and the hitten asteroid to calculate the speed of the
        2 new asteroids and add them to the game
        """
        # If the exploded asteroid was not a small one, split it into 2
        # Note: get_size - 1 to get the index
        size_idx = self.LIST_SIZE.index(asteroid.get_size()) - 1
        #if self.LIST_SIZE[size_idx] > self.LIST_SIZE[self.MIN_PERMITED]:
        if size_idx >= self.MIN_PERMITED:
            # Calculate the speed of the new asteroids after impact
            distance = (asteroid.get_speed_x() ** 2 +
                        asteroid.get_speed_y() ** 2) ** 0.5
            speed_x = \
                (torpedo.get_speed_x() + asteroid.get_speed_x()) / distance
            speed_y = \
                (torpedo.get_speed_y() + asteroid.get_speed_y()) / distance
            # Current location of the asteroid that exploded
            x = asteroid.get_x_cor()
            y = asteroid.get_y_cor()
            # Add 2 asteroids with opposite directions
            self.game.add_asteroid(x, y, speed_x, speed_y,
                                   self.LIST_SIZE[size_idx])
            self.game.add_asteroid(x, y, -speed_x, -speed_y,
                                   self.LIST_SIZE[size_idx])
    def asteroid_explosion(self):
        """
        Behaviour when an asteroid explodes: replace the asteroid with 2 new
        asteroids, get the score relative to the size of the
        exploded asteroid, and also remove the torpedos.
        """
        # Keep the initial lists of torpedos and asteroids for the loop because
        # they are changing during the process (when there is an explosion)
        list_torpedos = [torp for torp in self.game.get_torpedos()]
        list_asteroids = [astr for astr in self.game.get_asteroids()]
        for asteroid in list_asteroids:
            for torpedo in list_torpedos:
                if self.game.intersect(asteroid, torpedo):
                    # Get the index of the list of size LIST_SIZE of the
                    # ateroid, it is also the index of the corresponding score
                    size_idx = self.LIST_SIZE.index(asteroid.get_size())
                    self.game.add_to_score(self.LIST_SCORE[size_idx])
                    self.new_two_asteroids(torpedo, asteroid)
                    # Remove the ateroid that exploded
                    self.game.remove_asteroid(asteroid)
                    # Remove the list of 1 torpedo that exploded
                    self.game.remove_torpedos([torpedo])
    def ship_collision(self):

           # Flag to indicate if a collision happenned
           has_collided = False
           # Keep the initial list of asteroids for the loop because it is
           # changing during the process (when there is a collision)
           list_asteroids = [asteroid for asteroid in self.game.get_asteroids()]
           for asteroid in list_asteroids:
               # If there is a collision between asteroid and ship
               if self.game.intersect(self.game.get_ship(), asteroid):
                   self.game.remove_asteroid(asteroid)
                   has_collided = True
           # In case there was a collision.
           # This process is out of the "for" to avoid to decrease more than one
           # life in case of more than one collision at the same time
           if has_collided:
               # Decrease one life
               self.game.ship_down()
               self.game.show_message("Collision!!", "Houston we had a problem")


    def check_end(self):
        """
        End the game at those conditions
        """
        end_game = False
        # Lost the last life after impact whith asteroide
        if self.game.get_num_lives() == self.MIN_PERMITED:
            self.game.show_message("You loose!", "Game Over!")
            end_game = True
        # No more asteroid
        elif len(self.game.get_asteroids()) == self.MIN_PERMITED:
            self.game.show_message("You win!","Congratulation!")
            end_game = True
        # User pressed quit key (Q)
        elif self.game.should_end():
            self.game.show_message("Good Bye!","You quit the game")
            end_game = True
        # if one of the conditions happenned
        if end_game:
            self.game.end_game()


def main():
    runner = GameRunner()
    runner.run()


if __name__ == "__main__":
    main()
