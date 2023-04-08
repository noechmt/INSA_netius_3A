import pygame
from Class.Text import Text


class Duel: 

    def __init__(self, screen) :
        self.screen = screen
        self.width_screen, self.height_screen = self.screen.get_size()

        self.duel_sprite = {
            "background": pygame.image.load("game_screen/game_screen_sprites/chat_background.jpg").convert_alpha(),
            "stop" : pygame.image.load("game_screen/game_screen_sprites/paneling_paused.png").convert_alpha(),
            "continue" : pygame.image.load("game_screen/game_screen_sprites/paneling_up.png") 
        }

        self.text = {

            "title" : None

        }

        self.init_text()

        self.ON = False

        self.duel_accepted = True
        self.duel_refused = False
        self.response = False

    def init_text(self) : 

        (width_menu, height_menu) = (self.width_screen/6, self.height_screen / 5)
        (left_menu, top_menu) = (self.width_screen, 2 * self.height_screen / 5)
        (width_text_name, height_text_name) = (width_menu, height_menu / 3)
        (left_text, top_text) = (left_menu*.001, top_menu*0.005)
        text_font = pygame.font.Font(
            "GUI/Fonts/Title Screen/Berry Rotunda.ttf", 40)
        self.text["waiting"] = Text(left_text, top_text,
                        width_text_name, height_text_name, "", text_font)
            


    def display(self) : 
        self.screen.blit(pygame.transform.scale(self.duel_sprite["background"], (self.width_screen*.450, self.height_screen*.450)),
                         (self.width_screen*.25, self.height_screen*.25))

   
        
        



    






