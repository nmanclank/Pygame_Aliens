import sys
from time import sleep
import pygame

from pygame.sprite import RenderUpdates
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
clock = pygame.time.Clock()

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

        #instance of scrboard
        self.sb = Scoreboard(self)

        #Ship init
        self.ship = Ship(self)

        #Bullet
        self.bullets = pygame.sprite.Group()
        #Alien
        self.aliens = RenderUpdates()

        self._create_fleet()

        #btton
        self.play_button = Button(self, "Play")

        self.background =pygame.Surface(self.screen.get_size())
        self.background.fill(self.settings.bg_color)
        self.background = self.background.convert()

    def run_(self):
        """ start the loopty loop/.. and pull? shoes? looking cool now, are we?"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            clock.tick(60)

    def _check_events(self):
        # game input events (kbm and whatnot)

        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                sys.exit()

                #play button click event
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    def _check_play_button(self, mouse_pos):
        """ start new game on click"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        if button_clicked and not self.stats.game_active:

            #reset game speed scaled
            self.settings.init_dynamic_settings()

            #hide cursor
            pygame.mouse.set_visible(False)

            self.stats.reset_stats()
            self.stats.game_active = True


            #prep
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

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
            #print(len(self.bullets))
            self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """ respond to bullet-alien collisions. """

        #print(len(self.aliens))
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens,
                                                True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            #increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """ Update """
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("Ship hit!!!!!")
            self._ship_hit()
        # Also check for bottom aliens
        self._check_aliens_bottom()

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

        if self.stats.ships_left > 0:

            self.stats.ships_left -= 1
            self.sb.prep_ships()
#############purge aliens (more than likely this will be changed. )
            self.aliens.empty()
            self.bullets.empty()
#############new fleet (prob will also change later)
            self._create_fleet()
            self.ship.center_ship()
#############small pause
            sleep(0.5)
        else:
            self.stats.game_active = False
#############toggle mouse visible
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """ return True if alien is bottom of screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _update_screen(self):
        """ Update screen - Images, new screen, etc. """

        #dirty = self.aliens.draw(self.background)


        self.screen.blit(self.background, (0, 0))

        self.ship.blitme()

        #dirty.extend(self.aliens.draw(self.screen))

        self.screen.fill(self.settings.bg_color)  # Redraw
        self.ship.blitme()  # ship draw
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()


        self.aliens.draw(self.screen)

#############Draw score info
        self.sb.show_score()

#############draw button IF
        if not self.stats.game_active:
            self.play_button.draw_button()

        #  Make screen visible
        #pygame.display.update(dirty)
        pygame.display.flip()

if __name__ == "__main__":
    """ Get in loser! We're running the game"""
    alleyuns_game = AliensTheGame()
    alleyuns_game.run_()