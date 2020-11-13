class GameStats():
    """Track statistics for Alien Invasion"""

    def __init__(self, ai_settings):
        """Initialize statistics"""
        self.ai_settings = ai_settings
        self.reset_stats()

        # Start alien invasion in an active state
        self.game_active = False

        # High score, should never be reset
        # Accessing text file in game folder
        self.hs_file = open('highscore.txt', 'r')
        self.high_score = int(self.hs_file.read())

    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        # Number of ships left
        self.ships_left = self.ai_settings.ship_limit
        # Score
        self.score = 0
        # Level
        self.level = 1
        
