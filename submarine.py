# Import game module and random numbers
import pygame
import random

# Import pygmae.locals for easeier aces to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

# Define constraints for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((20,10))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect()

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)

            # Keep player on the screen 
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH    
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
# class Enemy(pygame.sprite.Sprite):
#     def __init__(self):
#         super(Enemy, self).__init__()
#         self.surf = pygame.Surface((20,10))

# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Instantiate the player
player = Player()

#Variable to keep main loop running
running = True

# Create a clock to adjust the frame rate
clock = pygame.time.Clock()

# Main game loop
while running:
    # Look for every event in the queue
    for event in pygame.event.get():
        # Did the user pres down a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the game loop
            if event.key == K_ESCAPE:
                running = False
            
            # Did the user click the window close button?
            elif event.type == QUIT:
                running = False

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    # Update the player position based on user keypresses
    player.update(pressed_keys)

    # Fill the screen with color
    screen.fill((255,255,255))

    # Draw the player
    screen.blit(player.surf, player.rect)

    # Update the display
    pygame.display.flip()

    # Frame rate adjust here from clock created before main loop
    clock.tick(30)