import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("AI-Modified Block Game")

# Colors
BLACK = (0, 0, 0)
HIGHLIGHT_COLOR = (128, 255, 128)  # Highlight color for user interaction
BLOCK_COLOR = (0, 255, 0)  # Color for blocks
COLLECTED_BLOCK_COLOR = (255, 255, 0)  # Color for collected blocks (yellow)
MISSED_BLOCK_COLOR = (255, 0, 0)  # Color for missed blocks (red)

# Game Variables
block_width = 50
block_height = 50
player_width = 100
player_height = 10
player_speed = 10

score = 0
level = 1
game_over = False

# Player paddle
player_x = (SCREEN_WIDTH // 2) - (player_width // 2)
player_y = SCREEN_HEIGHT - 30
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

# Blocks
blocks = []
block_interval = 2000  # time between blocks in milliseconds
last_block_time = pygame.time.get_ticks()

# Font
font = pygame.font.SysFont(None, 36)

# Function to draw text on screen
def draw_text(text, x, y, color):
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, (x, y))

# Function to check AI difficulty adjustment based on score multiples
def check_ai_difficulty():
    global level
    
    if score >= 100 and level <= (score // 100) * 2:
        level += 2  
        print("Jumping to higher level due to score of 100!")
    elif score >= 50 and level <= (score // 50):
        level += 1  
        print("Moving to the next level due to score of 50!")

# Function to reset game state
def reset_game():
    global score, level, blocks, game_over
    score = 0
    level = 1
    blocks.clear()
    game_over = False

# Animation functions for block collection and misses
def animate_block_collection(block):
    # Change the block's color temporarily to simulate glowing effect.
    original_color = BLOCK_COLOR
    
    # Draw the glowing effect for a short duration.
    glow_duration_ms = int(200)   # Total glowing duration in milliseconds.
    frames = glow_duration_ms // 20   # Number of frames for the animation.
    
    for _ in range(frames):
        pygame.draw.rect(screen, COLLECTED_BLOCK_COLOR, block)
        pygame.display.flip()
        pygame.time.delay(10)   # Delay between frames
        
        pygame.draw.rect(screen, original_color, block)
        pygame.display.flip()
        pygame.time.delay(10)   # Delay between frames

def animate_block_missing():
    print('Block missed! Animation would play here.')

def animate_game_over():
    print('Game Over! Animation would play here.')

# Game Loop
running = True

while running:
    screen.fill(BLACK)  # Change background color to black

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Restart game on key press if game is over
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:  
                reset_game()

    # Move the player with arrow keys only if not game over
    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
            player_rect.x += player_speed

        # Create new blocks
        current_time = pygame.time.get_ticks()
        if current_time - last_block_time > block_interval:
            block_x = random.randint(0, SCREEN_WIDTH - block_width)
            blocks.append(pygame.Rect(block_x, 0, block_width, block_height))
            last_block_time = current_time

        # Move blocks and check for collisions or misses
        for block in blocks[:]:
            block.y += level + 2   # Increase speed based on level
            
            if block.y > SCREEN_HEIGHT:
                animate_block_missing()   # Call animation function when a block is missed
                blocks.remove(block)
                game_over = True   # Set game over when a block is missed
                
            elif block.colliderect(player_rect):
                animate_block_collection(block)   # Call animation function when a block is collected
                blocks.remove(block)
                score += 20   # More points for catching block

    # Draw player and blocks only if not game over with highlight colors 
    pygame.draw.rect(screen, HIGHLIGHT_COLOR, player_rect)  
    
    for block in blocks:
        pygame.draw.rect(screen, BLOCK_COLOR if not game_over else MISSED_BLOCK_COLOR, block)

    # Draw score and level or game over message 
    if not game_over:
        draw_text(f"Score: {score}", 10, 10, HIGHLIGHT_COLOR)
        draw_text(f"Level: {level}", 10, 50, HIGHLIGHT_COLOR)
        
        # AI-based level progression check 
        check_ai_difficulty()
        
    else:
        draw_text("Game Over! Press 'R' to Restart", SCREEN_WIDTH // 4 + 50, SCREEN_HEIGHT // 2 - 20, HIGHLIGHT_COLOR)

    # Update display 
    pygame.display.flip()

    # Frame rate control 
    pygame.time.Clock().tick(60)
