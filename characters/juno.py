import pygame
import os

class Juno(object):
    # Player class
    def __init__(self , x: int , y: int , speed=1):
        CURRENT_DIR = os.path.dirname(__file__)
        ASSETS_DIR = os.path.join(CURRENT_DIR , ".." , "assets")
        IMG_DIR = os.path.join(ASSETS_DIR , "kiriko-juno1.png")

        self.img = pygame.image.load(IMG_DIR).convert_alpha()
        self.img = pygame.transform.scale(self.img , (115,115))
        self.rect = pygame.Rect(x,y , self.img.get_width() , self.img.get_height())
        self.speed = speed

    def move(self , keys , barrier , npcs) -> None:
        dx , dy = 0 , 0

        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1
        if keys[pygame.K_q]:
            pygame.quit()

        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        bar_x = self.rect.x + dx * self.speed
        bar_y = self.rect.y + dy * self.speed

        tmp_rect = pygame.Rect(bar_x , bar_y , self.rect.width , self.rect.height)
        for npc in npcs:
            if tmp_rect.colliderect(npc.rect):
                return

        if barrier.contains(tmp_rect):
            self.rect.x = bar_x
            self.rect.y = bar_y

    def draw(self, surface):
        surface.blit(self.img , (self.rect.x , self.rect.y))
