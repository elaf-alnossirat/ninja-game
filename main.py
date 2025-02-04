import pygame
from game import Game
from menu import menu  # Import the menu function
from config import WIDTH, HEIGHT, FPS

def main():
    """Main function to display the menu and start the game."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fruit Slicing Game")

    while True:  # Loop to keep the game running until the player exits
        choice = menu()  # Show the menu before starting the game

        if choice == "start":  # If the player chooses "Start Game"
            game = Game()  # Create a new instance of the game
            clock = pygame.time.Clock()

            while game.running:
                game.handle_event()
                game.update()

                screen.fill((0, 0, 0))  # Black background
                game.draw(screen)
                pygame.display.flip()
                clock.tick(FPS)

            # After the game ends, show the score and return to the menu
            print(f"Final Score: {game.score}")  # Optional: Print the score to the console

        elif choice == "exit":  # If the player chooses "Exit"
            pygame.quit()
            return  # Exit the game completely

if __name__ == "__main__":
    main()  # Run the main function