import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """ Bullet class """
    def __init__(self, alleyuns):
        """ Create bullet object   """
        super().__init__()
        self.screen = alleyuns.screen
        self.settings = alleyuns.settings
        self.color = alleyuns.settings.bullet_color

        #create bullet rect obj (0,0) + position correct
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = alleyuns.ship.rect.midtop

        #postion
        self.y = float(self.rect.y)

    def update(self):
        """ Move the bullet """
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)