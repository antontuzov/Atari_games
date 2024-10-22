import pygame
import random
import time


# initialize pygame
pygame.init


# global variables
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GAME_SPEED = 500 #Lower is faster
COLUMNS = SCREEN_WIDTH // GRID_SIZE
ROWS = SCREEN_HEIGHT // GRID_SIZE

#COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
MAGENTA = (255, 0, 255)



#Define shapes
shapes = [
     [[1, 1, 1],
     [0, 1, 0]],  # T shape

    [[1, 1],
     [1, 1]],  # O shape

    [[1, 1, 1, 1]],  # I shape

    [[1, 1, 0],
     [0, 1, 1]],  # S shape

    [[0, 1, 1],
     [1, 1, 0]],  # Z shape

    [[1, 1, 1],
     [1, 0, 0]],  # L shape

    [[1, 1, 1],
     [0, 0, 1]]  # J shape
]

shape_colors = [
    RED,
    BLUE,
    YELLOW,
    GREEN,
    CYAN,
    ORANGE,
    MAGENTA
]


class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0
        
    @property
    def rotated_shape(self):
        return list(zip(*self.shape[::-1]))
    
    


def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(COLUMNS)] for _ in range(ROWS)]
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (col, row) in locked_positions:
                grid[row][col] = locked_positions[(col, row)]
    return grid

def convert_shape_format(piece):
    positions = []
    format_shape = piece.shape
    for i, row in enumerate(format_shape):
        for j, column in enumerate(row):
            if column == 1:
                positions.append((piece.x + j, piece.y + i))
    return positions

def valid_space(piece, grid):
    accepted_pos = [[(j, i) for j in range(COLUMNS) if grid[i][j] == BLACK] for i in range(ROWS)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(piece)
    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] >= 0:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    return Piece(5, 0, random.choice(shapes))



def draw_text_center(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, True, color)

    surface.blit(label, (SCREEN_WIDTH / 2 - label.get_width() / 2,
                         SCREEN_HEIGHT / 2 - label.get_height() / 2))
    
    
    
    
    
def draw_grid(surface, grid):
    for i in range(ROWS):
        for j in range(COLUMNS):
            pygame.draw.rect(surface, grid[i][j],
                             (j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
            
        
    # Draw grid lines
    for i in range(ROWS):
        pygame.draw.line(surface, WHITE, (0, i * GRID_SIZE), (SCREEN_WIDTH, i * GRID_SIZE))
    for j in range(COLUMNS):
        pygame.draw.line(surface, WHITE, (j * GRID_SIZE, 0), (j * GRID_SIZE, SCREEN_HEIGHT))
        
        

def draw_window(surface, grid):
    surface.fill(BLACK)
    draw_grid(surface, grid)
    pygame.display.update()
    
    
def clear_rows(grid, locked):
    increment = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if BLACK not in row:
            increment += 1
            # Add positions to remove from locked
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if increment > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + increment)
                locked[newKey] = locked.pop(key)
    return increment

def main():
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0

    while run:
        grid = create_grid(locked_positions)
        fall_speed = GAME_SPEED

        fall_time += clock.get_rawtime()
        clock.tick()

        # Piece falling logic
        if fall_time / 1000 >= fall_speed / 1000:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.shape = current_piece.rotated_shape
                    if not valid_space(current_piece, grid):
                        current_piece.shape = current_piece.rotated_shape[::-1]

        piece_pos = convert_shape_format(current_piece)

        # Add piece to the grid
        for i in range(len(piece_pos)):
            x, y = piece_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # If piece hit the ground
        if change_piece:
            for pos in piece_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            # Clear rows
            clear_rows(grid, locked_positions)

        draw_window(screen, grid)

        # Check if game lost
        if check_lost(locked_positions):
            draw_text_middle(screen, "GAME OVER", 80, WHITE)
            pygame.display.update()
            pygame.time.delay(2000)
            run = False


# Start game
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris')
main()
pygame.quit()
    
    
                
                
                
    
        
    
    
    
    
    
    
    
    
    
            
    
            
            
    
        
    
    

        