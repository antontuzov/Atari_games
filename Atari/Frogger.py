import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Frogger")

# Define player (frog)
class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2 - 25
        self.y = SCREEN_HEIGHT - 50
        self.width = 50
        self.height = 50
        self.speed = 50
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.rect.topleft = (self.x, self.y)

        # Prevent the player from going out of the screen
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.rect)

# Define the car class (obstacles)
class Car:
    def __init__(self, x, y, width, height, speed, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.x += self.speed
        if self.speed > 0 and self.x > SCREEN_WIDTH:  # Move right
            self.x = -self.width
        if self.speed < 0 and self.x < -self.width:  # Move left
            self.x = SCREEN_WIDTH
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

# Create the lanes with cars
def create_cars():
    cars = []
    car_width, car_height = 80, 50
    lane_height = 100
    for i in range(1, 6):  # Five lanes of cars
        y = i * lane_height
        speed = random.choice([5, -5])  # Some cars move left, some move right
        color = random.choice([RED, BLUE])
        for j in range(3):  # Three cars per lane
            x = j * 300 + random.randint(0, 100)
            cars.append(Car(x, y, car_width, car_height, speed, color))
    return cars

# Function to check collision between frog and car
def is_collision(player, car):
    return player.rect.colliderect(car.rect)

# Main game loop
def main():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 55)

    # Player (frog) initialization
    player = Player()

    # Cars (obstacles) initialization
    cars = create_cars()

    # Variables to control game state
    score = 0
    running = True
    game_over = False

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Player movement input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move(-1, 0)
                if event.key == pygame.K_RIGHT:
                    player.move(1, 0)
                if event.key == pygame.K_UP:
                    player.move(0, -1)
                if event.key == pygame.K_DOWN:
                    player.move(0, 1)

        # Move and draw cars
        for car in cars:
            car.move()
            car.draw()

            # Check collision between frog and car
            if is_collision(player, car):
                game_over = True
                running = False

        # Draw player (frog)
        player.draw()

        # Check if player reaches the top (wins the level)
        if player.y <= 0:
            score += 1
            player = Player()  # Reset frog position
            cars = create_cars()  # Recreate the cars for a new level

        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    if game_over:
        # Display game over message
        screen.fill(BLACK)
        game_over_text = font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
        pygame.display.flip()
        pygame.time.wait(2000)

    pygame.quit()

# Start the game
if __name__ == "__main__":
    main()
