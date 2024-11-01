import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load images
player_image = pygame.image.load("img/player.png").convert_alpha()
alien_image = pygame.image.load("img/enemy.png").convert_alpha()
bullet_image = pygame.image.load("img/bullet.png").convert_alpha()

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Player settings
player_width, player_height = player_image.get_size()
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 5

# Bullet settings
bullet_speed = -10
bullets = []

# Alien settings
alien_speed = 5
alien_rows = 3
alien_cols = 8
aliens = []

# Initialize game clock
clock = pygame.time.Clock()

# Load fonts
font = pygame.font.SysFont(None, 36)
title_font = pygame.font.SysFont(None, 72)

def create_aliens(rows, cols):
    aliens = []
    for row in range(rows):
        for col in range(cols):
            x = 50 + col * 60
            y = 50 + row * 60
            aliens.append([x, y])
    return aliens

def draw_player(x, y):
    screen.blit(player_image, (x, y))

def draw_alien(alien):
    screen.blit(alien_image, (alien[0], alien[1]))

def draw_bullet(bullet):
    screen.blit(bullet_image, (bullet[0], bullet[1]))

def main_menu():
    while True:
        screen.fill(BLACK)
        title_text = title_font.render("Space Invaders", True, WHITE)
        start_text = font.render("Press Enter to Start", True, WHITE)
        exit_text = font.render("Press Esc to Exit", True, WHITE)

        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
        screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def game(level):
    global player_x
    running = True
    score = 0
    aliens = create_aliens(alien_rows + level, alien_cols)
    alien_direction = 1

    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed
        if keys[pygame.K_SPACE]:
            if len(bullets) < 3:  # Limit number of bullets on screen
                bullets.append([player_x + player_width // 2, player_y])

        # Move bullets
        for bullet in bullets[:]:
            bullet[1] += bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)

        # Move aliens
        move_down = False
        for alien in aliens:
            alien[0] += alien_speed * alien_direction
            if alien[0] <= 0 or alien[0] >= WIDTH - 40:
                move_down = True

        if move_down:
            alien_direction *= -1
            for alien in aliens:
                alien[1] += 20 + level * 5

        # Check for bullet collisions with aliens
        for bullet in bullets[:]:
            for alien in aliens[:]:
                if alien[0] < bullet[0] < alien[0] + 40 and alien[1] < bullet[1] < alien[1] + 40:
                    bullets.remove(bullet)
                    aliens.remove(alien)
                    score += 1
                    break

        # Draw everything
        draw_player(player_x, player_y)
        for bullet in bullets:
            draw_bullet(bullet)
        for alien in aliens:
            draw_alien(alien)

        # Display score and level
        score_text = font.render(f'Score: {score}', True, WHITE)
        level_text = font.render(f'Level: {level}', True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (WIDTH - 100, 10))

        # Check for level completion
        if not aliens:
            return score

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def main():
    main_menu()
    level = 1
    total_score = 0

    while True:
        level_score = game(level)
        total_score += level_score
        level += 1

        # Level transition
        screen.fill(BLACK)
        level_up_text = font.render(f"Level {level}", True, WHITE)
        total_score_text = font.render(f"Score: {total_score}", True, WHITE)
        continue_text = font.render("Press Enter to Continue", True, WHITE)

        screen.blit(level_up_text, (WIDTH // 2 - level_up_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(total_score_text, (WIDTH // 2 - total_score_text.get_width() // 2, HEIGHT // 2))
        screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT // 2 + 50))
        pygame.display.flip()

        # Wait for player to continue to the next level
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting = False

if __name__ == "__main__":
    main()

        
        
        
        
        
       
       
                
                
            
                
                
                        
                
            
                
            
            
     
        
    
    
    
    
    
       
        
        
   
   










