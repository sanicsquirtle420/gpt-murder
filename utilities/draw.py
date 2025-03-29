from characters.npc import *
from utilities.data import *

def draw_window(player, npcs, window, button_center, button_radius, show_text):
    bg = pygame.image.load("assets/Sprites/Setting/Map.png")
    width, height = bg.get_size()
    scaled_bg = pygame.transform.scale(bg, (width * 2, height * 2))
    world_height, world_width = window.get_height() * 2, window.get_width() * 2
    # x / y offsets
    x = max(0, min(player.rect.x - window.get_width() // 2 + player.rect.width // 2, world_width - window.get_width()))
    y = max(0, min(player.rect.y - window.get_height() // 2 + player.rect.height // 2, world_height - window.get_height()))
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
            txt_w = window.get_width() - 100
            txt_h = window.get_height() // 10
            rect = pygame.Rect(50, window.get_height() - 200, txt_w, txt_h)
            font = pygame.font.SysFont("Arial", 30)
            dialogue_box = render_textrect(npc.get_dialouge(), font, rect, (255,255,255))
            window.blit(dialogue_box, (rect.x , rect.y))
            break
    
    # Draw circular button
    pygame.draw.circle(window, (0, 150, 255), button_center, button_radius)
    font = pygame.font.SysFont("Arial", 20)
    text_surface = font.render("B", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=button_center)
    window.blit(text_surface, text_rect)
    
    # Display text on button click COLOR: (249,228,188)
    if show_text:
        text_box = pygame.Rect(25, 50, 400, 200)
        journal_box = render_textrect("Let the kitsune guide you! I draw the lovers... is something tempting you? I licked my wounds. Let's go." 
            , font, text_box, (249,228,188), justification=1)
        window.blit(journal_box, (text_box.x + 10, text_box.y + 40))
    
    pygame.display.update()

def render_textrect(string, font, rect, bg_color ,justification=0, max_height=175):
    # creates a rect object for long text
    output = []
    request = string.splitlines()
    for line in request:
        if font.size(str(request))[0] <= rect.width:
            output.append(line)
        else:
            words = line.split(" ")
            line = ""
            for word in words:
                test_l = f"{line} {word}".strip()
                if font.size(test_l)[0] <= rect.width:
                    line = test_l
                else:
                    output.append(line)
                    line = word
            
            output.append(line)

    total_h = len(output) * font.get_height()
    total_h = min(total_h, max_height)

    surface = pygame.Surface((rect.width , total_h), pygame.SRCALPHA)
    surface.fill((bg_color))

    off_y = 0
    for line in output:
        if off_y + font.get_height() > max_height:
            break

        if justification == 0:
            # left align
            text_surface = font.render(line, True, (0,0,0))
        elif justification == 1:
            # center
            text_surface = font.render(line, True, (0,0,0))
            text_rect = text_surface.get_rect(center=(rect.width // 2, off_y + font.get_height() // 2))
        if justification == 0:
            surface.blit(text_surface, (0, off_y))
        else:
            surface.blit(text_surface, text_rect.topleft)

        off_y += font.get_height()
    return surface