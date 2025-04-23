import pygame, sys, random
from button import Button

VELIKOST_CTVERCE = 30
SLOUPCE = 10
RADKY = 20
SIRKA_MRIZKY = SLOUPCE * VELIKOST_CTVERCE
VYSKA_MRIZKY = RADKY * VELIKOST_CTVERCE

high_score = 0

pygame.init()
pygame.mixer.init()  # zvuk

def play_music(track):
    pygame.mixer.music.stop()  
    pygame.mixer.music.load(track)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

SCREEN = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.display.set_caption("Menu")

grid = [[None for _ in range(SLOUPCE)] for _ in range(RADKY)]

def draw_score(surface):
    font = get_font(36)
    text = font.render(f"Skóre: {score}", True, (255, 255, 255))
    surface.blit(text, (20, 20))

# Funkce pro kontrolu a odstranění plných řádků
def remove_full_rows():
    global grid, score
    new_grid = [[None for _ in range(SLOUPCE)] for _ in range(RADKY)]
    new_row_index = RADKY - 1
    removed_rows = 0

    for y in range(RADKY - 1, -1, -1):  # Procházení řádků odspodu
        if None in grid[y]:  # Řádek **není** plný, zkopírujeme ho do nové mřížky
            new_grid[new_row_index] = grid[y]
            new_row_index -= 1
        else:  # Plný řádek **odstraníme**
            removed_rows += 1

    # Přidáme nové prázdné řádky na vrchol
    for i in range(removed_rows):
        new_grid[i] = [None for _ in range(SLOUPCE)]

    grid = new_grid  # Aktualizujeme herní mřížku

    if removed_rows > 0:
        score += removed_rows * 100  # Zvýšení skóre na základě počtu odstraněných řádků

def add_to_grid(shape, pos, color):
    """ Přidání tvaru do mřížky po dopadu """
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                grid[pos[1] + y][pos[0] + x] = color

    remove_full_rows()  # Po přidání tvaru zkontrolujeme plné řádky

