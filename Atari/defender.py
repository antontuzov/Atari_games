import pygame
import random

#initialize pygame
pygame.init()

#set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Defender")


# load images
player_img = pygame.image.load('img/player.png')
enemy_img = pygame.image.load('img/enemy1.png')
bullet_img = pygame.image.load('img/bullet1.png')
humanoid_img = pygame.image.load('img/humanoid.png')


# set up player properties
player_width = player_img.get_size()
player_height = player_img.get_size()
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 10


# set up bullet properties
bullet_width = bullet_img.get_size()
bullet_height = bullet_img.get_size()
bullet_speed = -10


# set up enemy properties
enemy_width = humanoid_img.get_size()
enemy_height = humanoid_img.get_size()
enemy_speed = 5

enemies = []

# Set up humanoid properties
humanoid_width, humanoid_height = humanoid_img.get_size()
humanoids = []

# game clock
clock = pygame.time.Clock()

def draw_player(x, y):
    screen.blit(player_img, (x, y))
    
def draw_bullet(bullet):
    screen.blit(bullet_img, (bullet[0], bullet[1]))
    
    
    
def draw_enemy(enemy):
    screen.blit(enemy_img, (enemy[0], enemy[1]))
    

def draw_humanoid(humanoid):
    screen.blit(humanoid_img, (humanoid[0], humanoid[1]))
    
    
def spawn_enemy():
    x = random.randint(0, WIDTH - enemy_width)
    return [x, 0]

def spawn_humanoid():
    x = random.randint(0, WIDTH - humanoid_width)
    return [x, random.randint(50, 400)]


def main ():
    global player_x
    ruunning = True
    score = 0
    
    
    
    # spawn enemies
    for _ in range(3):
        enemies.append(spawn_enemy())
        
    # spawn humanoids
    for _ in range(3):
        humanoids.append(spawn_humanoid())
        
    
    
    
