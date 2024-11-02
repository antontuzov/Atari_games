import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Donkey Kong")

# Load images
background_image = pygame.image.load("img/bg.png").convert()
player_image = pygame.image.load("img/player.png").convert_alpha()
kong_image = pygame.image.load("img/authority.png").convert_alpha()
barrel_image = pygame.image.load("img/et.png").convert_alpha()
ladder_image = pygame.image.load("img/ladder.png").convert_alpha()
platform_image = pygame.image.load("img/81.png").convert_alpha()

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Player settings
player_x, player_y = WIDTH // 2, HEIGHT - 80
player_speed = 5
player_jumping = False
player_jump_speed = 10
gravity = 0.5
player_dy = 0  # Vertical speed for jumping

# Barrel settings
barrel_speed = 3
barrels = []

# Game clock
clock = pygame.time.Clock()

# Load fonts
font = pygame.font.SysFont(None, 36)
title_font = pygame.font.SysFont(None, 72)

def main_menu():
    while True:
        screen.fill(BLACK)
        title_text = title_font.render("Donkey Kong", True, WHITE)
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

def draw_background():
    screen.blit(background_image, (0, 0))

def draw_player(x, y):
    screen.blit(player_image, (x, y))

def draw_kong(x, y):
    screen.blit(kong_image, (x, y))

def draw_barrel(barrel):
    screen.blit(barrel_image, (barrel[0], barrel[1]))

def draw_platform(x, y):
    screen.blit(platform_image, (x, y))

def draw_ladder(x, y):
    screen.blit(ladder_image, (x, y))

def game(level):
    global player_x, player_y, player_dy, player_jumping
    running = True
    score = 0

    # Kong position
    kong_x, kong_y = WIDTH // 2 - 50, 50

    # Platforms and ladders for level
    platforms = [[50, HEIGHT - 100, WIDTH - 100, 20], [50, HEIGHT - 300, WIDTH - 100, 20]]
    ladders = [[150, HEIGHT - 180, 20, 120], [WIDTH - 200, HEIGHT - 380, 20, 120]]

    while running:
        draw_background()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player movement and jumping
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_image.get_width():
            player_x += player_speed
        if keys[pygame.K_SPACE] and not player_jumping:
            player_jumping = True
            player_dy = -player_jump_speed

        # Apply gravity for jumping
        if player_jumping:
            player_y += player_dy
            player_dy += gravity
            if player_y >= HEIGHT - 80:
                player_y = HEIGHT - 80
                player_jumping = False

        # Move barrels
        for barrel in barrels:
            barrel[0] += barrel_speed
            if barrel[0] > WIDTH:
                barrels.remove(barrel)
            elif player_x < barrel[0] < player_x + player_image.get_width() and player_y < barrel[1] < player_y + player_image.get_height():
                print("Game Over!")
                running = False

        # Add new barrels randomly
        if random.randint(1, 60) == 1:
            barrels.append([kong_x, kong_y + 50])

        # Draw elements
        draw_kong(kong_x, kong_y)
        draw_player(player_x, player_y)
        for platform in platforms:
            draw_platform(platform[0], platform[1])
        for ladder in ladders:
            draw_ladder(ladder[0], ladder[1])
        for barrel in barrels:
            draw_barrel(barrel)

        # Check for level completion
        if player_y < 100:
            print("Level Complete!")
            return

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def main():
    main_menu()
    level = 1

    while True:
        game(level)
        level += 1

        # Level transition
        screen.fill(BLACK)
        level_up_text = font.render(f"Level {level}", True, WHITE)
        continue_text = font.render("Press Enter to Continue", True, WHITE)

        screen.blit(level_up_text, (WIDTH // 2 - level_up_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT // 2 + 50))
        pygame.display.flip()

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
