import pygame
from Class.Text import Text
from Class.Input_box import InputBox


class Chat:
    def __init__(self, screen):

        # useless dict for now, may add another sprite someday (probably not)
        self.chat_sprite = {
            "background": pygame.image.load("game_screen/game_screen_sprites/chat_background.jpg").convert_alpha()
        }

        self.screen = screen
        self.width_screen, self.height_screen = self.screen.get_size()
        self.message_history = ['']*100
        self.history_index = 0
        self.init_history()
        self.init_title()
        self.init_input()

    def init_title(self):
        (width_menu, height_menu) = (self.width_screen/6, self.height_screen / 5)
        (left_menu, top_menu) = (self.width_screen, 2 * self.height_screen / 5)
        (width_text_name, height_text_name) = (width_menu, height_menu / 3)
        (left_text, top_text) = (left_menu*0.005, top_menu*0.001)
        text_font = pygame.font.Font(
            "GUI/Fonts/Title Screen/Berry Rotunda.ttf", 20)
        self.title = Text(left_text, top_text,
                          width_text_name, height_text_name, "IN-GAME chatroom", text_font)

    def init_input(self):
        (width_menu, height_menu) = (self.width_screen/6, self.height_screen / 5)
        (left_menu, top_menu) = (self.width_screen, 2 * self.height_screen / 5)
        (width_input_name, height_input_name) = (
            width_menu*2.3, height_menu / 6)
        (left_input_name, top_input_name) = (
            left_menu*0.025, top_menu)
        input_name_font = pygame.font.Font(
            "GUI/Fonts/Title Screen/Berry Rotunda.ttf", 15)
        self.input = InputBox(left_input_name, top_input_name, width_input_name,
                              height_input_name, input_name_font, 35, "", (255, 255, 255))

    def display(self):
        # print("darken?")
        self.screen.blit(pygame.transform.scale(self.chat_sprite["background"], (self.width_screen*.450, self.height_screen*.450)),
                         (self.width_screen*1/80, self.height_screen*0.01))
        self.title.draw(self.screen)
        self.input.draw_60(self.screen)
        for i in range(self.history_index, self.history_index + 5):
            self.message_history[i].draw(self.screen)

    def history_append(self, msg):
        for i in reversed(range(0, len(self.message_history)-1)):
            self.message_history[i+1].text = self.message_history[i].text
        self.message_history[0].text = msg

    def init_history(self):
        text_font = pygame.font.Font(
            "GUI/Fonts/Title Screen/Berry Rotunda.ttf", 20)
        (width_menu, height_menu) = (
            self.width_screen/6, self.height_screen * 0.001)
        (left_menu, top_menu) = (self.width_screen, 2 * self.height_screen / 6)
        (width_text_name, height_text_name) = (width_menu, height_menu * 0.001)
        # (left_text, top_text) = (left_menu*0.001, top_menu*0.001)
        for i in range(len(self.message_history)):
            self.message_history[i] = self.title = Text(left_menu*0.15, top_menu*(1 - (i % 5)*0.1),
                                                        width_text_name, height_text_name, self.message_history[i], text_font)

    def handle_history_scroll(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 5 and self.history_index > 0:
                self.history_index -= 5

            if event.button == 4 and self.history_index < 95:

                self.history_index += 5

        
            

