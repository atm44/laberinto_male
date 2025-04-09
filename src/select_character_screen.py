from load_global_variables import *
from ui_helpers import *

def select_character_screen(clock):
    global screen
    screen = pygame.display.set_mode((640, 480))
    selected_image = None

    # Load and scale player images
    characters_selection = []
    characters_players = []
    for i in range(1, 4):
        img = pygame.image.load(f"./imagenes/player_{i}.png").convert_alpha()
        img = pygame.transform.scale(img, (CELL_SIZE*5, CELL_SIZE*5))
        img_player = pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE))
        characters_selection.append(img)
        characters_players.append(img_player)

    # Set positions
    positions = [
        (160, 200),
        (320, 200),
        (480, 200)
    ]

    while True:
        screen.fill(BLACK)
        draw_text("Elegí tu personaje", 36, WHITE, (320, 80),screen)

        # Draw images
        for i, img in enumerate(characters_selection):
            rect = img.get_rect(center=positions[i])
            screen.blit(img, rect)

        pygame.display.flip()
        await asyncio.sleep(0)  # Give control back to the main thread
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, pos in enumerate(positions):
                    rect = characters_selection[i].get_rect(center=pos)
                    if rect.collidepoint(event.pos):                        
                        return characters_players[i]  # Return the selected image
        
        clock.tick(60)

