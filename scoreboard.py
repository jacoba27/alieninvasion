import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    """A class to report scoring information"""

    def __init__(self, ai_settings, screen, stats):
        """Initialize scorekeeping attributes"""
        # Screen
        self.screen = screen
        # Rectangle for screen
        self.screen_rect = screen.get_rect()
        # Settings
        self.ai_settings = ai_settings
        # Statistics
        self.stats = stats

        # Font settings for scoring display
        # Font color
        self.text_color = (30, 30, 30)
        # Size and font type
        self.font = pygame.font.SysFont(None, 48)

        # Prepare image of scoreboard using function
        self.prep_score()
        # Prepare image of high score as well
        self.prep_high_score()
        # Prepare level display
        self.prep_level()
        # Prepare ships left display
        self.prep_ships()

    def prep_score(self):
        """Prepare score to be shown on screen"""

        # Initialize the string for the score variable, rounded
        rounded_score = int(round(self.stats.score, -1))
        # Insert commas into number where needed
        score_str = "{:,}".format(rounded_score)
        # Render the image of the score
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.ai_settings.bg_color)

        # Display score at top right of screen
        # Obtain rectangle of scoring text image
        self.score_rect = self.score_image.get_rect()
        # Place right side of image near the right side of screen
        self.score_rect.right = self.screen_rect.right - 20
        # Place top of image near top of screen
        self.score_rect.top = 20

    def show_score(self):
        """Show scoreboard on screen"""
        # Current score
        self.screen.blit(self.score_image, self.score_rect)
        # High score
        self.screen.blit(self.high_score_image, self.high_score_rect)
        # Level
        self.screen.blit(self.level_image, self.level_rect)
        # Ships
        self.ships.draw(self.screen)

    def prep_high_score(self):
        """Prepare high score to be shown on screen"""

        # Initialize rounded score
        high_score = int(round(self.stats.high_score, -1))
        # Format the string as a number with commas where needed
        high_score_str = "{:,}".format(high_score)
        # Render high score as an image
        self.high_score_image = self.font.render(high_score_str, True,
                                                  self.text_color, self.ai_settings.bg_color)

        # Center the high score at the top of the screen
        # Obtain the rectangle for the high score image
        self.high_score_rect = self.high_score_image.get_rect()
        # Center the high score at the center of the whole screen
        self.high_score_rect.centerx = self.screen_rect.centerx
        # Put the high score at the same height as current score
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Turn the level into a rendered image"""
        # Render the image of the level
        self.level_image = self.font.render(str(self.stats.level), True,
                                            self.text_color, self.ai_settings.bg_color)
        # Position the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Show how many ships are left"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
