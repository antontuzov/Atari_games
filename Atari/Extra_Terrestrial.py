import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("E.T. the Extra-Terrestrial")

# Load images
et_image = pygame.image.load("img/et.png").convert_alpha()
phone_piece_image = pygame.image.load("img/enemy1.png").convert_alpha()
authority_image = pygame.image.load("img/authority.png").convert_alpha()

# Set up colors
BLACK = (0, 0, 0)

# Game variables
et_x = WIDTH // 2
et_y = HEIGHT - 70
et_speed = 5

# Phone pieces
phone_pieces = []
for _ in range(5):
    x = random.randint(0, WIDTH - 40)  # Assuming the phone piece is 40 pixels wide
    y = random.randint(0, HEIGHT - 100)
    phone_pieces.append([x, y])

# Authorities
authorities = []
for _ in range(3):
    x = random.randint(0, WIDTH - 40)
    authorities.append([x, 0])  # Start from the top

# Game clock
clock = pygame.time.Clock()

def draw_et(x, y):
    screen.blit(et_image, (x, y))

def draw_phone_piece(phone_piece):
    screen.blit(phone_piece_image, (phone_piece[0], phone_piece[1]))

def draw_authority(authority):
    screen.blit(authority_image, (authority[0], authority[1]))

def main():
    global et_x, et_y
    running = True
    score = 0

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and et_x > 0:
            et_x -= et_speed
        if keys[pygame.K_RIGHT] and et_x < WIDTH - 40:  # Assuming E.T. is 40 pixels wide
            et_x += et_speed
        if keys[pygame.K_UP] and et_y > 0:
            et_y -= et_speed
        if keys[pygame.K_DOWN] and et_y < HEIGHT - 70:  # Assuming E.T. is 70 pixels tall
            et_y += et_speed

        # Move authorities
        for authority in authorities:
            authority[1] += 2  # Move down
            if authority[1] > HEIGHT:  # Reset position
                authority[1] = 0
                authority[0] = random.randint(0, WIDTH - 40)

        # Check for collisions with phone pieces
        for phone_piece in phone_pieces[:]:
            if (phone_piece[0] < et_x < phone_piece[0] + 40 and
                phone_piece[1] < et_y < phone_piece[1] + 40):
                phone_pieces.remove(phone_piece)
                score += 1

        # Check for collisions with authorities
        for authority in authorities:
            if (authority[0] < et_x < authority[0] + 40 and
                authority[1] < et_y < authority[1] + 40):
                print("Game Over! Final Score:", score)
                running = False

        # Draw E.T., phone pieces, and authorities
        draw_et(et_x, et_y)
        for phone_piece in phone_pieces:
            draw_phone_piece(phone_piece)
        for authority in authorities:
            draw_authority(authority)

        # Display score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
