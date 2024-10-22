import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BALL_RADIUS = 15
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong')

# Paddle class
class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10
        self.rect = pygame.Rect(self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, up=True):
        if up:
            self.y -= self.speed
        else:
            self.y += self.speed
        self.y = max(0, min(SCREEN_HEIGHT - PADDLE_HEIGHT, self.y))
        self.rect = pygame.Rect(self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

# Ball class
class Ball:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.x_speed = random.choice([-5, 5])
        self.y_speed = random.choice([-5, 5])
        self.rect = pygame.Rect(self.x - BALL_RADIUS, self.y - BALL_RADIUS, BALL_RADIUS*2, BALL_RADIUS*2)

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed
        if self.y <= 0 or self.y >= SCREEN_HEIGHT - BALL_RADIUS * 2:
            self.y_speed *= -1
        self.rect = pygame.Rect(self.x - BALL_RADIUS, self.y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), BALL_RADIUS)

    def reset(self):
        self.__init__()

# Function to check collision between paddles and ball
def check_collision(ball, paddle1, paddle2):
    if ball.rect.colliderect(paddle1.rect) or ball.rect.colliderect(paddle2.rect):
        ball.x_speed *= -1

# Main game loop
def main():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 55)

    # Paddle and ball initialization
    paddle1 = Paddle(30, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
    paddle2 = Paddle(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ball = Ball()

    # Scores
    score1 = 0
    score2 = 0

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Player 1 controls (W/S)
        if keys[pygame.K_w]:
            paddle1.move(up=True)
        if keys[pygame.K_s]:
            paddle1.move(up=False)

        # Player 2 controls (UP/DOWN)
        if keys[pygame.K_UP]:
            paddle2.move(up=True)
        if keys[pygame.K_DOWN]:
            paddle2.move(up=False)

        # Move the ball
        ball.move()

        # Check for paddle collisions
        check_collision(ball, paddle1, paddle2)

        # Score handling
        if ball.x < 0:
            score2 += 1
            ball.reset()
        if ball.x > SCREEN_WIDTH:
            score1 += 1
            ball.reset()

        # Draw paddles, ball, and score
        paddle1.draw()
        paddle2.draw()
        ball.draw()

        # Display score
        score_text = font.render(f"{score1} - {score2}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Start the game
if __name__ == '__main__':
    main()

        
        
        
        
    
    
    
        
        
        
       
        
        
    
