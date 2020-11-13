# Import Python game-creation package
import pygame
from pygame.sprite import Group

# Import the settings module
from settings import Settings

# Import the ship module
from ship import Ship

# Import the game's functions module
import game_functions as gf

# Import the game's statisitcs module
from game_stats import GameStats

# Import the game's button module
from button import Button

# Import the scoreboard module
from scoreboard import Scoreboard

# Function initilizing game and containing main game loop
def run_game():
    # Initialize PyGame
    pygame.init()

    # Initialize settings
    ai_settings = Settings()

    # Initialize screen
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make the play button
    play_button = Button(ai_settings, screen, "Play")

    # Create an instance to store game statistics
    stats = GameStats(ai_settings)

    # Create an instance to store game stats and create scoreboard
    sb = Scoreboard(ai_settings, screen, stats)

    # Make a ship
    ship = Ship(ai_settings, screen)

    # Make a group to store bullets in
    # Using group() method from pygame.sprite package
    bullets = Group()

    # Create a group of aliens
    aliens = Group()

    # Create the fleet of aleins
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Start the main loop for the game
    while True:

        # Check for input events
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
                 bullets)

        # These things should only run when the game is active
        if stats.game_active:
            
            # Update ship movement
            ship.update()

            # Update bullets
            gf.update_bullets(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets)

            # Update aliens
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)

        # Update screen
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                         play_button)

# Run the game by calling the main function
run_game()
