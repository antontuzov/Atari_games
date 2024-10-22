import pygame
import random



#initialize pygame
pygame.init()


#global variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)


#paddle dimensions
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
PADDLE_VEL = 50


#ball dimensions
BALL_RADIUS = 8
BALL_VEL = 5


#Brick seting
BRICK_WIDTH = 75
BRICK_HEIGHT = 20
BRICK_VEL = 5
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_OFFSET_TOP = 50
BRICK_PADDING = 5


#game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Breakout')



#paddle class
class Paddle:
    def __init__(self):
        self.x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
        self.y = SCREEN_HEIGHT - 40 
        self.vel = PADDLE_VEL
        self.rect = pygame.Rect(self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT)
        
    def move(self, derection):
        if derection == 'left' and self.x > 0:
            self.x -= self.vel
        if derection == 'right' and self.x < SCREEN_WIDTH - PADDLE_WIDTH:
            self.x += self.vel
        self.rect = pygame.Rect(self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT)
        
    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)
        

#ball class
class Ball:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.x_vel = random.choice([-BALL_VEL, BALL_VEL])
        self.y_vel = -BALL_VEL
        self.rect = pygame.Rect(self.x - BALL_RADIUS, self.y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
        
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        
        
        #Bounce off the walls
        if self.x <= 0 or self.x >= SCREEN_WIDTH - BALL_RADIUS * 2:
            self.x_vel *= -1
        if self.y <= 0:
            self.y_vel *= -1
        self.rect = pygame.Rect(self.x - BALL_RADIUS, self.y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
        
        
    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), BALL_RADIUS)
        
    def reset(self):
        self.__init__()
        
        
        
    
    #brick class
    
    
class Brick:
        def __init__(self, x,y, color):
            self.x = x
            self.y = y
            self.color = color
            self.rect = pygame.Rect(self.x, self.y, BRICK_WIDTH, BRICK_HEIGHT)
            
        def draw(self):
            pygame.draw.rect(screen, self.color, self.rect)
            
            
            
            
# Function to create the bricks
def create_bricks():
    bricks = []
    colors = [RED, GREEN, BLUE]
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            x = col * (BRICK_WIDTH + BRICK_PADDING) + BRICK_PADDING
            y = row * (BRICK_HEIGHT + BRICK_PADDING) + BRICK_OFFSET_TOP
            brick = Brick(x, y, random.choice(colors))
            bricks.append(brick)
    return bricks
      
      
      
#cheack for collision
def check_collision(ball, paddle, bricks):
    if ball.rect.colliderect(paddle.rect):
        ball.y_vel *= -1
        
    for brick in bricks:
        if ball.rect.colliderect(brick.rect):
            ball.y_vel *= -1
            bricks.remove(brick)
    return bricks


#game loop

def main():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 55)
    
    #paddle, ball and bricks initialization
    paddle = Paddle()
    ball = Ball()
    bricks = create_bricks()
    
   # Game veriables
    score = 0
    lives = 3
    ruuning = True
    
    
    while ruuning:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ruuning = False
                pygame.display.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    paddle.move('left')
                if event.key == pygame.K_RIGHT:
                    paddle.move('right')
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    paddle.move('stop')
                    
        #move ball
        ball.move()
        
        #check for collision
        bricks = check_collision(ball, paddle, bricks)
        
        #Ball hits the bottom
        if ball.y >= SCREEN_HEIGHT - BALL_RADIUS * 2:
            lives -= 1
            ball.reset()
        
        #draw paddle, ball and bricks
        paddle.draw()
        ball.draw()
        for brick in bricks:
            brick.draw()
            
        #display score and lives
        text = font.render('Score: ' + str(score), True, WHITE)
        screen.blit(text, (SCREEN_WIDTH - 150, 10))
        text = font.render('Lives: ' + str(lives), True, WHITE)
        screen.blit(text, (10, 10))
        
        pygame.display.update()
        clock.tick(60)
        
    pygame.quit()
    
    
  
  
  
    
    
#start game
if __name__ == '__main__':
    main()
    
    
        

            
      
    

   
    
        

        

        
        
      

