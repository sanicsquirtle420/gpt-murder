import pygame
from characters.juno import *
from characters.npc import *
import random
from utilities.data import *

def main():
    pygame.init()
    main_theme =  pygame.mixer.Sound('audio/main_theme.mp3')
    main_theme.play()
    win = pygame.display.set_mode((1419, 734), pygame.RESIZABLE)
    bg = pygame.image.load("assets/Sprites/Setting/Map.png")
    world_width, world_height = bg.get_size()
    world_width *= 2
    world_height *= 2
    clock = pygame.time.Clock()
    pygame.display.set_caption("Deep Murder (Juno / beta version)")
    j: Juno = Juno(world_width // 2, world_height // 2, speed=10)
    npcs: list[NPC] = []
    for character in CHARACTERS:
        npc = NPC(character, win,)
        if npc.rect.right > world_width:
            npc.rect.right = world_width
        if npc.rect.bottom > world_height:
            npc.rect.bottom = world_height
        npcs.append(npc)
    border = pygame.Rect(0, 0, world_width, world_height)
    
    # Button settings (moved to left corner and made circular)
    button_center = (50, 50)
    button_radius = 30
    show_text = False  # Flag to control text display
    
    status: bool = True
    while status:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = False
            elif event.type == pygame.VIDEORESIZE:
                border = pygame.Rect(0, 0, world_width, world_height)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (event.pos[0] - button_center[0])**2 + (event.pos[1] - button_center[1])**2 <= button_radius**2:
                    show_text = not show_text  # Toggle text visibility
        
        keys = pygame.key.get_pressed()
        j.move(keys , border,  npcs)
        j.animate(60/1000)
        offset_x = max(0, min(j.rect.x - win.get_width() // 2 + j.rect.width // 2, world_width - win.get_width()))
        offset_y = max(0, min(j.rect.y - win.get_height() // 2 + j.rect.height // 2, world_height - win.get_height()))
        
        draw_window(j, npcs, border, win, offset_x, offset_y, button_center, button_radius, show_text)
    
    pygame.quit()

def draw_window(player, npcs: list[NPC], barrier, window, x, y, button_center, button_radius, show_text):
    bg = pygame.image.load("assets/Sprites/Setting/Map.png")
    width, height = bg.get_size()
    scaled_bg = pygame.transform.scale(bg, (width * 2, height * 2))
    window.blit(scaled_bg, (-x, -y))
    
    keys = pygame.key.get_pressed()
    pygame.draw.rect(window, (189, 52, 235), (0, 0, window.get_width(), window.get_height()), 10)
    
    for npc in npcs:
        npc.move()
        npc.animate(60/1000)
        npc.draw(window, x, y)
    
    sorted_npc = sorted(npcs, key=lambda npc: player.distance_to(npc))
    player.draw(window, x, y)
    
    for npc in sorted_npc:
        if player.near_character(npc) and keys[pygame.K_p]:
            font = pygame.font.SysFont("Arial", 30)
            text = font.render("Interaction text", False, (0, 0, 0))
            text_x, text_y = 25, window.get_height() - 100
            text_rect = text.get_rect(topleft=(text_x, text_y))
            pygame.draw.rect(window, (255, 255, 255), (text_rect.left - 8, text_rect.top - 8, text.get_width() + 16, text.get_height() + 16))
            window.blit(text, (25, window.get_height() - 100))
            break
    
    # Draw circular button
    pygame.draw.circle(window, (0, 150, 255), button_center, button_radius)
    font = pygame.font.SysFont("Arial", 20)
    text_surface = font.render("B", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=button_center)
    window.blit(text_surface, text_rect)
    
    # Display text on button click
    if show_text:
        text_box = pygame.Rect(50, 50, 300, 100)
        pygame.draw.rect(window, (255, 255, 255), text_box)
        text = font.render("Hello, this is a message!", True, (0, 0, 0))
        window.blit(text, (text_box.x + 10, text_box.y + 40))
    
    pygame.display.update()

if __name__ == "__main__":
    main()
