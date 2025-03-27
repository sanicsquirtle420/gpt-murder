from characters.npc import *
from utilities.data import *

def draw_window(player, npcs: list[NPC], window, x, y, button_center, button_radius, show_text):
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
            txt_w = window.get_width() - 100
            txt_h = window.get_height() // 10
            rect = pygame.Rect(50, window.get_height() - 200, txt_w, txt_h)
            font = pygame.font.SysFont("Arial", 30)
            tst_str = f"{npcs.index(npc)}: I draw the lovers is something tempting you. Let the kitsune guide you! Scaredy cat? But cats are the scariest creature of them all! Locking satelite vector."
            dialogue_box = render_textrect(tst_str, font, rect, justification=0)
            window.blit(dialogue_box, (rect.x , rect.y))
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

def render_textrect(string, font, rect ,justification=0):
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

    surface = pygame.Surface((rect.width , rect.height))
    surface.fill((255,255,255))

    off_y = 0
    for line in output:
        if off_y + font.get_height() > rect.width:
            break

        if justification == 0:
            txt_surface = font.render(line, True, (0,0,0))
        # I'm too lazy to type out the other justifications
        if justification == 0:
            surface.blit(txt_surface, (0, off_y))

        off_y += font.get_height()
    return surface
