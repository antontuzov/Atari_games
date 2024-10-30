import pygame
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
TILE_SIZE = 20

# Colors
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
WALL_COLOR = (50, 50, 255)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man")

# Load Pac-Man animation frames
pacman_frames = [
    pygame.image.load("img/pacman_open.png").convert_alpha(),
    pygame.image.load("img/pacman_half.png").convert_alpha(),
    pygame.image.load("img/pacman_closed.png").convert_alpha()
]
ghost_img = pygame.image.load("img/ghost.png").convert_alpha()

# Maze Layout (1: Wall, 0: Path)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Define Pac-Man with animation
class PacMan:
    def __init__(self):
        self.x, self.y = TILE_SIZE, TILE_SIZE
        self.speed = TILE_SIZE
        self.direction = "RIGHT"
        self.frames = pacman_frames
        self.current_frame = 0
        self.animation_delay = 5  # Frames to wait before changing animation
        self.animation_counter = 0

    def move(self, maze):
        dx, dy = 0, 0
        if self.direction == "LEFT": dx = -self.speed
        elif self.direction == "RIGHT": dx = self.speed
        elif self.direction == "UP": dy = -self.speed
        elif self.direction == "DOWN": dy = self.speed

        # Check maze boundaries
        new_x, new_y = self.x + dx, self.y + dy
        if not maze[int(new_y / TILE_SIZE)][int(new_x / TILE_SIZE)] == 1:
            self.x, self.y = new_x, new_y

    def animate(self):
        # Update animation frame
        self.animation_counter += 1
        if self.animation_counter >= self.animation_delay:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.animation_counter = 0

    def draw(self):
        # Draw current frame of animation
        screen.blit(self.frames[self.current_frame], (self.x, self.y))

# Define Ghost (same as before, for simplicity)
class Ghost:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.speed = TILE_SIZE
        self.img = ghost_img

    def move_towards(self, target_x, target_y, maze):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.hypot(dx, dy)
        if distance == 0:
            return  # Pac-Man and Ghost are at the same position

        if abs(dx) > abs(dy):
            step_x = self.speed if dx > 0 else -self.speed
            new_x = self.x + step_x
            if maze[int(self.y / TILE_SIZE)][int(new_x / TILE_SIZE)] != 1:
                self.x = new_x
            else:
                self.y += self.speed if dy > 0 else -self.speed
        else:
            step_y = self.speed if dy > 0 else -self.speed
            new_y = self.y + step_y
            if maze[int(new_y / TILE_SIZE)][int(self.x / TILE_SIZE)] != 1:
                self.y = new_y
            else:
                self.x += self.speed if dx > 0 else -self.speed

    def draw(self):
        screen.blit(self.img, (self.x, self.y))

# Pellet class
class Pellet:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.eaten = False

    def draw(self):
        if not self.eaten:
            pygame.draw.circle(screen, WHITE, (self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2), TILE_SIZE // 4)

# Initialize game objects
pacman = PacMan()
ghosts = [Ghost(300, 300), Ghost(400, 300)]
pellets = [Pellet(x * TILE_SIZE, y * TILE_SIZE) for x in range(20) for y in range(5) if maze[y][x] == 0]

# Game loop variables
clock = pygame.time.Clock()
score = 0
running = True

# Main game loop
while running:
    screen.fill(BLACK)
    
    # Draw maze
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == 1:
                pygame.draw.rect(screen, WALL_COLOR, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pacman.direction = "LEFT"
            elif event.key == pygame.K_RIGHT:
                pacman.direction = "RIGHT"
            elif event.key == pygame.K_UP:
                pacman.direction = "UP"
            elif event.key == pygame.K_DOWN:
                pacman.direction = "DOWN"

    # Move and animate Pac-Man
    pacman.move(maze)
    pacman.animate()

    # Move ghosts
    for ghost in ghosts:
        ghost.move_towards(pacman.x, pacman.y, maze)

    # Check for collisions with pellets
    for pellet in pellets:
        if not pellet.eaten and pacman.x == pellet.x and pacman.y == pellet.y:
            pellet.eaten = True
            score += 1

    # Check for collisions with ghosts
    for ghost in ghosts:
        if pacman.x == ghost.x and pacman.y == ghost.y:
            running = False  # Game Over

    # Draw pellets, Pac-Man, and ghosts
    for pellet in pellets:
        pellet.draw()
    pacman.draw()
    for ghost in ghosts:
        ghost.draw()

    # Draw score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, BLUE)
    screen.blit(score_text, (10, 10))

    # Update the screen
    pygame.display.flip()
    clock.tick(10)

pygame.quit()
