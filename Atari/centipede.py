import pygame
import random


#initialize pygame
pygame.init()


#set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Centipede")


# load images
shooter_img = pygame.image.load('img/humanoid.png').convert_alpha()
centepede_seg_img = pygame.image.load('img/enemy1.png').convert_alpha()
mashroom_img = pygame.image.load('img/mashroom.png').convert_alpha()
bullet_img = pygame.image.load('img/bullet.png').convert_alpha()


# set up game veriables
shooter_width, shooter_height = shooter_img.get_size()
shooter_x = WIDTH // 2 - shooter_width // 2
shooter_y = HEIGHT - shooter_height - 10
shooter_speed = 5

# bullet veriables
bullet_speed = -10
bullets = []

# centipede veriables

centipede = []
centipede_speed = 1
centipede_length = 10
for i in range(centipede_length):
    centipede.append([random.randint(0, WIDTH - 40), i * 40])
    
    
# mashroom veriables
mashrooms = []
for _ in range(5):
    x = random.randint(0, WIDTH - 40)  # Assuming the mashroom is 40 pixels wide
    y = random.randint(0, HEIGHT - 100)
    mashrooms.append([x, y])

    
# game clock 
clock = pygame.time.Clock()

def draw_shooter(x, y):
    screen.blit(shooter_img, (x, y))

def draw_centipede(segment):
    screen.blit(centepede_seg_img, (segment[0], segment[1]))
    
def draw_mashroom(mashroom):
    screen.blit(mashroom_img, (mashroom[0], mashroom[1]))
    
def draw_bullet(bullet):
    screen.blit(bullet_img, (bullet[0], bullet[1]))
    

def main():
    global shooter_x
    running = True
    score = 0

    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and shooter_x > 0:
            shooter_x -= shooter_speed
        if keys[pygame.K_RIGHT] and shooter_x < WIDTH - shooter_width:
            shooter_x += shooter_speed
        if keys[pygame.K_SPACE]:
            bullets.append([shooter_x + shooter_width // 2 - 5, shooter_y])  # Adjust bullet position

        # Move bullet
        for bullet in bullets[:]:
            bullet[1] += bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)
                
        # Move centipede
        for segment in centipede[:]:
            segment[0] -= centipede_speed
            if segment[0] < 0:
                centipede.remove(segment)
                centipede.append([random.randint(0, WIDTH - 40), i * 40])
                score += 1
                break
            
            
            
        # draw shooter, centipede, bullet, mashroom
        draw_shooter(shooter_x, shooter_y)
        for segment in centipede:
            draw_centipede(segment)
            
        for bullet in bullets:
            draw_bullet(bullet)
            
        for mashroom in mashrooms:
            draw_mashroom(mashroom)
            
        # check for game over
        
        for segment in centipede:
            if segment[1] >= HEIGHT - shooter_height:
                print("Game Over! final score:", score)
                running = False
                break
            
        
        # check for collisions
        for bullet in bullets:
            for segment in centipede:
                if bullet[0] >= segment[0] and bullet[0] <= segment[0] + 40 and bullet[1] >= segment[1] and bullet[1] <= segment[1] + 40:
                    centipede.remove(segment)
                    bullets.remove(bullet)
                    score += 1
                    break
                
                
        # collision with mashroom
        for segment in centipede:
            for mashroom in mashrooms:
                if segment[0] >= mashroom[0] and segment[0] <= mashroom[0] + 40 and segment[1] >= mashroom[1] and segment[1] <= mashroom[1] + 100:
                    centipede.remove(segment)
                    score += 1
                    break
                
        
            
            
            
        # dysplay score
        font = pygame.font.SysFont(None, 30)
        text = font.render("Score: " + str(score), True, (255, 255, 255))
        screen.blit(text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()
    


if __name__ == "__main__":
    main()
        

            
               
                
                
    
    
    








