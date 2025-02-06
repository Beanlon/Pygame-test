import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 1441, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Platform Game')

# Choose a proportional tile size   
TILE_SIZE = 60  # Proportional size based on GCD

clock = pygame.time.Clock()

# Load and scale background image
background = pygame.image.load("Sky4.jpg")  
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

def draw_grid():
    """Draws a grid with proportional tiles."""
    for x in range(0, WIDTH, TILE_SIZE):  # Vertical lines
        pygame.draw.line(screen, (255, 255, 255), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILE_SIZE):  # Horizontal lines
        pygame.draw.line(screen, (255, 255, 255), (0, y), (WIDTH, y))

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, moving, direction=1):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Block2.png")
        self.image = pygame.transform.scale(self.image, (width, 20))
        self.moving = moving
        self.start_x = x
        self.move_counter = 0
        self.direction = direction  # Set initial direction (1 for right, -1 for left)
        self.speed = 3
        self.range = TILE_SIZE * 2  
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, platforms):
        if self.moving:
            original_x = self.rect.x
            self.rect.x += self.direction * self.speed

            for platform in platforms:
                if platform != self and self.rect.colliderect(platform.rect):
                    self.rect.x = original_x
                    self.direction *= -1  # Reverse direction
                    break

            if abs(self.rect.x - self.start_x) >= self.range:
                self.rect.x = original_x
                self.direction *= -1  # Reverse direction

class Player:
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load(f'guy{num}.png')
            img_right = pygame.transform.scale(img_right, (36, 60))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = False
        self.alive = True  # Track if the player is alive
        self.on_platform = False  # Track if the player is on a platform

    def update(self, platforms):
        if not self.alive:  # Stop updating if dead
            return

        dx = 0
        dy = 0
        walk_cooldown = 5

        # Get keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and not self.jumped and not self.in_air:
            self.vel_y = -20  
            self.jumped = True
            self.in_air = True  

        if not key[pygame.K_SPACE]:
            self.jumped = False

        if key[pygame.K_LEFT]:
            dx -= 5
            self.counter += 1
            self.direction = -1
        if key[pygame.K_RIGHT]:
            dx += 5
            self.counter += 1
            self.direction = 1
        if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
            self.counter = 0
            self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]

        # Handle animation
        if self.counter > walk_cooldown:
            self.counter = 0    
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]

        # Gravity
        self.vel_y += 1.4  
        if self.vel_y > 10:  
            self.vel_y = 10  

        dy += self.vel_y

        # Prevent player from moving out of screen
        if self.rect.x + dx < 0:
            dx = -self.rect.x  
        if self.rect.x + dx + self.width > WIDTH:
            dx = WIDTH - (self.rect.x + self.width)  

        # Check for collision with tiles
        self.in_air = True  
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:  
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:  
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air = False  

        # Check for collision with platforms
        self.on_platform = False
        for platform in platforms:
            if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:  
                    dy = platform.rect.bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:  
                    dy = platform.rect.top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air = False
                    self.on_platform = True
                    # Move player horizontally with the platform
                    if platform.moving:
                        self.rect.x += platform.direction * platform.speed

        # Update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        # Check if player falls off the screen
        if self.rect.top > HEIGHT:
            self.alive = False  # Mark the player as dead
            game_over()  # Call the game over function

        # Draw player
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

# Game over function
def game_over():
    screen.fill((0, 0, 0))  # Clear screen with black
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, (255, 0, 0))
    screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    pygame.display.update()
    pygame.time.delay(2000)  # Wait 2 seconds
    restart_game()  # Restart the game

# Function to restart the game
def restart_game():
    global player, world
    player = Player(100, HEIGHT - 150)  # Reset player position
    world = World(world_data)  # Reload world

class World:
    def __init__(self, data):
        self.tile_list = []
        self.platforms = pygame.sprite.Group()

        grass_img = pygame.image.load("Block2.png")  
        dirt_img = pygame.image.load("Dirt.png")
        dirt2_img = pygame.image.load("Block3.png")  

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:  
                if tile == 1:
                    img = pygame.transform.scale(grass_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.topleft = (col_count * TILE_SIZE, row_count * TILE_SIZE)
                    self.tile_list.append((img, img_rect))
                elif tile == 2:  
                    img = pygame.transform.scale(dirt_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.topleft = (col_count * TILE_SIZE, row_count * TILE_SIZE)
                    self.tile_list.append((img, img_rect))
                elif tile == 3:  
                    img = pygame.transform.scale(dirt2_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.topleft = (col_count * TILE_SIZE, row_count * TILE_SIZE)
                    self.tile_list.append((img, img_rect))
                elif tile == 4:  # Moving platform
                    platform = Platform(col_count * TILE_SIZE, row_count * TILE_SIZE, TILE_SIZE, True, direction=1)
                    self.platforms.add(platform)
                elif tile == 5:  # Moving platform in opposite direction
                    platform = Platform(col_count * TILE_SIZE, row_count * TILE_SIZE, TILE_SIZE, True, direction=-1)
                    self.platforms.add(platform)

                col_count += 1
            row_count += 1

    def draw(self, screen):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
        self.platforms.draw(screen)

# World data (platforms)
world_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 4, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 1, 1, 1, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 3],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3],
    [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3],
    [1, 1, 1, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2]
]

player = Player(100, HEIGHT - 150)  # Place player on the ground
world = World(world_data)

def main_menu():
    menu_font = pygame.font.Font(None, 74)
    start_text = menu_font.render("Start Game", True, (255, 255, 255))
    quit_text = menu_font.render("Quit", True, (255, 255, 255))

    while True:
        screen.fill((0, 0, 0))
        screen.blit(start_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        screen.blit(quit_text, (WIDTH // 2 - 50, HEIGHT // 2 + 50))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Quit the game
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if WIDTH // 2 - 100 <= mouse_pos[0] <= WIDTH // 2 + 100 and HEIGHT // 2 - 50 <= mouse_pos[1] <= HEIGHT // 2:
                    return True  # Start the game
                if WIDTH // 2 - 50 <= mouse_pos[0] <= WIDTH // 2 + 50 and HEIGHT // 2 + 50 <= mouse_pos[1] <= HEIGHT // 2 + 100:
                    return False  # Quit the game

# Game loop
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))
    world.draw(screen)
    player.update(world.platforms)
    for platform in world.platforms:
        platform.update(world.platforms)  # Pass the list of platforms to the update method
    draw_grid()
    pygame.display.update()

pygame.quit()