def draw_high_score(surface):
    """ Zobrazení nejvyššího skóre v hlavním menu """
    font = get_font(50)
    text = font.render(f"Nejvyšší skóre: {high_score}", True, (255, 255, 255))
    screen_width, screen_height = SCREEN.get_size()
    center_x = screen_width // 2
    SCREEN.blit(text, (center_x - text.get_width() // 2, 650))  # Pod tlačítky

def update_high_score():
    """ Aktualizace nejvyššího skóre po skončení hry """
    global high_score
    if score > high_score:
        high_score = score

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
    """ Kreslení mřížky a pevně usazených bloků """
    offset_x = (surface.get_width() - SIRKA_MRIZKY) // 2
    offset_y = (surface.get_height() - VYSKA_MRIZKY) // 2

    # Nakreslení mřížky
    pygame.draw.rect(surface, (30, 30, 30), (offset_x, offset_y, SIRKA_MRIZKY, VYSKA_MRIZKY))

    for y in range(RADKY):
        for x in range(SLOUPCE):
            rect = pygame.Rect(offset_x + x * VELIKOST_CTVERCE, offset_y + y * VELIKOST_CTVERCE,
                               VELIKOST_CTVERCE, VELIKOST_CTVERCE)
            pygame.draw.rect(surface, (80, 80, 80), rect, 1)

            # Pokud existuje blok v mřížce, vykreslíme ho
            if grid[y][x]:
                pygame.draw.rect(surface, grid[y][x], rect)

def draw_shape(surface, shape, pos, color):
    """ Kreslí aktuální tvar na mřížku s jemným ohraničením """
    offset_x = (surface.get_width() - SIRKA_MRIZKY) // 2
    offset_y = (surface.get_height() - VYSKA_MRIZKY) // 2

    border_color = (max(0, color[0] - 50), max(0, color[1] - 50), max(0, color[2] - 50))  # Tmavší varianta barvy

    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(offset_x + (pos[0] + x) * VELIKOST_CTVERCE,
                                   offset_y + (pos[1] + y) * VELIKOST_CTVERCE,
                                   VELIKOST_CTVERCE, VELIKOST_CTVERCE)

                pygame.draw.rect(surface, color, rect)  # Hlavní barva tvaru
                pygame.draw.rect(surface, border_color, rect, 2)  # Jemné ohraničení



def check_collision(shape, pos):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                new_x = pos[0] + x
                new_y = pos[1] + y
                if new_x < 0 or new_x >= SLOUPCE or new_y >= RADKY:
                    return True  # mimo okraj
                if new_y >= 0 and grid[new_y][new_x] is not None:
                    return True  # kolize s existujícím tvarem
    return False

def game_over_screen(screen):
    screen_width, screen_height = SCREEN.get_size()
    center_x = screen_width // 2
    font = get_font(36)
    text = font.render('Konec hry', True, (60, 0, 0))
    screen.blit(text, (300, 20))
    pygame.display.update()
    pygame.time.delay(2000)

                

obtiznost = "Lehká"  # výchozí obtížnost


TVARY = {
    "I": {
        "shape": [[1, 1, 1, 1]],
        "color": (0, 255, 255)
    },
    "O": {
        "shape": [[1, 1], [1, 1]],
        "color": (255, 255, 0)
    },
    "T": {
        "shape": [[0, 1, 0], [1, 1, 1]],
        "color": (128, 0, 128)
    },
    "S": {
        "shape": [[0, 1, 1], [1, 1, 0]],
        "color": (0, 255, 0)
    },
    "Z": {
        "shape": [[1, 1, 0], [0, 1, 1]],
        "color": (255, 0, 0)
    },
    "J": {
        "shape": [[1, 0, 0], [1, 1, 1]],
        "color": (0, 0, 255)
    },
    "L": {
        "shape": [[0, 0, 1], [1, 1, 1]],
        "color": (255, 165, 0)
    }
}

def draw_next_shape(surface, shape):
    """ Nakreslí další tvar v malém okně vpravo nahoře """
    offset_x = SIRKA_MRIZKY + 50
    offset_y = 50

    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(offset_x + x * VELIKOST_CTVERCE, offset_y + y * VELIKOST_CTVERCE, 
                                   VELIKOST_CTVERCE, VELIKOST_CTVERCE)
                pygame.draw.rect(surface, (255, 255, 255), rect)

def rotate_shape(shape):
    """ Rotuje tvar pomocí transpozice a obrácení řádků """
    return [list(row) for row in zip(*shape[::-1])]

def adjust_position_within_bounds(shape, pos):
    width = len(shape[0])
    height = len(shape)

    new_x = max(0, min(SLOUPCE - width, pos[0]))
    new_y = max(0, min(RADKY - height, pos[1]))
    return [new_x, new_y]

def check_game_over():
    """ Kontrola, zda některý tvar dosáhl horní hranice mřížky """
    for x in range(SLOUPCE):
        if grid[0][x] is not None:
            return True
    return False

def play():
    global grid, score
    grid = [[None for _ in range(SLOUPCE)] for _ in range(RADKY)]  # Reset grid
    score = 0  # Reset skóre při začátku hry
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.5  # Výchozí rychlost pádu bloků

    current_piece = random.choice(list(TVARY.values()))
    next_piece = random.choice(list(TVARY.values()))
    shape_pos = [3, 0]

    while True:
        screen_width, screen_height = SCREEN.get_size()
        center_x = screen_width // 2
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        dt = clock.tick(60) / 1000
        fall_time += dt

        # **Aktualizace rychlosti na základě skóre**
        fall_speed = max(0.1, 0.5 - (score // 500) * 0.05)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    update_high_score()
                    return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_pos = [shape_pos[0] - 1, shape_pos[1]]
                    if not check_collision(current_piece["shape"], new_pos):
                        shape_pos = new_pos
                elif event.key == pygame.K_RIGHT:
                    new_pos = [shape_pos[0] + 1, shape_pos[1]]
                    if not check_collision(current_piece["shape"], new_pos):
                        shape_pos = new_pos
                elif event.key == pygame.K_DOWN:
                    if not check_collision(current_piece["shape"], [shape_pos[0], shape_pos[1] + 1]):
                        shape_pos[1] += 1
                elif event.key == pygame.K_SPACE:
                    while not check_collision(current_piece["shape"], [shape_pos[0], shape_pos[1] + 1]):
                        shape_pos[1] += 1
                elif event.key == pygame.K_UP:
                    rotated = rotate_shape(current_piece["shape"])
                    if not check_collision(rotated, shape_pos):
                        current_piece["shape"] = rotated

        if fall_time > fall_speed:
            if not check_collision(current_piece["shape"], [shape_pos[0], shape_pos[1] + 1]):
                shape_pos[1] += 1
            else:
                if check_game_over():
                    update_high_score()
                    game_over_screen(SCREEN)
                    return
                add_to_grid(current_piece["shape"], shape_pos, current_piece["color"])
                current_piece = next_piece
                next_piece = random.choice(list(TVARY.values()))
                shape_pos = [3, 0]
            fall_time = 0

        SCREEN.fill((0, 0, 0))
        SCREEN.blit(get_scaled_bg(), (0, 0))
        OPTIONS_BACK = Button(image=None, pos=(70, 100),
                              text_input="Zpět", font=get_font(75),
                              base_color="White", hovering_color="Black", base_color2="Red")
        OPTIONS_BACK.changeHoverColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        draw_grid(SCREEN)
        draw_shape(SCREEN, current_piece["shape"], shape_pos, current_piece["color"])
        draw_shape(SCREEN, next_piece["shape"], [SLOUPCE + 2, 2], next_piece["color"])
        draw_score(SCREEN)  # Zobrazení skóre

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
                              text_input="Zpět", font=get_font(75),
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

        MENU_TEXT = get_font(100).render("Hlavní Menu", True, "#b68f40")
        screen_width, screen_height = SCREEN.get_size()
        center_x = screen_width // 2
        MENU_RECT = MENU_TEXT.get_rect(center=(center_x, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(center_x, 250), 
                            text_input="Hrát", font=get_font(75), base_color="#d7fcd4", hovering_color="White", base_color2=None)
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(center_x, 400), 
                            text_input="Obtížnost", font=get_font(75), base_color="#d7fcd4", hovering_color="White", base_color2=None)
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(center_x, 550), 
                            text_input="Zavřít", font=get_font(75), base_color="#d7fcd4", hovering_color="White", base_color2=None)

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeHoverColor(MENU_MOUSE_POS)
            button.update(SCREEN)
            
        draw_high_score(SCREEN)
        
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