import pygame
from config import WIDTH, HEIGHT

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (70, 70, 70)
RED = (200, 50, 50)
DARK_RED = (150, 30, 30)

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Ninja - Menu")

# Load background image
background_path = "assets/background/background.png"
try:
    background = pygame.image.load(background_path)
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except FileNotFoundError:
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill(BLACK)

# Load sounds
pygame.mixer.init()
button_click_sound = pygame.mixer.Sound("assets/sound/click-124467.mp3")
menu_music = "assets/sound/loop-menu-preview-109594.mp3"

# Play background music
pygame.mixer.music.load(menu_music)
pygame.mixer.music.play(-1)  # Loop indefinitely

# Font
font = pygame.font.SysFont("Arial", 36)

# Button properties
button_width, button_height = 250, 70
start_button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - 80, button_width, button_height)
exit_button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 20, button_width, button_height)

def draw_button(rect, text, base_color, hover_color, mouse_pos):
    """Draws a button with a hover effect and text."""
    color = hover_color if rect.collidepoint(mouse_pos) else base_color
    pygame.draw.rect(screen, color, rect, border_radius=15)
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def menu():
    """Displays the main menu and handles button clicks."""
    running = True
    while running:
        screen.blit(background, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        # Draw buttons with hover effects
        draw_button(start_button_rect, "Start Game", GRAY, DARK_GRAY, mouse_pos)
        draw_button(exit_button_rect, "Exit", RED, DARK_RED, mouse_pos)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button_rect.collidepoint(mouse_pos):
                    button_click_sound.play()
                    pygame.time.delay(200)  # Small delay for effect
                    return "start"
                elif exit_button_rect.collidepoint(mouse_pos):
                    button_click_sound.play()
                    pygame.time.delay(200)
                    pygame.quit()
                    exit()

if __name__ == "__main__":
    menu()
