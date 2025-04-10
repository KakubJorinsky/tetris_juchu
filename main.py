import pygame, sys
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green", base_color2=None)

        PLAY_BACK.changeHoverColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()
    
def options():
    selected_option = "Lehká"
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("Nastavení obtížnosti", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 60))
        
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        
        OPTION_1 = Button(image=None, pos=(640, 240),
                          text_input="Lehká", font=get_font(75), base_color="Black", hovering_color="Green", base_color2="Red")

        OPTION_2 = Button(image=None, pos=(640, 340),
                          text_input="Střední", font=get_font(75), base_color="Black", hovering_color="Green", base_color2="Red")

        OPTION_3 = Button(image=None, pos=(640, 440),
                          text_input="Těžká", font=get_font(75), base_color="Black", hovering_color="Green", base_color2="Red")
        
        if selected_option == "Lehká":
            OPTION_1.text = get_font(75).render("Lehká", True, "Red")
        else:
            OPTION_1.changeHoverColor(OPTIONS_MOUSE_POS)

        if selected_option == "Střední":
            OPTION_2.text = get_font(75).render("Střední", True, "Red")
        else:
            OPTION_2.changeHoverColor(OPTIONS_MOUSE_POS)

        if selected_option == "Těžká":
            OPTION_3.text = get_font(75).render("Těžká", True, "Red")
        else:
            OPTION_3.changeHoverColor(OPTIONS_MOUSE_POS)
        
        OPTIONS_BACK = Button(image=None, pos=(640, 660), 
                            text_input="ZPĚT", font=get_font(75), base_color="Black", hovering_color="Green", base_color2="Red")
        
        OPTION_1.changeHoverColor(OPTIONS_MOUSE_POS)
        OPTION_2.changeHoverColor(OPTIONS_MOUSE_POS)
        OPTION_3.changeHoverColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.changeHoverColor(OPTIONS_MOUSE_POS)
        OPTION_1.update(SCREEN)
        OPTION_2.update(SCREEN)
        OPTION_3.update(SCREEN)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTION_1.checkForInput(OPTIONS_MOUSE_POS):
                    selected_option = "Lehká"
                if OPTION_2.checkForInput(OPTIONS_MOUSE_POS):
                    selected_option = "Střední"
                if OPTION_3.checkForInput(OPTIONS_MOUSE_POS):
                    selected_option = "Těžká"


        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("HLAVNÍ MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="HRÁT", font=get_font(75), base_color="#d7fcd4", hovering_color="White", base_color2=None)
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="OBTÍŽNOST", font=get_font(75), base_color="#d7fcd4", hovering_color="White", base_color2=None)
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
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