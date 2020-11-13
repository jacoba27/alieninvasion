# sys is used to exit the game
import sys

# Use pygame for essential gaming tools
import pygame

# Import the bullet class from the bullet module
from bullet import Bullet

# Import the alien class from the alien module
from alien import Alien

# This is used to briefly pause the game
from time import sleep

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
                 bullets):
    """Respond to keypresses and mouse events"""
    # Loop checking for events
    for event in pygame.event.get():
        
        # Checking if the player wants to quit the game through exit button
        if event.type == pygame.QUIT:
            # Write new high score first
            write_new_high_score(stats)
            pygame.quit()
            sys.exit()

        # Starting ship movement when right or left key is pressed
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, stats, sb, screen, ship, bullets)

        # Stopping ship movement when key is released
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        # Check if the mouse left button is clicked
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Initialize the mouse position in variables
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Call function to activate play button
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y)

def write_new_high_score(stats):
    """Override high score text file with new high score"""
    if stats.score > stats.high_score:
        file='highscore.txt' 
        with open(file, 'w') as filetowrite:
            filetowrite.write(str(stats.score))

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y):
    """Start game when player clicks play button"""

    # Initialize variable for mouse clicking play button
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    # Check if the play button is clicked and
    # also check if the game is not already active
    if button_clicked and not stats.game_active:
        # Reset the game settings
        ai_settings.initialize_dynamic_settings()
        # Hide the mouse cursor
        pygame.mouse.set_visible(False)
        # Reset the game statistics
        stats.reset_stats()
        # Start the game
        stats.game_active = True
        # Reset the scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # Cleanse the game of aliens and bullets
        aliens.empty()
        bullets.empty()
        # Create new fleet
        create_fleet(ai_settings, screen, ship, aliens)
        # Center the ship
        ship.center_ship()

def check_keydown_events(event, ai_settings, stats, sb, screen, ship, bullets):
    """Respond to keypresses"""
    # If the right key is pressed down
    if event.key == pygame.K_RIGHT:
        # Activate the right ship movement flag
        ship.moving_right = True
    # If the left key is pressed down
    elif event.key == pygame.K_LEFT:
        # Activate the left ship movement flag
        ship.moving_left = True
    # If the spacebar is pressed
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    # Player can press 'q' to quit game
    elif event.key == pygame.K_q:
        # Write new high score first
        write_new_high_score(stats)
        pygame.quit()
        sys.exit()

def check_keyup_events(event, ship):
    """Respond to key releases"""
    # If the right key is released
    if event.key == pygame.K_RIGHT:
        # De-activate the right ship movement flag
        ship.moving_right = False
    # If the left key is released
    elif event.key == pygame.K_LEFT:
        # De-activate the left ship movement flag
        ship.moving_left = False

def check_high_score(stats, sb):
    """Check to see if there is a new high score"""
    # Check if current score is greater than high score
    if stats.score > stats.high_score:
        # Write new high score to file
        write_new_high_score(stats)
        # Set high score equal to current score
        stats.high_score = stats.score
        # Display new high score
        sb.prep_high_score()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                  play_button):
    """Updating each frame"""
    # Update background
    screen.fill(ai_settings.bg_color)

    # Update all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # Update ship
    ship.blitme()

    # Update aliens
    aliens.draw(screen)

    # Show the scoreboard
    sb.show_score()

    # Make the play button visible when the game is inactive
    if not stats.game_active:
        play_button.draw_button()

    # Update display
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets):
    """Update position of bullets and get rid of old bullets"""
    
    # Update bullet positions
    bullets.update()

    # Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    # Enable response from bullet-alien collisions
    # To remove the aliens and bullets that collide
    # By calling a function
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets):
    """Respond to bullet-alien collisions"""

    # Remove any bullets and aliens that have collided
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    # Check for aliens being destroyed
    if collisions:
        for aliens in collisions.values():
            # Increase player score
            stats.score += ai_settings.alien_points * len(aliens)
            # Display increased score
            sb.prep_score()
        # Check if high score is broken
        check_high_score(stats, sb)
        
    # When all aliens are destroyed
    if len(aliens) == 0:
        # Destroy all bullets
        bullets.empty()
        # Increase speed of game
        ai_settings.increase_speed()
        # Increase level
        stats.level += 1
        sb.prep_level()
        # Create new alien fleet
        create_fleet(ai_settings, screen, ship, aliens)

def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet"""

    # Create a new bullet and add it to the bullets group
    # Only if it's under the bullet limit length
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens"""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """Create the full fleet of aliens"""

    # Define some values which will help create the fleet of aliens
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    # Create the fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                         row_number)

def check_fleet_edges(ai_settings, aliens):
    """Detect when aliens have reached the edge of the screen"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Drop alien fleet and change their direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to ship being hit by alien"""

    # Check if there are still ships left
    if stats.ships_left > 0:
        
        # Decrement ships left
        stats.ships_left -= 1

        # Update scoreboard
        sb.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause briefly to let player notice
        sleep(0.5)

    # Otherwise, end the game
    else:
        stats.game_active = False
        # Also make the mouse cursor visible again
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen"""
    # Define the rectangle for the entire screen
    screen_rect = screen.get_rect()
    # Loop through each alien
    for alien in aliens.sprites():
        # Check if the alien hits the bottom
        if alien.rect.bottom >= screen_rect.bottom:
            # Treated the same as if the ship got hit
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Update positions of all aliens in the fleet"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # Look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)
