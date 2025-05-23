class Settings:
    """ Do I even have to explain what this class does? If you can't tell, go to bed..."""

    def __init__(self):
        # Screen
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_color = (241, 148, 138)

        #SHIP
        self.ship_speed = 10
        self.ships_limit = 3

        #Bullet settings
        self.bullet_speed = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)

        self.bullets_allowed = 25

        # Aliens
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10


        #Speed scale up
        self.speedup_scale = 1.1

        # Score scaling
        self.score_scale = 1.5

        self.init_dynamic_settings()




    def init_dynamic_settings(self):
        """ Init non static settings """
        #self.ship_speed = 1.5
        self.bullet_speed = 5.0
        self.alien_speed = 3.0
        self.alien_points = 50

        self.fleet_direction = 1

    def increase_speed(self):
        """ Increase speed """
        self.alien_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        #self.ship_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
