import random
import pygame
import os
from utilities.support import *

class NPC(object):
    def __init__(self, character, window):
        CURRENT_DIR = os.path.dirname(__file__)
        ASSETS_DIR = os.path.join(CURRENT_DIR, "..", "assets")
        IMG_DIR = os.path.join(ASSETS_DIR, "shakes.jpg")

        x = character["init_pos"][0]
        y = character["init_pos"][1]

        self.name = character["name"]
        self.movable_area = character["movable_area"]

        self.img = pygame.image.load(IMG_DIR).convert_alpha()
        self.img = pygame.transform.scale(self.img, (115, 115))
        self.window = window
        self.rect = pygame.Rect(x, y, self.img.get_width(), self.img.get_height())

        self.status = "down_idle"
        self.frame_index = 0

        self.last_move_time = pygame.time.get_ticks()
        self.wait_time = random.randint(5000, 8000)

        self.speed = 2 
        self.target_x = x
        self.target_y = y

    def import_assets(self):
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [], 'down_idle': []
        }
        for animation in self.animations.keys():
            full_path = f"assets/animations/finn/{animation}"
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.img = self.animations[self.status][int(self.frame_index)]

    def move(self):
        """Handles smooth movement towards a target position."""
        current_time = pygame.time.get_ticks()

       
        if self.rect.x != self.target_x or self.rect.y != self.target_y:
            self.smooth_move()
            return

       
        if current_time - self.last_move_time < self.wait_time:
            return

        
        directions = ["up", "down", "left", "right"]
        direction = random.choice(directions)
        move_distance = random.randint(50, 100)  

        min_x = self.rect.x
        max_x = self.rect.x + self.movable_area[0]
        min_y = self.rect.y
        max_y = self.rect.y + self.movable_area[1]

        if direction == "up":
            self.target_y = max(self.rect.y - move_distance, min_y)
            self.status = "up"
        elif direction == "down":
            self.target_y = min(self.rect.y + move_distance, max_y)
            self.status = "down"
        elif direction == "left":
            self.target_x = max(self.rect.x - move_distance, min_x)
            self.status = "left"
        elif direction == "right":
            self.target_x = min(self.rect.x + move_distance, max_x)
            self.status = "right"

        self.last_move_time = current_time
        self.wait_time = random.randint(5000, 8000)  

    def smooth_move(self):
        """Moves the NPC smoothly towards the target position."""
        if self.rect.x < self.target_x:
            self.rect.x += min(self.speed, self.target_x - self.rect.x)
        elif self.rect.x > self.target_x:
            self.rect.x -= min(self.speed, self.rect.x - self.target_x)

        if self.rect.y < self.target_y:
            self.rect.y += min(self.speed, self.target_y - self.rect.y)
        elif self.rect.y > self.target_y:
            self.rect.y -= min(self.speed, self.rect.y - self.target_y)

        
        if self.rect.x == self.target_x and self.rect.y == self.target_y:
            self.status = "down_idle"

    def draw(self, surface, x, y):
        surface.blit(self.img, (self.rect.x - x, self.rect.y - y))
