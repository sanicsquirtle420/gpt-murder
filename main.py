import pygame
from characters.juno import *
from characters.npc import *
import random
from utilities.data import *

# Journal hints
journal_entries = [
    "Hint 1: Arrived at the town. Something feels off...",
    "Hint 2: Met a strange Botanist near the fountain.",
    "Hint 3: Found a clue near the well.",
    "Hint 4: The music in the forest changed suddenly...",
]

def draw_journal(window, entries, pos=(50, 160)):
    font = pygame.font.SysFont("Arial", 22)
    box_width = 700
    line_height = 32
    padding = 18
    visible_lines = len(entries)
    box_height = padding * 2 + line_height * visible_lines
    journal_box = pygame.Rect(pos[0], pos[1], box_width, box_height)

    pygame.draw.rect(window, (245, 245, 245), journal_box)  # Soft white background
    pygame.draw.rect(window, (0, 0, 0), journal_box, 2)      # Black border

    for idx, entry in enumerate(entries):
        text = font.render(entry, True, (0, 0, 0))
        window.blit(text, (pos[0] + padding, pos[1] + padding + idx * line_height))

def main():
    pygame.init()
    main_theme = pygame.mixer.Sound('audio/main_theme.mp3')
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

    # Button settings
    button_center = (50, 50)
    button_radius = 30
    show_text = False

    # Load journal icon
    journal_icon = pygame.image.load("assets/Sprites/UI/GUI/2 Buttons/book.png")
    journal_icon = pygame.transform.scale(journal_icon, (40, 40))

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
                    show_text = not show_text
        
        keys = pygame.key.get_pressed()
        j.move(keys , border,  npcs)
        j.animate(60/1000)
        offset_x = max(0, min(j.rect.x - win.get_width() // 2 + j.rect.width // 2, world_width - win.get_width()))
        offset_y = max(0, min(j.rect.y - win.get_height() // 2 + j.rect.height // 2, world_height - win.get_height()))
        
        draw_window(j, npcs, border, win, offset_x, offset_y, button_center, button_radius, show_text, journal_icon)
    
    pygame.quit()

def draw_window(player, npcs: list[NPC], barrier, window, x, y, button_center, button_radius, show_text, journal_icon):
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

    # Draw circular button with better background
    pygame.draw.circle(window, (40, 40, 40), button_center, button_radius)
    window.blit(journal_icon, journal_icon.get_rect(center=button_center))

    # Show journal if toggled
    if show_text:
        draw_journal(window, journal_entries)

    pygame.display.update()

if __name__ == "__main__":
    main()
