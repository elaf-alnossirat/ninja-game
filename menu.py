import pygame
from config import WIDTH, HEIGHT

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (200, 50, 50)

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Ninja - Menu")

# Load background image (if available)
background_path = "assets/background/background.png"
try:
    background = pygame.image.load(background_path)
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except FileNotFoundError:
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill(BLACK)  # Default to black if the image is missing

# Font
font = pygame.font.SysFont("Arial", 36)

# Button properties
button_width, button_height = 200, 60
start_button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - 50, button_width, button_height)
exit_button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 50, button_width, button_height)

def draw_button(rect, text, color):
    """Draws a button with text on the screen."""
    pygame.draw.rect(screen, color, rect, border_radius=10)
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def menu():
    """Displays the main menu and handles button clicks."""
    running = True
    while running:
        screen.blit(background, (0, 0))

        # Draw buttons
        draw_button(start_button_rect, "Start Game", GRAY)
        draw_button(exit_button_rect, "Exit", RED)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):
                    return "start"  # Start the game
                elif exit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()  # Exit the game

if __name__ == "__main__":
    menu()
