from ui_helpers import *
from load_global_variables import *


def start_screen(clock,logo_img):
    global screen
    screen = pygame.display.set_mode((640, 480))
    name = ""
    active = False
    input_box = pygame.Rect(20, 120, 200, 36)

    while True:
        screen.fill(WHITE)
        draw_text("Laberinto de male", 48, BLACK, (320, 60),screen)
        draw_text("Nombre:", 24, BLACK, (65, 100),screen)

        pygame.draw.rect(screen, BLACK, input_box, 2)

        
        img = pygame.transform.smoothscale(logo_img, (400, 400))
        img_rect = img.get_rect(center=(420, 300))
        screen.blit(img, img_rect)
        
        name_to_show = "Escribe aquí..."
        if active:
            name_to_show = name


        draw_text(name_to_show, 24, BLACK, input_box.center,screen)

        btn_small = pygame.Rect(20, 180, 200, 40)
        btn_medium = pygame.Rect(20, 230, 200, 40)
        btn_large = pygame.Rect(20, 280, 200, 40)
        btn_exit = pygame.Rect(20, 340, 200, 40)

        draw_button(btn_small, "Pequeño (15x15)",screen)
        draw_button(btn_medium, "Mediano (21x21)",screen)
        draw_button(btn_large, "Grande (31x31)",screen)
        draw_button(btn_exit, "Salir",screen)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True  
                    pygame.draw.rect(screen, WHITE, input_box, 2)
                else:
                    active = False
                if btn_small.collidepoint(event.pos) and name:
                    return (15, 15, name)
                elif btn_medium.collidepoint(event.pos) and name:
                    return (21, 21, name)
                elif btn_large.collidepoint(event.pos) and name:
                    return (31, 31, name)
                elif btn_exit.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 12:
                        name += event.unicode

        clock.tick(30)