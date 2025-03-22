import pygame

pygame.init()
screen = pygame.display.set_mode((800 , 700) , pygame.RESIZABLE)
pygame.display.set_caption("Juno :D")
# font = pygame.font.SysFont("Arial" , 30)
img = pygame.image.load("assets/kiriko-juno1.png").convert_alpha()

def draw_window(img_info):
    screen.fill((147,204,207))
    screen.blit(img , (img_info.x , img_info.y))
    pygame.display.update()

def main():
    juno_info = pygame.Rect(0,0 , img.get_width() , img.get_height())
    status: bool = True
    while status:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                status = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            juno_info.x = juno_info.x - 1
        elif keys[pygame.K_d]:
            juno_info.x = juno_info.x + 1
        elif keys[pygame.K_w]:
            juno_info.y = juno_info.y - 1
        elif keys[pygame.K_s]:
            juno_info.y = juno_info.y + 1
        elif keys[pygame.K_q]:
            pygame.quit()

        draw_window(juno_info)

    pygame.quit()

if __name__ == "__main__":
    main()
