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


# Set up player properties
player_width, player_height = player_img.get_size()
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 10

# Set up bullet properties
bullet_width, bullet_height = bullet_img.get_size()
bullet_speed = -10
bullets = []

# Set up enemy properties
enemy_width, enemy_height = enemy_img.get_size()
enemy_speed = 3
enemies = []

# Set up humanoid properties
humanoid_width, humanoid_height = humanoid_img.get_size()
humanoids = []

# Game clock
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

def main():
    global player_x
    running = True
    score = 0

    # Spawn initial enemies
    for _ in range(5):
        enemies.append(spawn_enemy())
    
    # Spawn initial humanoids
    for _ in range(3):
        humanoids.append(spawn_humanoid())

    

    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed
        if keys[pygame.K_SPACE]:
            bullets.append([player_x + player_width // 2 - bullet_width // 2, player_y])

        # Move bullets
        for bullet in bullets[:]:
            bullet[1] += bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)

        # Move enemies and check for collisions
        for enemy in enemies[:]:
            enemy[1] += enemy_speed
            if enemy[1] > HEIGHT:
                enemies.remove(enemy)  # Remove enemy if it goes off the screen
            # Check for bullet collision
            for bullet in bullets[:]:
                if (enemy[0] < bullet[0] < enemy[0] + enemy_width and
                        enemy[1] < bullet[1] < enemy[1] + enemy_height):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 1
                    break

        # Move humanoids and check for collisions
        for humanoid in humanoids[:]:
            humanoid[1] += enemy_speed
            if humanoid[1] > HEIGHT:
                humanoids.remove(humanoid)  # Remove humanoid if it goes off the screen

            # Check for enemy collision
            for enemy in enemies:
                if (humanoid[0] < enemy[0] < humanoid[0] + humanoid_width and
                        humanoid[1] < enemy[1] < humanoid[1] + humanoid_height):
                    humanoids.remove(humanoid)
                    enemies.remove(enemy)
                    score -= 1  # Lose score for enemy hitting humanoid
                    break

        # Draw player, bullets, enemies, and humanoids
        draw_player(player_x, player_y)
        for bullet in bullets:
            draw_bullet(bullet)
        for enemy in enemies:
            draw_enemy(enemy)
        for humanoid in humanoids:
            draw_humanoid(humanoid)

        # Display score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

        # Spawn new enemies and humanoids occasionally
        if random.randint(1, 100) < 5:  # 5% chance to spawn a new enemy
            enemies.append(spawn_enemy())
        if random.randint(1, 100) < 3:  # 3% chance to spawn a new humanoid
            humanoids.append(spawn_humanoid())

    pygame.quit()

if __name__ == "__main__":
    main()
                    
            
            
        
                
        
                
     
           
        
    
        
        
        
    
    
    
