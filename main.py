import sys
from time import sleep
import pygame


from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien

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

        #Init stats
        self.stats = GameStats(self)

        #Ship init
        self.ship = Ship(self)

        #Bullet
        self.bullets = pygame.sprite.Group()
        #Alien
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def run_(self):
        """ start the loopty loop/.. and pull? shoes? looking cool now, are we?"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
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

        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """ Keyup actions """
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

    def _fire_bullet(self):
        """ Fire the bullet """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):

        self.bullets.update()
        # Purge off screen bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
            print(len(self.bullets))

            self._check_bullet_alien_collisions()



    def _check_bullet_alien_collisions(self):
        """ respond to bullet-alien collisions. """

        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens,
                                                True, True)
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()


    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("Ship hit!!!!!")
            self._ship_hit()

    def _create_fleet(self):
        """ Create the fleet """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)


        for alien_number in range(number_aliens_x):
            alien = Alien(self)
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            self.aliens.add(alien)

    def _create_alien(self,alien_number, row_number):
        """ Create the alien """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """respond on event fleet reaches edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """ Drop the entire fleet and change the fleet direction """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """ player hit by alien"""

        self.stats.ships_left -= 1

        #purge aliens (more than likely this will be changed. )
        self.aliens.empty()
        self.bullets.empty()

        #new fleet (prob will also change later)
        self._create_fleet()
        self.ship.center_ship()

        #small pause
        sleep(0.5)

    def _update_screen(self):
        """ Update screen - Images, new screen, etc. """
        self.screen.fill(self.settings.bg_color)  # Redraw
        self.ship.blitme()  # ship draw

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        #  Make screen visible
        pygame.display.flip()




if __name__ == "__main__":
    """ Get in loser! We're running the game"""
    alleyuns_game = AliensTheGame()
    alleyuns_game.run_()
