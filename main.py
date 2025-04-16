import sys
import pygame

class AliensTheGame:
    """ Main game class """
    def __init__(self):
        """ Initialization (resources and whatever who cares)"""
        pygame.init()

        self.screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption('Aliens!')
    def run_(self):
        """ start the loopty loop/.. and pull? shoes? looking cool now, are we?"""
        while True:
            # game input events (kbm and whatnot)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            # Make screen visible
            pygame.display.flip()




if __name__ == "__main__":
    """ Get in loser! We're running the game"""
    alley_uns = AliensTheGame()
    alley_uns.run_()
