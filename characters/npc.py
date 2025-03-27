import random
import pygame
import os
from utilities.support import *

class NPC(object):
    def __init__(self, character, window):
        x = character["init_pos"][0]
        y = character["init_pos"][1]

        self.initX = x
        self.initY = y

        self.name = character["name"]
        self.spriteDir = character["spriteDir"]
        
        self.import_assets()
        self.spriteDir = character["spriteDir"]
        self.movable_area = character["movable_area"]
        self.status = "down_idle"
        self.frame_index = 0

        self.scale = 5  # Adjustable to change size
        self.animations = {status: [pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale)) 
                                  for img in frames] 
                          for status, frames in self.animations.items()}
        self.img = self.animations[self.status][self.frame_index]
        self.scaled_img  = pygame.transform.scale(self.img, (200, 200))
        self.window = window
        self.rect = pygame.Rect(x, y, self.scaled_img.get_width(), self.scaled_img .get_height())

        

        self.last_move_time = pygame.time.get_ticks()
        self.wait_time = random.randint(5000, 8000)

        self.speed = 2 
        self.target_x = x
        self.target_y = y

    def import_assets(self):
        self.animations = {
        'up': [], 'down': [], 'left': [], 'right': [], 'down_idle': [], 
        'right_idle': [], 'up_idle': [], 'left_idle': []
        }
        
        for animation in self.animations.keys():
            full_path = f"assets/animations/{self.spriteDir}/{animation}"
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.img = self.animations[self.status][int(self.frame_index)]

    def move(self):
        """Handles smooth movement within the defined movable area."""
        current_time = pygame.time.get_ticks()
    
        # If the NPC is moving it continues
        if self.rect.x != self.target_x or self.rect.y != self.target_y:
            self.smooth_move()
            return
    
        # NPC stops once it reaches the target
        if current_time - self.last_move_time < self.wait_time:
            return
    
        # Directions of movement
        directions = ["up", "down", "left", "right"]
        random.shuffle(directions)  # direction randomizer
    
        move_distance = random.randint(50, 100)
    
        # Establishes a target for the npc to move to within the map
        for direction in directions:
            if direction == "up":
                new_target_y = max(self.initY, self.rect.y - move_distance)
                if new_target_y != self.rect.y:
                    self.target_y = new_target_y
                    self.status = "up"
                    break
            elif direction == "down":
                new_target_y = min(self.initY + self.movable_area[1], self.rect.y + move_distance)
                if new_target_y != self.rect.y:
                    self.target_y = new_target_y
                    self.status = "down"
                    break
            elif direction == "left":
                new_target_x = max(self.initX, self.rect.x - move_distance)
                if new_target_x != self.rect.x:
                    self.target_x = new_target_x
                    self.status = "left"
                    break
            elif direction == "right":
                new_target_x = min(self.initX + self.movable_area[0], self.rect.x + move_distance)
                if new_target_x != self.rect.x:
                    self.target_x = new_target_x
                    self.status = "right"
                    break

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
            self.status = self.status.split('_')[0] + '_idle'

    def draw(self, surface, x, y):
        surface.blit(self.img, (self.rect.x - x, self.rect.y - y))
