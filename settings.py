class Settings():
    """A class to store all settings for the game"""

    def __init__(self):
        """Initialize the game's static settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        # Alien settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.2
        # How quicmkly the alien point values increase
        self.score_scale = 1.5
        
        # Initialize the settings that change throughout the game
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        # Speed of the ship
        self.ship_speed_factor = 1.2
        # Speed of bullets
        self.bullet_speed_factor = 5
        # Speed of aliens
        self.alien_speed_factor = 1

        # Changing fleet direction
        # 1 represents right; -1 represents left
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 100

    def increase_speed(self):
        """Increase speed and point settings"""

        # Ship
        self.ship_speed_factor *= self.speedup_scale
        # Bullets
        self.bullet_speed_factor *= self.speedup_scale
        # Aliens
        self.alien_speed_factor *= self.speedup_scale

        # Increase alien point values as game gets harder
        self.alien_points = int(self.alien_points * self.score_scale)
