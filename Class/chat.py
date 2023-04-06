import pygame
from Class.Text import Text
from Class.Input_box import InputBox


class Chat : 
    def __init__(self, screen) :
        self.chat_sprite = {
            "background" : pygame.image.load("game_screen/game_screen_sprites/chat_background.jpg").convert_alpha()
        }

        self.screen = screen
        self.width_screen, self.height_screen = self.screen.get_size()
        self.init_title()
        self.init_input()
        
    def init_title(self) :
        # top left corner title
        (width_menu, height_menu) = (self.width_screen/6, self.height_screen / 5)
        (left_menu, top_menu) = (self.width_screen, 2 * self.height_screen / 5)
        (width_text_name, height_text_name) = (width_menu, height_menu / 3)
        (left_text, top_text) = (left_menu*0.001, top_menu*0.001)
        text_font = pygame.font.Font(
            "GUI/Fonts/Title Screen/Berry Rotunda.ttf", 20)
        self.title = Text(left_text, top_text,
                        width_text_name, height_text_name, "IN-GAME chatroom", text_font)

    def init_input(self) : 
        #input box 
        (width_menu, height_menu) = (self.width_screen/6, self.height_screen / 5)
        (left_menu, top_menu) = (self.width_screen, 2 * self.height_screen / 5)
        (width_input_name, height_input_name) = (
        width_menu*2.3, height_menu / 6)
        (left_input_name, top_input_name) = (
            left_menu*0.025, top_menu)
        input_name_font = pygame.font.Font(
            "GUI/Fonts/Title Screen/Berry Rotunda.ttf", 15)
        self.input = InputBox(left_input_name, top_input_name, width_input_name,
                            height_input_name, input_name_font, 50, "")

    def display(self) : 
        self.screen.blit(pygame.transform.scale(self.chat_sprite["background"],(self.width_screen*.450, self.height_screen*.450)), 
                             (self.width_screen*1/80, self.height_screen*0.01))
        self.title.draw(self.screen)
        self.input.draw(self.screen)
        