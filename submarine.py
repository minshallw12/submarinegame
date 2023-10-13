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
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

# Define the height of the sand
SAND_HEIGHT = 60

# Define the height of the sky
SKY_HEIGHT = 100


# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Sand:
    def __init__(self):
        self.surf = pygame.Surface((SCREEN_WIDTH, SAND_HEIGHT))
        self.surf.fill("#b59438")
        self.rect = self.surf.get_rect(bottom=SCREEN_HEIGHT)

class Sky:
    def __init__(self):
        self.surf = pygame.Surface((SCREEN_WIDTH, SKY_HEIGHT))
        self.surf.fill("#7aa7eb")
        self.rect = self.surf.get_rect()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((40,10))
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
        if self.rect.top <= 95:
            self.rect.top = 95
        if self.rect.bottom >= SCREEN_HEIGHT - 60:
            self.rect.bottom = SCREEN_HEIGHT - 60

# Define the torpedo object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'torpedo'
class Torpedo(pygame.sprite.Sprite):
    def __init__(self, initial_position):
        super(Torpedo, self).__init__()
        self.surf = pygame.Surface((20,10))
        self.surf.fill((50, 10, 200))
        self.rect = self.surf.get_rect(center = initial_position)
        self.speed = 10
    
    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20,10))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(100, SCREEN_HEIGHT-60)
            )
        )
        self.speed = random.randint(5, 20)
    
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500)

# Instantiate the player, sky, and sand
player = Player()
sky = Sky()
sand = Sand()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
torpedos = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

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
            # Was it the Space Bar? If so, create a torpedo event
            elif event.key == K_SPACE:
                ADDTORPEDO = pygame.USEREVENT + 2
                new_torpedo = Torpedo(player.rect.center)
                torpedos.add(new_torpedo)
                all_sprites.add(new_torpedo)

        # Did the user click the window close button?
        elif event.type == QUIT:
            running = False

        # Add a new enemey to game
        elif event.type == ADDENEMY:
            # Create a new enemy and add it to sprite group
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    # Update the player position based on user keypresses
    player.update(pressed_keys)

    # Update enemey position each frame
    enemies.update()
    torpedos.update()

    # Fill the screen with color
    screen.fill("#0f3573")

    # Draw sky and sand
    screen.blit(sky.surf, sky.rect)
    screen.blit(sand.surf, sand.rect)

    # Draw all the sprites
    for sprite in all_sprites:
        screen.blit(sprite.surf, sprite.rect)

    # Check if an enemy collides with player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, remove the player and stop the game loop
        player.kill()
        running = False

    # Check if a torpedo collides with an enemy. Groupcollide() is used for collisions between sprite groups
    collisions = pygame.sprite.groupcollide(torpedos, enemies, True, True)

    # If there are collisions, remove the torpedo and enemy
    for torpedo, enemy in collisions.items():
        torpedo.kill()
        for e in enemy:
            e.kill()

    # Update the display
    pygame.display.flip()

    # Frame rate adjust here from clock created before main loop
    clock.tick(30)