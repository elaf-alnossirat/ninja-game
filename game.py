import pygame
import time
import os
import random
from config import WIDTH, HEIGHT, FRUIT_SPEED

# Dictionnaire des fruits et leurs lettres associées
FRUIT_LETTERS = {
    "apple.png": "L",
    "orange.png": "O",
    "pineapple.png": "P",
    "watermelon.png": "W"
}

# Classe pour gérer les fruits
class Fruit:
    def __init__(self, image, x, y, speed):
        """Initialise un fruit entier ou coupé."""
        # Charger l'image du fruit entier
        self.image_path = os.path.join("assets", "fruits", "fruit_entier", image)
        self.half_image_path = os.path.join("assets", "fruits", "fruit_coupe", f"half{image}")

        try:
            self.image = pygame.image.load(self.image_path)
        except FileNotFoundError:
            print(f"⚠️ Erreur : L'image '{self.image_path}' est introuvable !")
            self.image = pygame.Surface((50, 50))  # Remplace par un carré si erreur

        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.is_cut = False  # Indique si le fruit est coupé
        self.letter = FRUIT_LETTERS.get(image, "")  # Lettre associée au fruit

    def cut(self):
        """Transforme le fruit en deux moitiés."""
        self.is_cut = True
        self.speed = -3  # Fait remonter légèrement les moitiés avant de tomber

        try:
            self.image = pygame.image.load(self.half_image_path)
        except FileNotFoundError:
            print(f"⚠️ Erreur : L'image coupée '{self.half_image_path}' est introuvable !")
            self.image = pygame.Surface((50, 50))  # Remplace par un carré si erreur

        self.image = pygame.transform.scale(self.image, (50, 50))

    def move(self):
        """Déplace le fruit entier ou coupé."""
        self.rect.y += self.speed
        if self.is_cut:
            self.speed += 0.5  # Augmente la gravité après la coupe

    def draw(self, screen):
        """Affiche le fruit ou ses moitiés à l'écran."""
        screen.blit(self.image, self.rect)
        
        # Afficher la lettre au-dessus du fruit
        font = pygame.font.SysFont("Arial", 24)
        letter_text = font.render(self.letter, True, (255, 255, 255))
        screen.blit(letter_text, (self.rect.x + 15, self.rect.y - 20))

# Classe principale du jeu
class Game:
    def __init__(self):
        """Initialise les paramètres du jeu avec un background et les strikes."""
        self.score = 0
        self.strikes = 0  # Nombre de fruits ratés
        self.fruits = []
        self.time_left = 30
        self.start_time = time.time()
        self.running = True

        background_path = os.path.join("assets", "background", "background.png")
        if os.path.exists(background_path):
            self.background = pygame.image.load(background_path)
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        else:
            print(f"⚠️ Erreur : L'image du background '{background_path}' est introuvable !")
            self.background = pygame.Surface((WIDTH, HEIGHT))
            self.background.fill((0, 0, 0))  # Fond noir par défaut

        self.fruit_images = [
            "apple.png",
            "orange.png",
            "pineapple.png",
            "watermelon.png"
        ]

    def spawn_fruit(self):
        """Génère un fruit aléatoire."""
        if random.randint(1, 100) > 80:
            image = random.choice(self.fruit_images)
            x = random.randint(50, WIDTH - 50)
            fruit = Fruit(image, x, 0, FRUIT_SPEED)
            self.fruits.append(fruit)

    def check_keypress(self, key):
        """Vérifie si une touche a été pressée pour couper un fruit."""
        for fruit in self.fruits[:]:
            if fruit.letter == key and not fruit.is_cut:
                fruit.cut()
                self.score += 1  # ✅ Augmente le score lorsqu'un fruit est tranché

    def handle_event(self):
        """Gère les événements du jeu (clavier et fermeture)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key).upper()  # Convertir en majuscule
                self.check_keypress(key)

    def update(self):
        """Met à jour le jeu (mouvement des fruits, strikes, timer)."""
        self.spawn_fruit()

        for fruit in self.fruits[:]:
            fruit.move()
            if fruit.rect.y > HEIGHT:  # ✅ Si un fruit tombe sans être coupé
                self.fruits.remove(fruit)
                if not fruit.is_cut:
                    self.strikes += 1  # ✅ Ajoute un strike
                    print(f"⚠️ Fruit raté ! Strikes: {self.strikes}/3")  # ✅ Debugging
                    if self.strikes >= 3:
                        self.end_game()

        elapsed_time = time.time() - self.start_time
        self.time_left = max(30 - int(elapsed_time), 0)

        if self.time_left <= 0:
            self.end_game()

    def draw(self, screen):
        """Affiche les éléments du jeu avec le background, score et strikes."""
        screen.blit(self.background, (0, 0))

        for fruit in self.fruits:
            fruit.draw(screen)

        font = pygame.font.SysFont("Arial", 24)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        timer_text = font.render(f"Temps restant: {self.time_left}s", True, (255, 255, 255))
        screen.blit(timer_text, (WIDTH - 200, 10))

        # ✅ Afficher les strikes en haut de l'écran
        strikes_text = font.render(f"Strikes: {self.strikes}/3", True, (255, 0, 0))
        screen.blit(strikes_text, (WIDTH // 2 - 50, 10))

    def end_game(self):
        """Termine la partie avec un écran 'Game Over' pendant 3 secondes."""
        print(f"Game Over! Score final: {self.score}")

        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        font = pygame.font.SysFont("Arial", 50)
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.fill((0, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2 + 10))
        pygame.display.flip()

        time.sleep(3)  # ✅ Pause avant fermeture
        self.running = False
