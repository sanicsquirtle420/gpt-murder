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
        self.next_change = self.last_time + 3000

    def move(self, barrier , player , npcs):
        current_time = pygame.time.get_ticks()
        if current_time >= self.next_change:
            self.target_x , self.target_y = self.get_new_spot()
            self.last_time = current_time
            # updates after 30  + random int from 5 to 20 seconds
            self.next_change = current_time + random.randint(5000 , 20000)

        dx , dy = 0 , 0

        if abs(self.rect.x - self.target_x) > self.speed:
            dx = self.speed if self.target_x > self.rect.x else -self.speed
        else:
            dx = self.target_x - self.rect.x
        if abs(self.rect.y - self.target_y) > self.speed:
            dy = self.speed if self.target_y > self.rect.y else -self.speed
        else:
            dy = self.target_y - self.rect.y

        new_x = self.rect.x + dx
        tmp_rect = pygame.Rect(new_x , self.rect.y , self.rect.width , self.rect.height)
        x_move = True
        if not barrier.contains(tmp_rect):
            x_move = False
        if tmp_rect.colliderect(player.rect):
            x_move = False
        for npc in npcs:
            if npc is not self and tmp_rect.colliderect(npc.rect):
                x_move = False
                break
        if x_move:
            self.rect.x = new_x

        new_y = self.rect.y + dy
        tmp_rect = pygame.Rect(self.rect.x, new_y, self.rect.width, self.rect.height)
        y_move = True
        if not barrier.contains(tmp_rect):
            y_move = False
        if tmp_rect.colliderect(player.rect):
            y_move = False
        for npc in npcs:
            if npc is not self and tmp_rect.colliderect(npc.rect):
                y_move = False
                break
        if y_move:
            self.rect.y = new_y

    def get_new_spot(self):
        max_x = self.window.get_width() - self.rect.width
        max_y = self.window.get_height() - self.rect.height
        return random.randint(0 , max_x) , random.randint(0 , max_y)

    def draw(self, surface , x , y):
        surface.blit(self.img, (self.rect.x - x, self.rect.y - y))
