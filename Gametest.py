import pygame

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 1501, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Platform Game')

# Choose a proportional tile size   
TILE_SIZE = 60  # Proportional size based on GCD

# Load and scale background image
background = pygame.image.load("Sky3.jpg")  
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

def draw_grid():
    """Draws a grid with proportional tiles."""
    for x in range(0, WIDTH, TILE_SIZE):  # Vertical lines
        pygame.draw.line(screen, (255, 255, 255), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILE_SIZE):  # Horizontal lines
        pygame.draw.line(screen, (255, 255, 255), (0, y), (WIDTH, y))

class Player():
    def __init__(self, x, y):
        img = pygame.image.load("guy1.png")
        self.image = pygame.transform.scale(img, (36, 60))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 1.1  # Vertical velocity (for gravity and jumping)
        self.jump = False  # Track if the player is jumping
        self.speed = 2  # Horizontal movement speed
        self.jump_force = -5.7 # Initial jump force (higher)
        self.gravity_up = 0.10  # Weak gravity during ascent (slower jump)
        self.gravity_down = 0.1  # Stronger gravity during descent (faster fall)

    def move(self, world):
        # Get key presses
        keys = pygame.key.get_pressed()

        # Horizontal movement
        dx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: 
            dx = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: 
            dx = self.speed

        # Jumping
        if keys[pygame.K_SPACE] and not self.jump:
            self.vel_y = self.jump_force  # Jump with new jump force
            self.jump = True  

        # Apply gravity (slower ascent, faster descent)
        if self.vel_y < 0:
            self.vel_y += self.gravity_up  # Apply weaker gravity while jumping up
        else:
            self.vel_y += self.gravity_down  # Apply stronger gravity while falling

        if self.vel_y > 10:
            self.vel_y = 10  # Terminal velocity

        dy = self.vel_y

        def draw(self, screen):
            """Draws the player on the screen along with a rectangle."""
            # Draw the player image
            screen.blit(self.image, self.rect)
    

        # Horizontal collision check
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0  # Stop moving horizontally if colliding

        # Vertical collision check
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                if self.vel_y > 0:  # Falling down
                    dy = tile[1].top - self.rect.bottom  # Prevent falling into the tile
                    self.vel_y = 0
                    self.jump = False  # Reset jumping when landing
                elif self.vel_y < 0:  # Hitting the ceiling
                    dy = tile[1].bottom - self.rect.top  # Prevent moving into the ceiling
                    self.vel_y = 0

        # Boundary checks
        if self.rect.x + dx < 0:  # Left boundary
            dx = 0
        if self.rect.x + dx > WIDTH - self.rect.width:  # Right boundary
            dx = 0
        if self.rect.y + dy > HEIGHT - self.rect.height:  # Bottom boundary
            dy = 0
            self.jump = False  # Allow jumping when standing on ground

        # Apply movement
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, screen):
        """Draws the player on the screen."""
        screen.blit(self.image, self.rect)


class World():
    def __init__(self, data):
        self.tile_list = []

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
                col_count += 1
            row_count += 1

    def draw(self, screen):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

# World data (platforms)
# World data (matching tile size 60px)
world_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
    
]

# Now the world layout is 25 tiles wide by 12 tiles high.

player = Player(100, HEIGHT - 150)  # Place player on the ground
world = World(world_data)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))
    world.draw(screen)
    draw_grid()
    player.move(world)  # Move the player
    player.draw(screen)  # Draw the player on the screen
    
    pygame.display.update()

pygame.quit()
