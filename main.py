from characters.juno import *
from characters.npc import *
import pygame
import random

def main():
    pygame.init()
    win = pygame.display.set_mode((1000, 800), pygame.RESIZABLE)
    world_width = win.get_width() * 2
    world_height = win.get_height() * 2
    clock = pygame.time.Clock()
    pygame.display.set_caption("Deep Murder (Juno / beta version)")
    j: Juno = Juno(world_width // 2, world_height // 2, speed=10)
    npcs: list[NPC] = []
    for i in range(3):
        rand_x = random.randint(15 , world_width - 15)
        rand_y = random.randint(15 , world_height - 15)
        npc = NPC(rand_x , rand_y, win)
        if npc.rect.right > world_width:
            npc.rect.right = world_width
        if npc.rect.bottom > world_height:
            npc.rect.bottom = world_height
        npcs.append(npc)
    border = pygame.Rect(0, 0, world_width, world_height)
    status: bool = True
    while status:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = False
            elif event.type == pygame.VIDEORESIZE:
                world_height = win.get_height() * 2
                world_width = win.get_width() * 2
                border = pygame.Rect(0, 0, world_width, world_height)
        keys = pygame.key.get_pressed()
        j.move(keys, border , npcs)
        offset_x = max(0, min(j.rect.x - win.get_width() // 2 + j.rect.width // 2, world_width - win.get_width()))
        offset_y = max(0, min(j.rect.y - win.get_height() // 2 + j.rect.height // 2, world_height - win.get_height()))

        for npc in npcs:
            npc.move(border , j , npcs)

        draw_window(j, npcs ,border , win, offset_x , offset_y)


    pygame.quit()

def draw_window(player, npcs: list[NPC] , barrier , window , x , y):
    window.fill((147, 204, 207))
    max_x = window.get_width() * 2
    max_y = window.get_height() * 2
    pygame.draw.rect(window, (189,52,235) , (0 - x, 0 - y, max_x , max_y) , 10)

    for npc in npcs:
        npc.move(barrier , player , npcs)
        npc.draw(window , x , y)

    window.blit(player.img , (player.rect.x - x , player.rect.y - y))

    pygame.display.update()

if __name__ == "__main__":
    main()
