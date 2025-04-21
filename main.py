import pygame, sys
from button import Button
import random
import time

VELIKOST_CTVERCE = 30
SLOUPCE = 10
RADKY = 20
SIRKA_MRIZKY = SLOUPCE * VELIKOST_CTVERCE
VYSKA_MRIZKY = RADKY * VELIKOST_CTVERCE

TVARY = {
    "I": [[1, 1, 1, 1]],
}

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.display.set_caption("Menu")

def get_scaled_bg():
    width, height = SCREEN.get_size()
    return pygame.transform.scale(pygame.image.load("assets/Background.png"), (width, height))

def get_scaled_bg2():
    width, height = SCREEN.get_size()
    return pygame.transform.scale(pygame.image.load("assets/Background2.png"), (width, height))

# Funkce pro získání dynamických offsetů pro mřížku
def get_grid_offset():
    screen_width, screen_height = SCREEN.get_size()
    offset_x = (screen_width - SIRKA_MRIZKY) // 2
    offset_y = (screen_height - VYSKA_MRIZKY) // 2
    return offset_x, offset_y

def draw_grid(surface):
    offset_x, offset_y = get_grid_offset()

    pygame.draw.rect(
        surface,
        (30, 30, 30),
        (offset_x, offset_y, SIRKA_MRIZKY, VYSKA_MRIZKY)
    )

    for y in range(RADKY):
        for x in range(SLOUPCE):
            rect = pygame.Rect(
                offset_x + x * VELIKOST_CTVERCE,
                offset_y + y * VELIKOST_CTVERCE,
                VELIKOST_CTVERCE,
                VELIKOST_CTVERCE
            )
            pygame.draw.rect(surface, (80, 80, 80), rect, 1)

def draw_shape(surface, shape, pos):
    offset_x, offset_y = get_grid_offset()

    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(
                    offset_x + (pos[0] + x) * VELIKOST_CTVERCE,
                    offset_y + (pos[1] + y) * VELIKOST_CTVERCE,
                    VELIKOST_CTVERCE,
                    VELIKOST_CTVERCE
                )
                pygame.draw.rect(surface, (0, 100, 255), rect)

obtiznost = "Lehká"  # výchozí obtížnost

def play():
    clock = pygame.time.Clock()
    fall_time = 0
    global obtiznost
    if obtiznost == "Lehká":
        fall_speed = 0.7
    elif obtiznost == "Střední":
        fall_speed = 0.4
    elif obtiznost == "Těžká":
        fall_speed = 0.2

    current_shape = TVARY["I"]
    shape_pos = [3, 0]  # x, y

    while True:
        dt = clock.tick(60) / 1000  # převedeno na vteřiny
        fall_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    shape_pos[0] -= 1
                elif event.key == pygame.K_RIGHT:
                    shape_pos[0] += 1
                elif event.key == pygame.K_DOWN:
                    shape_pos[1] += 1  # rychlejší pád

        if fall_time > fall_speed:
            shape_pos[1] += 1
            fall_time = 0

        SCREEN.blit(get_scaled_bg(), (0, 0))
        draw_grid(SCREEN)
        draw_shape(SCREEN, current_shape, shape_pos)

        pygame.display.update()

def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def options():
    global obtiznost
    selected_option = obtiznost

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("white")
        SCREEN.blit(get_scaled_bg2(), (0, 0))

        OPTIONS_TEXT = get_font(45).render("Nastavení obtížnosti", True, "Black")
        screen_width, screen_height = SCREEN.get_size()
        center_x = screen_width // 2
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(center_x, 60))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        options_list = [
            {"label": "Lehká", "pos": (center_x, 240)},
            {"label": "Střední", "pos": (center_x, 340)},
            {"label": "Těžká", "pos": (center_x, 440)}
        ]

        buttons = []

        for opt in options_list:
            is_selected = (selected_option == opt["label"])
            color = "Red" if is_selected else "Black"
            hover_color = "Yellow" if is_selected else "Green"

            btn = Button(image=None, pos=opt["pos"],
                         text_input=opt["label"], font=get_font(75),
                         base_color=color, hovering_color=hover_color, base_color2="Red")
            btn.changeHoverColor(OPTIONS_MOUSE_POS)
            btn.update(SCREEN)
            buttons.append((btn, opt))

        OPTIONS_BACK = Button(image=None, pos=(center_x, 660),
                              text_input="ZPĚT", font=get_font(75),
                              base_color="Black", hovering_color="Green", base_color2="Red")
        OPTIONS_BACK.changeHoverColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    print(f"Vybraná obtížnost: {selected_option}")
                    return

                for btn, opt in buttons:
                    if btn.checkForInput(OPTIONS_MOUSE_POS):
                        selected_option = opt["label"]
                        obtiznost = selected_option
                        break

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(get_scaled_bg(), (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("HLAVNÍ MENU", True, "#b68f40")
        screen_width, screen_height = SCREEN.get_size()
        center_x = screen_width // 2
        MENU_RECT = MENU_TEXT.get_rect(center=(center_x, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(center_x, 250), 
                            text_input="HRÁT", font=get_font(75), base_color="#d7fcd4", hovering_color="White", base_color2=None)
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(center_x, 400), 
                            text_input="OBTÍŽNOST", font=get_font(75), base_color="#d7fcd4", hovering_color="White", base_color2=None)
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(center_x, 550), 
                            text_input="ZAVŘÍT", font=get_font(75), base_color="#d7fcd4", hovering_color="White", base_color2=None)

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeHoverColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
