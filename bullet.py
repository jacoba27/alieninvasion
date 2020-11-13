import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_settings, screen, ship):
        """Create a bullet object at the ship's current position"""

        # The super() method utilizes the pygame sprites to group all
        # bullets together, treating them like one object
        super(Bullet, self).__init__()
        self.screen = screen

        # Create a bullet rectangle, first at (0, 0), and then setting
        # its correct position above the ship
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Store the bullet's position as a decimal value
        # This will allow us to be more precise with its location
        self.y = float(self.rect.y)

        # Setting up some basic attributes for the bullet
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Moving the bullet up the screen"""

        # Update the decimal position of the bullet
        self.y -= self.speed_factor

        # Update the rectangle position
        self.rect.y = self.y

    def draw_bullet(self):
        """Generate the bullet on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
