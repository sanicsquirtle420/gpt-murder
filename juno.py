import pygame

def main():
    pygame.init()

    # sets up the dimensions for the window (600 x 700)
    screen = pygame.display.set_mode((600 , 700) , pygame.RESIZABLE)
    font = pygame.font.SysFont("Arial" , 30)

    img = pygame.image.load("assets/kiriko-juno1.png").convert_alpha()

    status: bool = True
    while status:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = False
            elif event.type == pygame.VIDEORESIZE:
                # Handles screen resizing
                screen = pygame.display.set_mode((event.w , event.h) , pygame.RESIZABLE)

        screen_width , screen_height = screen.get_size()

        img_width = screen_width // 5
        img_height = screen_height // 5
        scaled_img = pygame.transform.scale(img , (img_width , img_height))

        img_x = (screen_width - img_width) // 2
        img_y = (screen_height - img_height) // 2

        text = font.render("Welcome to orbit!" , True , (0,0,0))
        text_x = (screen_width - text.get_width()) // 2
        text_y = screen_height - 100

        screen.fill((147 , 204 , 207))

        screen.blit(scaled_img , (img_x , img_y))
        screen.blit(text , (text_x , text_y))
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
