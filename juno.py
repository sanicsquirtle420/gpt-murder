import pygame
from pygame.rect import RectType

pygame.init()
screen = pygame.display.set_mode((1000 , 800) , pygame.RESIZABLE)
clock = pygame.time.Clock()
pygame.display.set_caption("Juno :D")

def draw_window(sample_char , barrier):
    screen.fill((147,204,207))
    sample_char.draw(screen)
    pygame.draw.rect(screen , (189 , 52 , 235) , barrier , 10)
    pygame.display.update()

def main():
    j: Juno = Juno(100,100 , speed=15)
    border = pygame.Rect(0, 0, screen.get_width(), screen.get_height())
    status: bool = True
    while status:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                status = False
        keys = pygame.key.get_pressed()
        j.move(keys , border)
        draw_window(j , border)

    pygame.quit()

class Juno(object):
    # Player class
    def __init__(self , x: int , y: int , speed=1):
        self.img = pygame.image.load("assets/kiriko-juno1.png").convert_alpha()
        self.img = pygame.transform.scale(self.img , (115,115))
        self.rect = pygame.Rect(x,y , self.img.get_width() , self.img.get_height())
        self.speed = speed

    def move(self , keys , barrier) -> None:
        bar_x , bar_y = self.rect.x , self.rect.y

        if keys[pygame.K_a]:
            bar_x -= self.speed
        if keys[pygame.K_d]:
            bar_x += self.speed
        if keys[pygame.K_w]:
            bar_y -= self.speed
        if keys[pygame.K_s]:
            bar_y += self.speed
        if keys[pygame.K_q]:
            pygame.quit()

        tmp_rect = pygame.Rect(bar_x , bar_y , self.rect.width , self.rect.height)
        if barrier.contains(tmp_rect):
            self.rect.x = bar_x
            self.rect.y = bar_y

    def draw(self, surface):
        surface.blit(self.img , (self.rect.x , self.rect.y))

if __name__ == "__main__":
    main()
