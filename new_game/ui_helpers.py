
from load_global_variables import *


def draw_text(text, size, color, center,screen,aligment="center"):
    font_obj = pygame.font.SysFont(FONT_NAME, size)
    text_surface = font_obj.render(text, True, color)
    if aligment == "center":
        rect = text_surface.get_rect(center=center)
    elif aligment == "left":
        rect = text_surface.get_rect(topleft=center)
    elif aligment == "right":
        rect = text_surface.get_rect(topright=center)
    elif aligment == "top":
        rect = text_surface.get_rect(midtop=center)
    elif aligment == "bottom":     
        rect = text_surface.get_rect(midbottom=center)  
    elif aligment == "midleft":
        rect = text_surface.get_rect(midleft=center)
    elif aligment == "midright":
        rect = text_surface.get_rect(midright=center)
    
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

