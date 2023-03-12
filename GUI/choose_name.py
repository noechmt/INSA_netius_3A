import pygame

from Class.Button import Button
from Class.Input_box import InputBox
from Class.Text import Text


def choose_name():

    pygame.init()

    # Create screen variable and set the size of the screen
    SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    # Get the size of the user's screen
    WIDTH_SCREEN, HEIGHT_SCREEN = SCREEN.get_size()

    SCREEN.fill((0, 0, 0))

    # Set the caption of the window as Caesar III²
    pygame.display.set_caption('Quintus III')

    # Load the picture and scale it to the full size
    background_image = pygame.image.load(
        "GUI/Images/Choose Name/Background.png")
    SCREEN.blit(pygame.transform.scale(
        background_image, (WIDTH_SCREEN, HEIGHT_SCREEN)), (0, 0))

    # Create the rectangle for the menu
    (width_menu, height_menu) = (WIDTH_SCREEN / 3, HEIGHT_SCREEN / 5)
    (left_menu, top_menu) = (WIDTH_SCREEN / 3, 2 * HEIGHT_SCREEN / 5)
    menu_background = pygame.image.load(
        "GUI/Images/Choose Name/Menu_background.jpg")
    SCREEN.blit(pygame.transform.scale(
        menu_background, (width_menu, height_menu)), (left_menu, top_menu))

    # Text choose a name
    (width_text_name, height_text_name) = (width_menu, height_menu / 3)
    (left_text_name, top_text_name) = (left_menu, top_menu)
    text_name_font = pygame.font.Font(
        "GUI/Fonts/Title Screen/Berry Rotunda.ttf", 30)
    text_name = Text(left_text_name, top_text_name,
                     width_text_name, height_text_name, "Please enter your name", text_name_font)
    text_name.draw(SCREEN)

    # Input box for the username
    (width_input_name, height_input_name) = (
        width_menu - width_menu / 10, height_menu / 3)
    (left_input_name, top_input_name) = (
        left_menu + width_menu / 20, top_menu + height_menu / 3)
    input_name_font = pygame.font.Font(
        "GUI/Fonts/Title Screen/Berry Rotunda.ttf", 25)
    input_name = InputBox(left_input_name, top_input_name, width_input_name,
                          height_input_name, input_name_font, 25, "Governor")
    input_name.draw(SCREEN)

    # Continue button/text
    (width_text_continue, height_text_continue) = (
        width_menu / 3, height_menu / 3)
    (left_text_continue, top_text_continue) = (
        left_menu + 2 * width_menu / 3, top_menu + 2 * height_menu / 3)
    text_continue_font = pygame.font.Font(
        "GUI/Fonts/Title Screen/Berry Rotunda.ttf", 20)
    text_continue = Text(left_text_continue, top_text_continue, width_text_continue,
                         height_text_continue, "Continue", text_continue_font)
    text_continue.draw(SCREEN)

    # Back button/text
    (width_text_back, height_text_back) = (width_menu / 3, height_menu / 3)
    (left_text_back, top_text_back) = (
        left_menu, top_menu + 2 * height_menu / 3)
    text_back_font = pygame.font.Font(
        "GUI/Fonts/Title Screen/Berry Rotunda.ttf", 20)
    text_back = Text(left_text_back, top_text_back,
                     width_text_back, height_text_back, "Back", text_back_font)
    text_back.draw(SCREEN)

    # Display the window
    pygame.display.flip()

    fps_font = pygame.font.Font("GUI/Fonts/Title Screen/Berry Rotunda.ttf", 16)
    # Loop that check if the user wants to close the window
    running = True
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    while running:
        # for loop through the event queue
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            # Check for QUIT event
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                text_back.handle_hover_text(pos, SCREEN)
                text_continue.handle_hover_text(pos, SCREEN)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if text_back.is_hovered(pos):
                    return False
                if text_continue.is_hovered(pos):
                    if input_name.get_text() != '':
                        file = open("Saves/.temp.txt", "w")
                        file.write(input_name.get_text())
                        file.close()
                        return True
            if (input_name.handle_event(event, SCREEN)):
                SCREEN.blit(pygame.transform.scale(
                    menu_background, (width_menu, height_menu)), (left_menu, top_menu))
                SCREEN.blit(pygame.transform.scale(background_image,
                            (WIDTH_SCREEN, HEIGHT_SCREEN)), (0, 0))
                SCREEN.blit(pygame.transform.scale(menu_background,
                            (width_menu, height_menu)), (left_menu, top_menu))
                text_name.draw(SCREEN)
                input_name.draw(SCREEN)
                text_back.draw(SCREEN)
                text_continue.draw(SCREEN)
        # Set the FPS at 60
        clock.tick(60)

        # Update the screen
        pygame.display.flip()
