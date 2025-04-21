import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """ Class for Alien base"""
    def __init__(self, alleyuns_game):
        """ init alien"""
        super().__init__()
        self.screen = alleyuns_game.screen
        self.settings = alleyuns_game.settings

        #img load and rect init
        self.image = pygame.image.load("resources/images/alien.png").convert_alpha()
        #self.image = pygame.transform.scale(self.image, (75, 75))
        #self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()

        #start loc
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def check_edges(self):
        """ return True if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()

        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """ They move? duh."""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
