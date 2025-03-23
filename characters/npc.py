import random
import pygame
import os
from utilities.support import *

class NPC(object):
    def __init__(self, character, window):

        self.import_assets()
        

        x = character["init_pos"][0]
        y = character["init_pos"][1]

        self.initX = x
        self.initY = y

        self.name = character["name"]
        self.spriteDir = character["spriteDir"]
        self.movable_area = character["movable_area"]
        self.status = "down_idle"
        self.frame_index = 0

        self.scale = 5  # You can adjust this value to change the size
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

       
        # if self.rect.x != self.target_x or self.rect.y != self.target_y:
        #     self.smooth_move()
        #     return

       
        # if current_time - self.last_move_time < self.wait_time:
        #     return

        
        # directions = ["up", "down", "left", "right"]
        # direction = random.choice(directions)
        # move_distance = random.randint(50, 100)  

        # min_x = self.initX
        # max_x = self.initX + self.movable_area[0]
        # min_y = self.initY
        # max_y = self.initY + self.movable_area[1]

        # if direction == "up":
        #     self.target_y = max(self.rect.y - move_distance, min_y)
        #     self.status = "up"
        # elif direction == "down":
        #     self.target_y = min(self.rect.y + move_distance, max_y)
        #     self.status = "down"
        # elif direction == "left":
        #     self.target_x = max(self.rect.x - move_distance, min_x)
        #     self.status = "left"
        # elif direction == "right":
        #     self.target_x = min(self.rect.x + move_distance, max_x)
        #     self.status = "right"

        # self.last_move_time = current_time
        # self.wait_time = random.randint(5000, 8000)  

    # def smooth_move(self):
    #     """Moves the NPC smoothly towards the target position."""
    #     if self.rect.x < self.target_x:
    #         self.rect.x += min(self.speed, self.target_x - self.rect.x)
    #     elif self.rect.x > self.target_x:
    #         self.rect.x -= min(self.speed, self.rect.x - self.target_x)

    #     if self.rect.y < self.target_y:
    #         self.rect.y += min(self.speed, self.target_y - self.rect.y)
    #     elif self.rect.y > self.target_y:
    #         self.rect.y -= min(self.speed, self.rect.y - self.target_y)

        
    #     if self.rect.x == self.target_x and self.rect.y == self.target_y:
    #         self.status = self.status.split('_')[0] + '_idle'

    def draw(self, surface, x, y):
        surface.blit(self.img, (self.rect.x - x, self.rect.y - y))
