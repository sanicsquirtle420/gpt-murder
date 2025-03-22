from characters.juno import *
import pygame

def main():
    pygame.init()
    win = pygame.display.set_mode((1000, 800), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Deep Murder (Juno / beta version)")
    j: Juno = Juno(50, 50, speed=10)
    border = pygame.Rect(0, 0, win.get_width(), win.get_height())
    status: bool = True
    while status:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = False
            elif event.type == pygame.VIDEORESIZE:
                border = pygame.Rect(0, 0, win.get_width(), win.get_height())
        keys = pygame.key.get_pressed()
        j.move(keys, border)
        draw_window(j, border , win)

    pygame.quit()

def draw_window(sample_char, barrier , window):
    window.fill((147, 204, 207))
    sample_char.draw(window)
    pygame.draw.rect(window, (189 , 52 , 235), barrier, 10)
    pygame.display.update()

if __name__ == "__main__":
    main()
