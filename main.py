import pygame
from game import Game
from menu import menu  # Import the menu function
from config import WIDTH, HEIGHT, FPS

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Slicing Game")

def main():
    """Main function to display the menu and start the game."""
    choice = menu()  # Show the menu before starting the game

    if choice == "start":  # If the player chooses "Start Game"
        game = Game()
        clock = pygame.time.Clock()

        while game.running:
            game.handle_event()
            game.update()

            screen.fill((0, 0, 0))  # Black background
            game.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()  # Run the main function
