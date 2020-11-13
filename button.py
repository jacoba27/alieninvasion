# Allows pygame to render text to the screen
import pygame.font

class Button():

    def __init__(self, ai_settings, screen, msg):
        """Initialize the attributes of the play button"""

        # Set the variable for the screen
        self.screen = screen
        # Set the variable for the screen rectangle
        self.screen_rect = screen.get_rect()

        # Set the dimensions and color properties of the button
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button rectangle object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button message only needs to be prepared once
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Turn the message into a rendered image and center text on button"""

        # Render the text as an image
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        # Retrieve the rectangle for the text image
        self.msg_image_rect = self.msg_image.get_rect()
        # Center the text rectangle
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button
        self.screen.fill(self.button_color, self.rect)
        # Draw message on button
        self.screen.blit(self.msg_image, self.msg_image_rect)
