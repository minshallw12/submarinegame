# Import game module and random numbers
import pygame
import pygame.freetype
import os
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

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Define the height of the sand
SAND_HEIGHT = 60

# Define the height of the sky
SKY_HEIGHT = 100

#Creat a font path
font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "fonts", "dogicapixelbold.ttf")
font_size = 64
pygame.freetype.init()
myfont = pygame.freetype.Font(font_path, font_size)

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
def stats(score):
    myfont.render_to(screen, (4, 4), "Score:"+str(score), (80, 80, 155), None, size=15)


class Sand(pygame.sprite.Sprite):
    def __init__(self):
        super(Sand, self).__init__()
        self.surf = pygame.Surface((SCREEN_WIDTH, SAND_HEIGHT))
        self.surf.fill("#d4cb7d")
        self.rect = self.surf.get_rect(bottom=SCREEN_HEIGHT)

class Sky(pygame.sprite.Sprite):
    def __init__(self):
        super(Sky, self).__init__()
        self.surf = pygame.Surface((SCREEN_WIDTH, SKY_HEIGHT))
        self.surf.fill("#7aa7eb")
        self.rect = self.surf.get_rect()

OBJECT_HEIGHT = 50
OBJECT_WIDTH = 50
class Sticker(pygame.sprite.Sprite):
    def __init__(self, position, image_path):
        super(Sticker, self).__init__()
        self.surf = pygame.image.load(image_path).convert_alpha()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(bottom = position[0], left = position[1])

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("./sprites/submarinewindowless.png").convert_alpha()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.score = 0

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
        if self.rect.top <= 85:
            self.rect.top = 85
        if self.rect.bottom >= SCREEN_HEIGHT - 60:
            self.rect.bottom = SCREEN_HEIGHT - 60

# Define the torpedo object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'torpedo'
class Torpedo(pygame.sprite.Sprite):
    def __init__(self, initial_position):
        super(Torpedo, self).__init__()
        self.surf = pygame.image.load("./sprites/spr_missile2.png").convert_alpha()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center = initial_position)
        self.speed = 10
    
    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class EnemyTorp(pygame.sprite.Sprite):
    def __init__(self):
        super(EnemyTorp, self).__init__()
        self.surf = pygame.image.load("./sprites/spr_missile1.png").convert_alpha()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
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

class Destroyer(pygame.sprite.Sprite):
    def __init__(self):
        super(Destroyer, self).__init__()
        self.surf = pygame.image.load("./sprites/ship1.png").convert_alpha()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                70
            )
        )
        self.speed = random.randint(1, 3)
        self.last_drop_time = 0
    
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Depth_Charge(pygame.sprite.Sprite):
    def __init__(self, initial_position):
        super(Depth_Charge, self).__init__()
        self.surf = pygame.image.load("./sprites/depth_charge2.png").convert_alpha()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center = initial_position)
        self.speed = random.randint(1,3)
    
    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > 750:
            self.kill()

# Initialize pygame
pygame.init()


# Create a custom event for adding a new enemy
ADDENEMYTORP = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMYTORP, 500)
ADDDESTROYER = pygame.USEREVENT + 2
pygame.time.set_timer(ADDDESTROYER, 7000)
ADDDEPTH_CHARGE = pygame.USEREVENT + 3
pygame.time.set_timer(ADDDEPTH_CHARGE, random.randint(500, 3000))


# Instantiate the player, sky, and sand
player = Player()
sky = Sky()
sand = Sand()
# pass coordinates in list [x,y]
cloud = Sticker([105, SCREEN_WIDTH-200], "./sprites/cloud22.png")
cloud2 = Sticker([115, 300], "./sprites/cloud22.png")
rock = Sticker([SCREEN_HEIGHT-40, SCREEN_WIDTH-500], "./sprites/4411.png")
chest = Sticker([SCREEN_HEIGHT-35, 70], "./sprites/titanic2.png")

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemy_torps = pygame.sprite.Group()
destroyers = pygame.sprite.Group()
depth_charges = pygame.sprite.Group()
torpedos = pygame.sprite.Group()
decor = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

destroyer_delays = {}

#Variable to keep main loop running
running = True

# Create a clock to adjust the frame rate
clock = pygame.time.Clock()

# Main game loop
while running:
    
    # Add the decor sprites to decor group to be rendered
    decor.add(sky, sand, cloud, cloud2, rock, chest)

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

        # Add a new enemy to game
        elif event.type == ADDENEMYTORP:
            # Create a new enemy and add it to sprite group
            new_enemy_torp = EnemyTorp()
            enemy_torps.add(new_enemy_torp)
            all_sprites.add(new_enemy_torp)
        
        elif event.type == ADDDESTROYER:
            new_destroyer = Destroyer()
            destroyers.add(new_destroyer)
            all_sprites.add(new_destroyer)
            destroyer_delays[new_destroyer] = random.randint(500, 3000)

        elif event.type == ADDDEPTH_CHARGE:
            for destroyer in destroyers:
                if destroyer in destroyer_delays and pygame.time.get_ticks() - destroyer.last_drop_time >= destroyer_delays[destroyer]:
                    new_depth_charge = Depth_Charge(destroyer.rect.center)
                    depth_charges.add(new_depth_charge)
                    all_sprites.add(new_depth_charge)
                    destroyer.last_drop_time = pygame.time.get_ticks()

        

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    # Update the player position based on user keypresses
    player.update(pressed_keys)

    # Update enemey position each frame
    enemy_torps.update()
    destroyers.update()
    depth_charges.update()
    torpedos.update()

    # Fill the screen with color
    screen.fill("#0f3573")

    # Draw sky, sand, clouds, rock, chest
    for sprite in decor:
        screen.blit(sprite.surf, sprite.rect)

    # Draw all the sprites
    for sprite in all_sprites:
        screen.blit(sprite.surf, sprite.rect)

    # Check if an enemy collides with player
    if pygame.sprite.spritecollideany(player, enemy_torps) or pygame.sprite.spritecollideany(player, destroyers) or pygame.sprite.spritecollideany(player, depth_charges):
        # If so, remove the player and stop the game loop
        player.kill()
        running = False

    # Check if a torpedo collides with an enemy. Groupcollide() is used for collisions between sprite groups
    enemy_torp_collisions = pygame.sprite.groupcollide(torpedos, enemy_torps, True, True)
    destroyer_collisions = pygame.sprite.groupcollide(torpedos, destroyers, True, True)

    # If there are collisions, remove the torpedo and enemy
    for torpedo, enemy_torp in enemy_torp_collisions.items():
        torpedo.kill()
        player.score += 1
        for e in enemy_torp:
            e.kill()
    for torpedo, destroyer in destroyer_collisions.items():
        torpedo.kill()
        player.score += 2
        for e in destroyer:
            e.kill()


    stats(player.score)
    # Update the display
    pygame.display.flip()

    # Frame rate adjust here from clock created before main loop
    clock.tick(30)