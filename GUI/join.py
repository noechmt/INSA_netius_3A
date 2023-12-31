import pygame

from Class.Button import Button
from Class.Input_box import InputBox
from Class.Text import Text
import threading as thread
import Class.Encoder as encode
import p2p.socket_python as spy
import subprocess
from time import sleep

def join_game():

    pygame.init()
    server = spy.Server(1235, 4)
    spy.Spython()
    spy.Spython.startThread()



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
    (width_menu, height_menu) = (WIDTH_SCREEN / 3, HEIGHT_SCREEN / 3)
    (left_menu, top_menu) = (WIDTH_SCREEN / 3, 2 * HEIGHT_SCREEN / 5)
    menu_background = pygame.image.load(
        "GUI/Images/Choose Name/Menu_background.jpg")
    SCREEN.blit(pygame.transform.scale(
        menu_background, (width_menu, height_menu)), (left_menu, top_menu))

    # Text "Rejoindre un server"
    (width_text_join, height_text_join) = (width_menu, height_menu / 3)
    (left_text_join, top_text_join) = (left_menu, top_menu)
    text_join_font = pygame.font.Font(
        "GUI/Fonts/Title Screen/Berry Rotunda.ttf", 30)
    text_join = Text(left_text_join, top_text_join,
                     width_text_join, height_text_join, "Rejoindre une partie", text_join_font)
    text_join.draw(SCREEN)

    # Text IP
    (width_text_ip, height_text_ip) = (
        width_menu - width_menu / 10, height_menu / 8)
    (left_text_ip, top_text_ip) = (left_menu -
                                   width_menu / 3, top_text_join + height_menu / 3)
    text_ip_font = pygame.font.Font(
        "GUI/Fonts/Title Screen/Berry Rotunda.ttf", 30)
    text_ip = Text(left_text_ip, top_text_ip,
                   width_text_ip, height_text_ip, "Ip", text_ip_font)
    text_ip.draw(SCREEN)

    # Input box for the game IP
    (width_input_ip, height_input_ip) = (
        width_menu - width_menu / 3, height_menu / 8)
    (left_input_ip, top_input_ip) = (
        left_menu + width_menu / 4, top_text_ip)
    input_ip_font = pygame.font.Font(
        "GUI/Fonts/Title Screen/Berry Rotunda.ttf", 25)
    input_ip = InputBox(left_input_ip, top_input_ip, width_input_ip,
                        height_input_ip, input_ip_font, 25, "192.168.")
    input_ip.draw(SCREEN)

    # Text pseudo
    (width_text_pseudo, height_text_pseudo) = (
        width_menu - width_menu / 10, height_menu / 8)
    (left_text_pseudo, top_text_pseudo) = (
        left_menu - width_menu / 3, top_text_ip + height_menu / 5)
    text_pseudo_font = pygame.font.Font(
        "GUI/Fonts/Title Screen/Berry Rotunda.ttf", 30)
    text_pseudo = Text(left_text_pseudo, top_text_pseudo,
                       width_text_pseudo, height_text_pseudo, "Pseudo", text_pseudo_font)
    text_pseudo.draw(SCREEN)

    # Input box for the game pseudo
    (width_input_pseudo, height_input_pseudo) = (
        width_menu - width_menu / 3, height_menu / 8)
    (left_input_pseudo, top_input_pseudo) = (
        left_menu + width_menu / 4, top_text_pseudo)
    input_pseudo_font = pygame.font.Font(
        "GUI/Fonts/Title Screen/Berry Rotunda.ttf", 25)
    input_pseudo = InputBox(left_input_pseudo, top_input_pseudo, width_input_pseudo,
                            height_input_pseudo, input_pseudo_font, 25, "Player1")
    input_pseudo.draw(SCREEN)

    # Connect button/text
    (width_text_connect, height_text_connect) = (
        width_menu / 3, height_menu / 3)
    (left_text_connect, top_text_connect) = (
        left_menu + 2 * width_menu / 3, top_menu + 2 * height_menu / 3)
    text_connect_font = pygame.font.Font(

        "GUI/Fonts/Title Screen/Berry Rotunda.ttf", 20)
    text_connect = Text(left_text_connect, top_text_connect, width_text_connect,
                        height_text_connect, "Connect", text_connect_font)
    text_connect.draw(SCREEN)

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
                text_connect.handle_hover_text(pos, SCREEN)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if text_back.is_hovered(pos):
                    spy.Spython.endThread()
                    spy.Server.socket.close()
                    return (False, False)
                if text_connect.is_hovered(pos):
                    if input_pseudo.get_text() != '':
                        file = open("Saves/temp.txt", "w")
                        file.write(input_pseudo.get_text())
                        file.close()
                        
                    spy.Spython.startLanProcess(input_ip.get_text())
                    sleep(1)
                    encode.join(input_pseudo.get_text())
                    return (True, False)

            if input_ip.handle_event(event, SCREEN):
                SCREEN.blit(pygame.transform.scale(
                    menu_background, (width_menu, height_menu)), (left_menu, top_menu))
                SCREEN.blit(pygame.transform.scale(background_image,
                            (WIDTH_SCREEN, HEIGHT_SCREEN)), (0, 0))
                SCREEN.blit(pygame.transform.scale(menu_background,
                            (width_menu, height_menu)), (left_menu, top_menu))
                text_join.draw(SCREEN)
                text_ip.draw(SCREEN)
                text_pseudo.draw(SCREEN)
                text_back.draw(SCREEN)
                text_connect.draw(SCREEN)
                input_ip.darken = False
                input_pseudo.darken = False
                input_ip.draw(SCREEN)
                input_pseudo.draw(SCREEN)

            if input_pseudo.handle_event(event, SCREEN):
                SCREEN.blit(pygame.transform.scale(
                    menu_background, (width_menu, height_menu)), (left_menu, top_menu))
                SCREEN.blit(pygame.transform.scale(background_image,
                            (WIDTH_SCREEN, HEIGHT_SCREEN)), (0, 0))
                SCREEN.blit(pygame.transform.scale(menu_background,
                            (width_menu, height_menu)), (left_menu, top_menu))
                text_join.draw(SCREEN)
                text_ip.draw(SCREEN)
                text_pseudo.draw(SCREEN)
                text_back.draw(SCREEN)
                text_connect.draw(SCREEN)
                input_ip.darken = False
                input_pseudo.darken = False
                input_ip.draw(SCREEN)
                input_pseudo.draw(SCREEN)

        # Set the FPS at 60
        clock.tick(60)

        # Update the screen
        pygame.display.flip()
