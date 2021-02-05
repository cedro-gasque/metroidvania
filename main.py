# Import the pygame module
import pygame

# Import random for random numbers
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Initialize pygame
pygame.init()
held_keys = {K_LEFT: False, K_RIGHT: False, K_UP: False}
# Define constants for the screen width and height
info_object = pygame.display.Info()

SCREEN_WIDTH = info_object.current_w
SCREEN_HEIGHT = info_object.current_h

GRAVITY = 0.03


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((8, 12))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.x = 0
        self.y = 0.
        self.grounded = True
        self.jumpspeed = -2
        self.jumpshortspeed = -1

    def left_right(self, pressed_keys, n, m, o, p):
        if pressed_keys[n]:
            if not held_keys[n]:
                held_keys[n] = True
                self.x = o
        else:
            held_keys[n] = False
            if held_keys[m]:
                self.x = p

    def update(self, pressed_keys):
        print(self.rect.top)
        if pressed_keys[K_UP]:
            if self.grounded:
                self.y = self.jumpspeed
            held_keys[K_UP] = True
        elif held_keys[K_UP]:
            held_keys[K_UP] = False
            if not self.grounded:
                if self.y < self.jumpshortspeed:
                    self.y = self.jumpshortspeed

        self.left_right(pressed_keys, K_LEFT, K_RIGHT, -1, 1)
        self.left_right(pressed_keys, K_RIGHT, K_LEFT, 1, -1)

        if not (pressed_keys[K_LEFT] or pressed_keys[K_RIGHT]):
            self.x = 0
        self.rect.move_ip(self.x, self.y)
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 320:
            self.rect.right = 320
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= 180:
            self.rect.bottom = 180
            self.grounded = True
            self.y = 0
        else:
            print(self.y)
            self.grounded = False
            self.y += GRAVITY


# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.Surface((320, 180))
window = pygame.display.set_mode((SCREEN_WIDTH//2, SCREEN_HEIGHT//2), pygame.NOFRAME)

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
# pygame.time.set_timer(ADDENEMY, 250)

# Instantiate player. Right now, this is just a rectangle.
player = Player()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Variable to keep the main loop running
running = True

# Main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN and event.key == K_ESCAPE\
           or event.type == QUIT:
            running = False

        # Add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    player.update(pressed_keys)

    # Update enemy position
    enemies.update()

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, then remove the player and stop the loop
        player.kill()
        running = False

    window.blit(pygame.transform.scale(screen, window.get_rect().size), (0, 0))
    # Update the display
    pygame.display.flip()
