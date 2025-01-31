import pygame
from game import Game

# Initialisation de Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Slicing Game")

def main():
    game = Game()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.handle_event()
        game.update()
        
        screen.fill((0, 0, 0))  # Fond noir
        game.draw(screen)  # Dessine tous les objets du jeu (fruits, bombes, score, etc.)
        pygame.display.flip()
        
    pygame.quit()

if __name__ == "__main__":
    main()
 