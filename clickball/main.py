#!/usr/bin/env python3
import asyncio
import pygame
import random

# Pygame initialisieren
pygame.init()

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Bildschirmgröße
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Platformer")

# Framerate
clock = pygame.time.Clock()
FPS = 60

# Spielerklasse
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - 150
        self.velocity = 5
        self.jump_height = -15
        self.gravity = 0.5
        self.velocity_y = 0
        self.on_ground = False

    def update(self):
        keys = pygame.key.get_pressed()

        # Bewegung nach links und rechts
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocity
        
        # Schwerkraft anwenden
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        
        # Überprüfe, ob der Spieler auf einer Plattform steht
        self.on_ground = False  # Zurücksetzen der Variable
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.velocity_y >= 0:
                # Wenn der Spieler auf der Plattform landet, setze ihn darauf
                self.rect.y = platform.rect.top - self.rect.height
                self.velocity_y = 0  # Stoppe die vertikale Bewegung
                self.on_ground = True
                break  # Verhindert mehrfaches Aufeinandertreffen mit verschiedenen Plattformen

        # Wenn der Spieler den Boden erreicht hat, stoppe die Schwebekraft
        if self.rect.y >= SCREEN_HEIGHT - 150:
            self.rect.y = SCREEN_HEIGHT - 150
            self.velocity_y = 0
            self.on_ground = True

        # Wenn der Spieler am unteren Rand des Bildschirms ankommt, setze ihn darauf
        if self.rect.y < 0:
            self.rect.y = 0
            self.velocity_y = 0

        # Springen
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_height
            self.on_ground = False


# Plattformen
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Gegner
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = 2

    def update(self):
        self.rect.x += self.velocity
        if self.rect.x >= SCREEN_WIDTH - 50 or self.rect.x <= 0:
            self.velocity = -self.velocity


# Spielobjekte
player = Player()
platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Plattformen hinzufügen
platforms.add(Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))  # Bodenplattform
platforms.add(Platform(200, SCREEN_HEIGHT - 150, 200, 20))  # Eine zusätzliche Plattform
platforms.add(Platform(500, SCREEN_HEIGHT - 250, 200, 20))  # Eine weitere Plattform

# Gegner hinzufügen
enemies.add(Enemy(400, SCREEN_HEIGHT - 250))

# Alle Sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(platforms)
all_sprites.add(enemies)

async def main(): 
    # Hauptspiel-Schleife
    running = True
    while running:
        clock.tick(FPS)

        # Ereignisse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Spieler und Gegner aktualisieren
        all_sprites.update()

        # Kollisionen mit Gegnern
        if pygame.sprite.spritecollide(player, enemies, False):
            print("Du wurdest getroffen! Spiel endet.")
            running = False

        # Bildschirm füllen
        screen.fill(WHITE)

        # Alle Sprites zeichnen
        all_sprites.draw(screen)

        # Bildschirm aktualisieren
        pygame.display.flip()

# Pygame beenden
    pygame.quit()
    await asyncio.sleep(0)

asyncio.run(main())
