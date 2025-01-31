import pygame
import random
import time

# Classe pour gérer les fruits
class Fruit:
    def __init__(self, image, x, y, speed):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def move(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
# Classe pour gérer les bombes
class Bombe:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("assets/bombs/bombe.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Classe du jeu qui gère le score, les frappes, et la logique
class Game:
    def __init__(self):
        self.score = 0
        self.strikes = 0
        self.fruits = []
        self.bombes = []
        self.time_left = 30  # Temps de jeu initial

    def check_collision(self, fruit, x, y):
        if fruit.rect.collidepoint(x, y):  # Vérifie si un fruit est tranché
            self.score += 1
            self.fruits.remove(fruit)

    def handle_event(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:  # Exemple d'action lorsque l'on appuie sur la barre d'espace
            pass

    def update(self):
        for fruit in self.fruits:
            fruit.move()
            if fruit.rect.y > 600:  # Si le fruit dépasse l'écran
                self.strikes += 1
                if self.strikes >= 3:
                    self.end_game()

    def draw(self, screen):
        # Dessiner les fruits
        for fruit in self.fruits:
            fruit.draw(screen)

        # Dessiner les bombes
        for bombe in self.bombes:
            bombe.draw(screen)

        # Afficher le score
        font = pygame.font.SysFont("Arial", 24)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))  # Afficher le score en haut à gauche

    def end_game(self):
        # Fin du jeu
        print(f"Game Over! Score: {self.score}")
        pygame.quit()
        exit()
