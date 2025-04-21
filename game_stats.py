class GameStats:
    """ Stats n stuff"""
    def __init__(self, alleyuns):
        """ Init """
        self.settings = alleyuns.settings
        self.reset_stats()
        #start in inactive state
        self.game_active = False

        self.high_score = 0

    def reset_stats(self):
        """ Init stats for game (may change idunno yet)"""

        self.ships_left = self.settings.ships_limit
        self.score = 0
        self.level = 1


