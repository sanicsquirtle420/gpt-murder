# from api.api import main as initialize_game_data 
from characters.juno import *
from characters.npc import *
from utilities.draw import *
import pygame

# TEMPORARILY DISABLED AI TO WORK ON THE GAME ITSELF

def main():
    pygame.init()
    # initialize_game_data()
    print(characters)
    main_theme =  pygame.mixer.Sound('audio/main_theme.mp3')
    # main_theme.play()
    win = pygame.display.set_mode((1419, 734), pygame.RESIZABLE)
    bg = pygame.image.load("assets/Sprites/Setting/Map.png")
    world_width, world_height = bg.get_size()
    world_width *= 2
    world_height *= 2
    clock = pygame.time.Clock()
    pygame.display.set_caption("Deep Murder (Juno version)")
    j: Juno = Juno(world_width // 2, world_height // 2, speed=10)
    npcs: list[NPC] = []
    for character in characters:
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
        draw_window(j, npcs, win, button_center, button_radius, show_text)
    
    pygame.quit()

if __name__ == "__main__":
    main()