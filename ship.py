import pygame


class Ship:
    """ A class for the 'ship'. """

    def __init__(self, alleyuns):
        """ Initialization for ship and position """
        self.screen = alleyuns.screen
        self.screen_rect = alleyuns.screen.get_rect() ## LOL git_rekt()

        self.settings = alleyuns.settings

        # Load the shippy and its rekt xD -um? o_O?
        self.image = pygame.image.load('resources/images/ship.png').convert_alpha()
        self.rect = self.image.get_rect()

        # new ship start pos (bottom -center)
        self.rect.midbottom = self.screen_rect.midbottom

        ##Ship pos
        self.x = float(self.rect.x)

        #MOVEMENT FLAG
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """ Update movement of self"""



        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        elif self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # X update
        self.rect.x = self.x


    def blitme(self):
        """ Draw the ship and current location. """

        self.screen.blit(self.image, self.rect)
    def center_ship(self):
        """ What do you think it does?"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)



