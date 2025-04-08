import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Falling Blocks")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Player settings
player_size = 50
player_speed = 5

# Block settings
block_size = 20
block_speed = 5
block_spawn_time = 1000  # milliseconds

# Font
font = pygame.font.Font(None, 36)

# Clock
clock = pygame.time.Clock()
FPS = 60


def spawn_block(blocks):
    """Create a new falling block at a random x-coordinate."""
    x = random.randint(0, WIDTH - block_size)
    y = -block_size
    rect = pygame.Rect(x, y, block_size, block_size)
    blocks.append(rect)


def draw_text(text, pos, color=WHITE):
    """Render text on the screen at the given position."""
    text_surf = font.render(text, True, color)
    screen.blit(text_surf, pos)


def show_game_over(score):
    """Display game over message and wait for restart or quit."""
    screen.fill(BLACK)
    over_text = font.render(f"Game Over! Score: {score}", True, RED)
    prompt_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
    screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2,
                             HEIGHT // 2 - over_text.get_height()))
    screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2,
                              HEIGHT // 2 + 10))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    return False
        clock.tick(FPS)


def main():
    """Main game loop with restart capability."""
    while True:
        # Initialize game state
        player = pygame.Rect(WIDTH // 2 - player_size // 2,
                             HEIGHT - player_size - 10,
                             player_size, player_size)
        blocks = []
        score = 0
        last_spawn_time = pygame.time.get_ticks()
        running = True

        # Game loop
        while running:
            clock.tick(FPS)
            current_time = pygame.time.get_ticks()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Spawn blocks periodically
            if current_time - last_spawn_time > block_spawn_time:
                spawn_block(blocks)
                last_spawn_time = current_time

            # Player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.left > 0:
                player.x -= player_speed
            if keys[pygame.K_RIGHT] and player.right < WIDTH:
                player.x += player_speed

            # Move blocks and check collisions
            for block in blocks[:]:
                block.y += block_speed
                # Catch block
                if block.colliderect(player):
                    score += 1
                    blocks.remove(block)
                # Missed block
                elif block.y > HEIGHT:
                    running = False

            # Draw everything
            screen.fill(BLACK)
            pygame.draw.rect(screen, WHITE, player)
            for block in blocks:
                pygame.draw.rect(screen, RED, block)
            draw_text(f"Score: {score}", (10, 10))
            pygame.display.flip()

        # After game loop ends, show game over and check restart
        if not show_game_over(score):
            break  # exit outer loop to quit

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
