import random
import pygame
import os

class NPC(object):
    def __init__(self, x: int, y: int , window):
        CURRENT_DIR = os.path.dirname(__file__)
        ASSETS_DIR = os.path.join(CURRENT_DIR, "..", "assets")
        IMG_DIR = os.path.join(ASSETS_DIR, "shakes.jpg")

        self.img = pygame.image.load(IMG_DIR).convert_alpha()
        self.img = pygame.transform.scale(self.img, (115, 115))
        self.window = window
        self.rect = pygame.Rect(x, y, self.img.get_width(), self.img.get_height())
        self.target_x , self.target_y = self.get_new_spot()
        self.speed = 5
        self.direction = 1
        # time tracking
        self.last_time = pygame.time.get_ticks()
        self.next_change = self.last_time + 30000

    def move(self, barrier , player , npcs):
        current_time = pygame.time.get_ticks()
        if current_time >= self.next_change:
            self.target_x , self.target_y = self.get_new_spot()
            self.last_time = current_time
            # updates after 1 minute and 5 - 20 seconds
            self.next_change = current_time + random.randint(5000 , 20000)

        if self.rect.x < self.target_x:
            dx = min(self.speed, self.target_x - self.rect.x)
        elif self.rect.x > self.target_x:
            dx = -min(self.speed, self.target_x - self.rect.x)
        else:
            dx = 0
        if self.rect.y < self.target_y:
            dy = min(self.speed, self.target_y - self.rect.y)
        elif self.rect.y > self.target_y:
            dy = -min(self.speed, self.target_y - self.rect.y)
        else:
            dy = 0

        new_x = self.rect.x + dx
        new_y = self.rect.y + dy
        tmp_rect = pygame.Rect(new_x , new_y , self.rect.width , self.rect.height)

        if tmp_rect.colliderect(player.rect):
            return
        for npc in npcs:
            if npc is not self and tmp_rect.colliderect(npc.rect):
                return
        if barrier.contains(tmp_rect):
            self.rect.x = new_x
            self.rect.y = new_y

    def get_new_spot(self):
        max_x = self.window.get_width() - self.rect.width
        max_y = self.window.get_height() - self.rect.height
        return random.randint(10 , max_x) , random.randint(10 , max_y)

    def draw(self, surface , x , y):
        surface.blit(self.img, (self.rect.x - x, self.rect.y - y))
