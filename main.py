import sys
import pygame
from settings import Settings
from ship import Ship


class AliensTheGame:
    """ Main game class """
    def __init__(self):
        """ Initialization (resources and whatever who cares)"""
        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Aliens!')


        #Ship init
        self.ship = Ship(self)

    def run_(self):
        """ start the loopty loop/.. and pull? shoes? looking cool now, are we?"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()

    def _check_events(self):
        # game input events (kbm and whatnot)

        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """ Keydown actions """
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True

        elif event.key == pygame.K_q:
                    sys.exit()

    def _check_keyup_events(self, event):
        """ Keyup actions """
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False




    def _update_screen(self):
        """ Update screen - Images, new screen, etc. """
        self.screen.fill(self.settings.bg_color)  # Redraw
        self.ship.blitme()  # ship draw

        # Make screen visible
        pygame.display.flip()




if __name__ == "__main__":
    """ Get in loser! We're running the game"""
    alleyuns_game = AliensTheGame()
    alleyuns_game.run_()
