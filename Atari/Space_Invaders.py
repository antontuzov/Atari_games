import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load player and enemy images
player_img = pygame.image.load('img/player.png')
enemy_img = pygame.image.load('img/enemy.png')
bullet_img = pygame.image.load('img/bullet.png')

# Player class
class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2 - 32
        self.y = SCREEN_HEIGHT - 100
        self.x_speed = 0
        self.speed = 7
        self.rect = pygame.Rect(self.x, self.y, 64, 64)

    def move(self):
        self.x += self.x_speed
        self.x = max(0, min(SCREEN_WIDTH - 64, self.x))
        self.rect = pygame.Rect(self.x, self.y, 64, 64)

    def draw(self):
        screen.blit(player_img, (self.x, self.y))

# Bullet class
class Bullet:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.y_speed = -10
        self.state = "ready"  # "ready" means not visible, "fire" means bullet is moving
        self.rect = pygame.Rect(self.x, self.y, 32, 32)

    def fire(self, x, y):
        self.state = "fire"
        self.x = x + 16  # Adjust to center bullet
        self.y = y - 20

    def move(self):
        if self.state == "fire":
            self.y += self.y_speed
            self.rect = pygame.Rect(self.x, self.y, 32, 32)
        if self.y < 0:
            self.state = "ready"

    def draw(self):
        if self.state == "fire":
            screen.blit(bullet_img, (self.x, self.y))

# Enemy class
class Enemy:
    def __init__(self):
        self.x = random.randint(50, SCREEN_WIDTH - 50)
        self.y = random.randint(50, 150)
        self.x_speed = random.choice([-5, 5])
        self.y_speed = 40
        self.rect = pygame.Rect(self.x, self.y, 64, 64)

    def move(self):
        self.x += self.x_speed
        if self.x <= 0 or self.x >= SCREEN_WIDTH - 64:
            self.x_speed *= -1
            self.y += self.y_speed
        self.rect = pygame.Rect(self.x, self.y, 64, 64)

    def draw(self):
        screen.blit(enemy_img, (self.x, self.y))

# Function to check collision between bullet and enemy
def is_collision(bullet, enemy):
    return bullet.rect.colliderect(enemy.rect)

# Main game loop
def main():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 55)

    # Load images
    global player_img, enemy_img, bullet_img
    player_img = pygame.image.load("img/player.png")
    enemy_img = pygame.image.load("img/enemy.png")
    bullet_img = pygame.image.load("img/bullet.png")

    # Player, enemies, and bullet initialization
    player = Player()
    bullet = Bullet()
    enemies = [Enemy() for _ in range(6)]  # Create 6 enemies

    score = 0
    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Player movement input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.x_speed = -player.speed
                if event.key == pygame.K_RIGHT:
                    player.x_speed = player.speed
                if event.key == pygame.K_SPACE and bullet.state == "ready":
                    bullet.fire(player.x, player.y)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.x_speed = 0

        # Move and draw player
        player.move()
        player.draw()

        # Move and draw bullet
        bullet.move()
        bullet.draw()

        # Move and draw enemies
        for enemy in enemies:
            enemy.move()
            enemy.draw()

            # Check for collision with bullet
            if bullet.state == "fire" and is_collision(bullet, enemy):
                bullet.state = "ready"
                score += 1
                enemies.remove(enemy)
                enemies.append(Enemy())  # Replace the enemy

            # Check for enemy reaching the player
            if enemy.y >= SCREEN_HEIGHT - 100:
                running = False

        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Start the game
if __name__ == "__main__":
    main()
