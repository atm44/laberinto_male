from load_global_variables import *
from ui_helpers import *

def win_screen(clock,victory_img):
    global screen
    screen = pygame.display.set_mode((640, 480))

    # Animación: variables
    scale = 1.0
    direction = 1
    max_scale = 1.5
    min_scale = 0.8
    scale_speed = 0.01

    while True:
        screen.fill(BLACK)
        draw_text(" ESCAPASTE! GENIAA! ", 36, GREEN, (320, 60),screen)

        # Animar la imagen (agrandar y achicar)
        scaled_size = int(128 * scale)
        img = pygame.transform.smoothscale(victory_img, (scaled_size, scaled_size))
        img_rect = img.get_rect(center=(320, 200))
        screen.blit(img, img_rect)

        # Botón volver
        btn_back = pygame.Rect(220, 360, 200, 50)
        draw_button(btn_back, "Volver al Menu",screen)

        pygame.display.flip()
        await asyncio.sleep(0)  # Give control back to the main thread
        # Lógica de animación
        scale += scale_speed * direction
        if scale >= max_scale or scale <= min_scale:
            direction *= -1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_back.collidepoint(event.pos):
                    return

        clock.tick(60)