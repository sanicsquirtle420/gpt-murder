import pygame

pygame.init()
window = pygame.display.set_mode((1000 , 800) , pygame.RESIZABLE)
clock = pygame.time.Clock()
pygame.display.set_caption("Deep Murder (Juno / beta version)")

def draw_window(sample_char, barrier):
    window.fill((147, 204, 207))
    sample_char.draw(window)
    pygame.draw.rect(window, (189 , 52 , 235), barrier, 10)
    pygame.display.update()

def main():
    j: Juno = Juno(50,50 , speed=10)
    border = pygame.Rect(0, 0, window.get_width(), window.get_height())
    status: bool = True
    while status:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = False
            elif event.type == pygame.VIDEORESIZE:
                border = pygame.Rect(0, 0, window.get_width(), window.get_height())
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

        if dx is not 0 and dy is not 0:
            dx *= 0.7071
            dy *= 0.7071

        bar_x = self.rect.x + dx * self.speed
        bar_y = self.rect.y + dy * self.speed

        tmp_rect = pygame.Rect(bar_x , bar_y , self.rect.width , self.rect.height)
        if barrier.contains(tmp_rect):
            self.rect.x = bar_x
            self.rect.y = bar_y

    def draw(self, surface):
        surface.blit(self.img , (self.rect.x , self.rect.y))

if __name__ == "__main__":
    main()
