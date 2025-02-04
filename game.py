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

# Dictionnaire des fruits coupés correspondants
FRUIT_CUT_IMAGES = {
    "apple.png": "halfapple.png",
    "orange.png": "halforange.png",
    "pineapple.png": "halfpineappl.png",
    "watermelon.png": "halfwatermelon.png"  # ✅ Correction du nom
}

# Classe pour gérer les fruits et les glaçons
class Fruit:
    def __init__(self, image, x, y, speed, is_ice=False):
        """Initialise un fruit ou un glaçon."""
        self.is_ice = is_ice  
        self.image_name = image  # ✅ Sauvegarde du nom original du fruit
        self.image_path = os.path.join("assets", "fruits", "fruit_entier", image) if not is_ice else os.path.join("assets", "ice", image)
        self.half_image_path = os.path.join("assets", "fruits", "fruit_coupe", FRUIT_CUT_IMAGES.get(image, "")) if not is_ice else None

        try:
            self.image = pygame.image.load(self.image_path)
        except FileNotFoundError:
            print(f"⚠️ Erreur : L'image '{self.image_path}' est introuvable !")
            self.image = pygame.Surface((50, 50))
            self.image.fill((0, 255, 255) if is_ice else (255, 0, 0))  

        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.is_cut = False  
        self.letter = FRUIT_LETTERS.get(image, "") if not is_ice else "I"  

    def cut(self):
        """Transforme le fruit en deux moitiés."""
        self.is_cut = True
        if self.is_ice:
            return  

        # ✅ Charger l'image coupée si elle existe
        if self.half_image_path and os.path.exists(self.half_image_path):
            try:
                self.image = pygame.image.load(self.half_image_path)
                self.image = pygame.transform.scale(self.image, (50, 50))
            except FileNotFoundError:
                print(f"⚠️ Erreur : Impossible de charger '{self.half_image_path}'")
        else:
            print(f"⚠️ Aucune image coupée trouvée pour {self.image_name}")

        self.speed = -3  

    def move(self):
        """Déplace le fruit ou le glaçon."""
        self.rect.y += self.speed
        if self.is_cut and not self.is_ice:
            self.speed += 0.5  

    def draw(self, screen):
        """Affiche l'objet à l'écran."""
        screen.blit(self.image, self.rect)

        font = pygame.font.SysFont("Arial", 24)
        letter_text = font.render(self.letter, True, (255, 255, 255))
        screen.blit(letter_text, (self.rect.x + 15, self.rect.y - 20))

# Classe principale du jeu
class Game:
    def __init__(self):
        """Initialise les paramètres du jeu avec le système des glaçons."""
        self.score = 0
        self.strikes = 0  
        self.fruits = []
        self.time_left = 30
        self.start_time = time.time()
        self.running = True
        self.freeze_end_time = None  
        self.show_frozen_message = False  
        self.freeze_duration = 3  # Duration in seconds to freeze the game

        background_path = os.path.join("assets", "background", "background.png")
        if os.path.exists(background_path):
            self.background = pygame.image.load(background_path)
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        else:
            print(f"⚠️ Erreur : L'image du background '{background_path}' est introuvable !")
            self.background = pygame.Surface((WIDTH, HEIGHT))
            self.background.fill((0, 0, 0))  

        self.fruit_images = ["apple.png", "orange.png", "pineapple.png", "watermelon.png"]
        self.ice_image = "ice-.png"  

    def spawn_fruit(self):
        """Génère un fruit ou un glaçon aléatoirement avec une limite."""
        if len(self.fruits) < 3:  
            if random.randint(1, 100) > 95:  
                x = random.randint(50, WIDTH - 50)
                ice = Fruit(self.ice_image, x, 0, FRUIT_SPEED, is_ice=True)
                self.fruits.append(ice)

            elif random.randint(1, 100) > 80:
                image = random.choice(self.fruit_images)
                x = random.randint(50, WIDTH - 50)
                fruit = Fruit(image, x, 0, FRUIT_SPEED)
                self.fruits.append(fruit)

    def check_keypress(self, key):
        """Vérifie si une touche a été pressée pour couper un fruit ou activer le glaçon."""
        for fruit in self.fruits[:]:
            if fruit.letter == key and not fruit.is_cut:
                if fruit.is_ice:
                    self.freeze_end_time = time.time() + self.freeze_duration
                    self.show_frozen_message = True
                fruit.cut()
                self.score += 1  

    def handle_event(self):
        """Gère les événements du jeu (clavier et fermeture)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key).upper()  
                self.check_keypress(key)

    def update(self):
        """Met à jour le jeu (mouvement des fruits, strikes, timer)."""
        if self.freeze_end_time and time.time() < self.freeze_end_time:
            return  

        self.show_frozen_message = False  

        self.spawn_fruit()

        for fruit in self.fruits[:]:
            fruit.move()
            if fruit.rect.y > HEIGHT:  
                self.fruits.remove(fruit)
                if not fruit.is_cut and not fruit.is_ice:  
                    self.strikes += 1  
                    if self.strikes >= 3:
                        self.end_game()

        if not (self.freeze_end_time and time.time() < self.freeze_end_time):
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

        if self.show_frozen_message:
            frozen_text = font.render("Temps gelé !", True, (0, 255, 255))
            screen.blit(frozen_text, (WIDTH // 2 - 80, HEIGHT // 2 - 20))

    def end_game(self):
        """Affiche un écran Game Over et quitte."""
        print(f"Game Over! Score final: {self.score}")
        time.sleep(3)  
        self.running = False