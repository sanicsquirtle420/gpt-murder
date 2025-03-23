import pygame
import os
from utilities.support import *
import math
class Juno(object):
    # Player class

    def __init__(self , x: int , y: int , speed=1):
        CURRENT_DIR = os.path.dirname(__file__)
        ASSETS_DIR = os.path.join(CURRENT_DIR , ".." , "assets")
        IMG_DIR = os.path.join(ASSETS_DIR , "kiriko-juno1.png")

        self.import_assets()

        self.status = 'down_idle'
        self.frame_index = 0

        self.img = self.animations[self.status][self.frame_index]
        self.rect = pygame.Rect(x,y , self.img.get_width() , self.img.get_height())
        self.speed = speed
        

    def import_assets(self):
        self.animations = {
            'up': [],'down': [],'left': [],'right': [],
			'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
			'right_hoe':[],'left_hoe':[],'up_hoe':[],'down_hoe':[],
			'right_axe':[],'left_axe':[],'up_axe':[],'down_axe':[],
			'right_water':[],'left_water':[],'up_water':[],'down_water':[]
        }

        for animation in self.animations.keys():
            full_path = f"assets/animations/main_character/{animation}"
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 4 * dt
        
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        
        self.img = self.animations[self.status][int(self.frame_index)]
    

    def move(self , keys , barrier , npcs) -> None:
        dx , dy = 0 , 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= 1
            self.status = 'left'
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += 1
            self.status = 'right'
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= 1
            self.status = 'up'
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += 1
            self.status = 'down'
        if keys[pygame.K_q]:
            pygame.quit()

        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        if dx == 0 and dy == 0:
            self.status = self.status.split('_')[0] + '_idle'

        bar_x = self.rect.x + dx * self.speed
        bar_y = self.rect.y + dy * self.speed

        tmp_rect = pygame.Rect(bar_x , bar_y , self.rect.width , self.rect.height)
        for npc in npcs:
            if tmp_rect.colliderect(npc.rect):
                return

        if barrier.contains(tmp_rect):
            self.rect.x = bar_x
            self.rect.y = bar_y

    def near_character(self, npc) -> bool:
        dist = math.sqrt((npc.rect.x - self.rect.x) ** 2 + (npc.rect.y - self.rect.y) ** 2)
        return dist < npc.rect.x + 5 or dist < npc.rect.y + 5

    def distance_to(self, npc):
        return math.sqrt((npc.rect.x - self.rect.x) ** 2 + (npc.rect.y - self.rect.y) ** 2)

    def draw(self, surface):
        surface.blit(self.img , (self.rect.x , self.rect.y))
