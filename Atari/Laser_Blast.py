import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Laser Blast")

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Set up player properties
player_width = 50
player_height = 10
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 50
player_speed = 10

# Set up bullet properties
bullet_width = 5
bullet_height = 10
bullet_speed = -15

# Initialize bullet list
bullets = []

# Set up target properties
target_width = 50
target_height = 30
target_speed = 5
target_spawn_time = 30  # Frames before a new target spawns
targets = []

# Game clock
clock = pygame.time.Clock()

def draw_player(x, y):
    pygame.draw.rect(screen, WHITE, (x, y, player_width, player_height))

def draw_bullet(bullet):
    pygame.draw.rect(screen, RED, (bullet[0], bullet[1], bullet_width, bullet_height))

def draw_target(target):
    pygame.draw.rect(screen, WHITE, (target[0], target[1], target_width, target_height))

def main():
    global player_x, player_y
    running = True
    score = 0
    frame_count = 0

    while running:
        screen.fill(BLACK)

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

        # Target spawning logic
        if frame_count % target_spawn_time == 0:
            target_x = random.randint(0, WIDTH - target_width)
            targets.append([target_x, 0])

        # Move targets and check for collisions
        for target in targets[:]:
            target[1] += target_speed
            if target[1] > HEIGHT:
                targets.remove(target)
            # Check for bullet collision
            for bullet in bullets[:]:
                if (target[0] < bullet[0] < target[0] + target_width and
                        target[1] < bullet[1] < target[1] + target_height):
                    targets.remove(target)
                    bullets.remove(bullet)
                    score += 1
                    break

        # Draw player, bullets, and targets
        draw_player(player_x, player_y)
        for bullet in bullets:
            draw_bullet(bullet)
        for target in targets:
            draw_target(target)

        # Display score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)
        frame_count += 1

    pygame.quit()

if __name__ == "__main__":
    main()
 
    
            
        
    
    


