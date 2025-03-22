import pygame
import os

class NPC(object):
    def __init__(self, x: int, y: int):
        CURRENT_DIR = os.path.dirname(__file__)
        ASSETS_DIR = os.path.join(CURRENT_DIR, "..", "assets")
        IMG_DIR = os.path.join(ASSETS_DIR, "shakes.jpg")

        self.img = pygame.image.load(IMG_DIR).convert_alpha()
        self.img = pygame.transform.scale(self.img, (115, 115))
        self.rect = pygame.Rect(x, y, self.img.get_width(), self.img.get_height())
        self.speed = 5
        self.direction = 1

    def move(self):
        if self.rect.y >= 500:
            self.direction = -1
        elif self.rect.y <= 100:
            self.direction = 1

        self.rect.y += self.speed * self.direction

    def draw(self, surface):
        surface.blit(self.img, (self.rect.x, self.rect.y))
