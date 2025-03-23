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
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = False
            elif event.type == pygame.VIDEORESIZE:
                world_height = win.get_height() * 2
                world_width = win.get_width() * 2
                border = pygame.Rect(0, 0, world_width, world_height)
        keys = pygame.key.get_pressed()
        j.move(keys, border , npcs)
        j.animate(dt)
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
    keys = pygame.key.get_pressed()
    pygame.draw.rect(window, (189,52,235) , (0 - x, 0 - y, max_x , max_y) , 10)

    sample = ["welcome to orbit" , "let the kitsune guide you" , "i am ready to put on a show"]

    for npc in npcs:
        npc.move(barrier, player, npcs)
        npc.draw(window, x, y)

    sorted_npc = sorted(npcs , key=lambda npc: player.distance_to(npc))

    for npc in sorted_npc:
        if player.near_character(npc) and keys[pygame.K_p]:
            font = pygame.font.SysFont("Arial" , 30)
            text = font.render(sample[npcs.index(npc)] , False , (0,0,0))
            window.blit(text , (25, window.get_height() - 100))
            break

    window.blit(player.img , (player.rect.x - x , player.rect.y - y))

    pygame.display.update()

if __name__ == "__main__":
    main()
