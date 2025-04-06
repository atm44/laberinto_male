
from load_global_variables import *


def draw_text(text, size, color, center,screen):
    font_obj = pygame.font.SysFont(FONT_NAME, size)
    text_surface = font_obj.render(text, True, color)
    rect = text_surface.get_rect(center=center)
    screen.blit(text_surface, rect)

def draw_button(rect, text,screen):
    pygame.draw.rect(screen, BLUE, rect)
    pygame.draw.rect(screen, WHITE, rect, 2)
    draw_text(text, 24, WHITE, rect.center,screen)

def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()