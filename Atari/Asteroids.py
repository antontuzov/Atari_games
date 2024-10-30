import pygame
import random
import math


# initialize pygame
pygame.init()


# screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Asteroids')






#load images
spaceship_img = pygame.image.load('img/spaceship.png')
asteroid_img = pygame.image.load('img/asteroid.png')


# scale images
asteroid_img = pygame.transform.scale(asteroid_img, (50, 50))
spaceship_img = pygame.transform.scale(spaceship_img, (60, 60))




# Player class

class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 60
        self.angle = 90
        self.speed = 5
    
    def rotate(self, direction):
        self.angle += direction * 5
        
    def move_forward(self):
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y -= self.speed * math.sin(math.radians(self.angle))
        
        
        # wrap around screen edges
        self.x = self.x % SCREEN_WIDTH
        self.y = self.y % SCREEN_HEIGHT
        
    def draw(self):
        rotated_img = pygame.transform.rotate(spaceship_img, self.angle)
        rect = rotated_img.get_rect(center=(self.x, self.y))
        screen.blit(rotated_img, rect)
        
        
    
    

# Asteroid class

class Asteroid:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(-100,40)
        self.speed = random.uniform(1, 3)
        self.angle = random.uniform(0, 360)
        
    def move(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = random.randint(-100, 40)
            self.x = random.randint(0, SCREEN_WIDTH)
            
    def draw(self):
        rotated_img = pygame.transform.rotate(asteroid_img, self.angle)
        rect = rotated_img.get_rect(center=(self.x, self.y))
        screen.blit(rotated_img, rect)
        
        
        
        
# collision check function


def is_collision(player, asteroid):
    return math.hypot(player.x - asteroid.x, player.y - asteroid.y) < 30



# main game loop

def main():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 55)
    
    player = Player()
    asteroids = [Asteroid() for _ in range(5)]
    
    score = 0
    running = True
    game_over = False
    
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.rotate(-1)
        if keys[pygame.K_RIGHT]:
            player.rotate(1)
        if keys[pygame.K_UP]:
            player.move_forward()

        # Move and draw asteroids
        for asteroid in asteroids:
            asteroid.move()
            asteroid.draw()
            if is_collision(player, asteroid):
                game_over = True
                running = False

        # Draw player
        player.draw()

        # Display score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    # Game Over screen
    if game_over:
        screen.fill(BLACK)
        game_over_text = font.render("GAME OVER", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
        pygame.display.flip()
        pygame.time.wait(2000)

    pygame.quit()

# Run the game
if __name__ == "__main__":
    main()
        
        
       
    
    
    
           
        
    
    
        
    
        

 