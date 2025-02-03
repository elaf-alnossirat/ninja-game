import pygame
from game import Game
from config import WIDTH, HEIGHT, FPS

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Slicing Game")

def main():
    game = Game()
    clock = pygame.time.Clock()

    while game.running:
        game.handle_event()
        game.update()

        screen.fill((0, 0, 0))  # Fond noir
        game.draw(screen)  # Dessine tous les objets du jeu (fruits, bombes, score, etc.)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()