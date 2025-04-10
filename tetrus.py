import pygame
import sys

# Inicializace pygame
pygame.init()

# Nastavení okna
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('TeTrus')

# Fonty a barvy
font = pygame.font.SysFont('freesansbold.ttf', 50)
font_small = pygame.font.SysFont('freesansbold.ttf', 30)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Herní smyčky
menu_on = True
game_on = False

# Výchozí obtížnost
obtiznost = "Lehká"


while menu_on:
    screen.fill(BLACK)  # Černé pozadí
    
    # Získání aktuální velikosti okna
    WIDTH, HEIGHT = screen.get_size()
    
    # Vytvoření textů
    text_hrat = font.render('Hrát', True, WHITE)
    text_mezernik = font_small.render('[Mezerník]', True, WHITE)
    text_obtiznost = font_small.render('Vyberte obtížnost:', True, WHITE)
    text_obtiznost_volba = font_small.render('1 - Lehká   2 - Střední   3 - Těžká', True, WHITE)
    text_aktualni_obtiznost = font_small.render(f'Aktuální obtížnost: {obtiznost}', True, WHITE)
    print("jaj")
    # Výpočet pozic pro centrování
    text_hrat_rect = text_hrat.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    text_mezernik_rect = text_mezernik.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 50))
    text_obtiznost_rect = text_obtiznost.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    text_obtiznost_volba_rect = text_obtiznost_volba.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    text_aktualni_obtiznost_rect = text_aktualni_obtiznost.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    
    # Vykreslení textů
    screen.blit(text_hrat, text_hrat_rect)
    screen.blit(text_mezernik, text_mezernik_rect)
    screen.blit(text_obtiznost, text_obtiznost_rect)
    screen.blit(text_obtiznost_volba, text_obtiznost_volba_rect)
    screen.blit(text_aktualni_obtiznost, text_aktualni_obtiznost_rect)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu_on = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 or event.key == pygame.K_KP_1:
                obtiznost = "Lehká"
            elif event.key == pygame.K_2 or event.key == pygame.K_KP_2:
                obtiznost = "Střední"
            elif event.key == pygame.K_3 or event.key == pygame.K_KP_3:
                obtiznost = "Těžká"
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        menu_on = False
        game_on = True
    
    
while game_on:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False
            pygame.quit()
            sys.exit()
        
    keys = pygame.key.get_pressed()

    
pygame.display.update()
