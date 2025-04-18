class GameStats:
    """ Stats n stuff"""
    def __init__(self, alleyuns):
        """ Init """
        self.settings = alleyuns.settings
        self.reset_stats()

    def reset_stats(self):
        """ Init stats for game (may change idunno yet)"""

        self.ships_left = self.settings.ships_limit


