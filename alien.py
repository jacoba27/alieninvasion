import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, ai_settings, screen):
        """Initialize the alien and set its starting position"""

        # Used to create alien sprite
        super(Alien, self).__init__()
        
        # Initialize screen
        self.screen = screen
        
        # Initialize settings
        self.ai_settings = ai_settings

        # Load the alien image
        self.image = pygame.image.load('alien.bmp')

        # Set the rectangle for the alien image
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the aliens exact position
        self.x = float(self.rect.x)

    def blitme(self):
        """Generate (or re-generate) the alien at its current position"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Return True if alien is at edge of screen"""
        # Get rectangle coordinates for entire screen
        screen_rect = self.screen.get_rect()
        # Compare edge coordinates of alien and entire screen
        # To determine when to switch directions
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Update alien movement"""
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x
        
