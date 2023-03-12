import pygame
from os import walk
from Class.Button import Button
from GUI.choose_name import choose_name


def choosing_save_window(screen):
    # Background for the choice
    (width_menu, height_menu) = (
        screen.get_size()[0] - 2*screen.get_size()[0]/10, screen.get_size()[1] - 2*screen.get_size()[1]/10)
    (left_menu, top_menu) = (screen.get_size()
                             [0] / 10, screen.get_size()[1] / 10)
    menu_background = pygame.image.load(
        "GUI/Images/Title screen/Menu_background.jpg")
    screen.blit(pygame.transform.scale(
        menu_background, (width_menu, height_menu)), (left_menu, top_menu))

    start_game_button = Button(screen.get_size()[0]/10, screen.get_size()[1]/10, width_menu,
                               height_menu / 15, text="Charger une partie")
    start_game_button.draw(screen)

    listeFichiers = []
    left_first_save = screen.get_size()[0] / 10
    top_first_save = 3*screen.get_size()[1] / 15
    height_first_save = screen.get_size()[1] / 15
    width_first_save = screen.get_size()[0] / 6
    i = 0
    u = 0
    blanc = pygame.image.load("GUI/Images/blanc.png")
    for (repertoire, sousRepertoires, fichiers) in walk("Saves/"):
        for fichier in fichiers:
            if fichier[0] != '.':
                if (i == 9):
                    i = 0
                    u += 1
                listeFichiers.append(Button(left_first_save, top_first_save + i*height_first_save,
                                            width_first_save + u*2*width_first_save, height_first_save, image=blanc, text=str(fichier)))
                i += 1
    for fichier in listeFichiers:
        fichier.draw(screen)
    return listeFichiers


def title_screen():

    pygame.init()

    # Create screen variable and set the size of the screen
    SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    # Get the size of the user's screen
    WIDTH_SCREEN, HEIGHT_SCREEN = SCREEN.get_size()

    # Set the caption of the window as Caesar III
    pygame.display.set_caption('Quintus III')

    # Load the picture and scale it to the full size
    background_image = pygame.image.load(
        "GUI/Images/Title screen/Background.png")
    SCREEN.blit(pygame.transform.scale(
        background_image, (WIDTH_SCREEN, HEIGHT_SCREEN)), (0, 0))

    # Create the rectangle for the menu
    (width_menu, height_menu) = (WIDTH_SCREEN / 5, HEIGHT_SCREEN / 3)
    (left_menu, top_menu) = (2 * WIDTH_SCREEN / 5, HEIGHT_SCREEN / 3)
    menu_background = pygame.image.load(
        "GUI/Images/Title screen/Menu_background.jpg")
    SCREEN.blit(pygame.transform.scale(
        menu_background, (width_menu, height_menu)), (left_menu, top_menu))

    # We want to keep the ration of the logo so height is width/3 as in the original size
    width_logo = width_menu - 2 * WIDTH_SCREEN / 60
    height_logo = width_logo / 3
    (left_logo, top_logo) = (left_menu +
                             WIDTH_SCREEN / 60, top_menu + HEIGHT_SCREEN / 60)
    logo_menu = pygame.image.load(
        "GUI/Images/Title screen/Logo_menu.png")
    SCREEN.blit(pygame.transform.scale(
        logo_menu, (width_logo, height_logo)), (left_logo, top_logo))

    logo_background = pygame.image.load(
        "GUI/Images/Title screen/Logo_background.jpg")

    width_buttons = width_logo
    height_buttons = height_logo // 2
    left_buttons = left_logo

    top_start_button = top_logo + height_logo + HEIGHT_SCREEN / 30
    start_game_button = Button(left_buttons, top_start_button, width_buttons,
                               height_buttons, image=logo_background, text="Commencer une partie")
    start_game_button.draw(SCREEN)

    top_load_button = top_start_button + height_buttons + HEIGHT_SCREEN / 100
    load_game_button = Button(left_buttons, top_load_button, width_buttons,
                              height_buttons, image=logo_background, text="Charger une partie")
    load_game_button.draw(SCREEN)

    top_leave_button = top_load_button + height_buttons + HEIGHT_SCREEN / 100
    leave_game_button = Button(left_buttons, top_leave_button, width_buttons,
                               height_buttons, image=logo_background, text="Quittez le jeu")
    leave_game_button.draw(SCREEN)

    # Display the window
    pygame.display.flip()

    fps_font = pygame.font.Font("GUI/Fonts/Title Screen/Berry Rotunda.ttf", 16)
    # Loop that check if the user wants to close the window
    running = True
    window_name = False
    choosing_save = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    while running:
        # for loop through the event queue
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            # Check for QUIT event
            if event.type == pygame.QUIT:
                running = False
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not choosing_save:
                    if leave_game_button.is_hovered(pos):
                        running = False
                        return False
                    if start_game_button.is_hovered(pos):
                        window_name = True
                        running = False
                    if load_game_button.is_hovered(pos):
                        choosing_save = True
                        listeFichiers = choosing_save_window(SCREEN)

                        file = open("Saves/.temp.txt", "w")
                else:
                    for fichier in listeFichiers:
                        if fichier.is_hovered(pos):
                            file.write("Saves/" + str(fichier.get_text()))
                            return True

            if event.type == pygame.MOUSEMOTION:
                if not choosing_save:
                    start_game_button.handle_hover_button(pos, SCREEN)
                    load_game_button.handle_hover_button(pos, SCREEN)
                    leave_game_button.handle_hover_button(pos, SCREEN)
                else:
                    for fichier in listeFichiers:
                        fichier.handle_hover_button(pos, SCREEN)

            if choosing_save:
                if event.type == pygame.KEYDOWN:
                    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                        return title_screen()

        # Set the FPS at 60
        clock.tick(60)

        # Update the screen
        pygame.display.flip()

    if window_name:
        # We display again this window if the back button is pressed from choose_name
        if (not choose_name()):
            title_screen()

        return True
