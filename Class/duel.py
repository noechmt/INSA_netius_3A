import pygame
from Class.Text import Text
import random as rd


class Duel: 

    def __init__(self, screen) :
        self.screen = screen
        self.width_screen, self.height_screen = self.screen.get_size()

        self.duel_sprite = {
            "background": pygame.image.load("game_screen/game_screen_sprites/chat_background.jpg").convert_alpha(),
            "stop" : pygame.image.load("game_screen/game_screen_sprites/paneling_paused.png").convert_alpha(),
            "continue" : pygame.image.load("game_screen/game_screen_sprites/paneling_up.png").convert_alpha()
        }

        self.text = {

            "title" : None,
            "myscore" : None,
            "enemyscore" : None

        }


        
        self.player_name = ""

        self.init_duel()

        self.init_text()

    def init_text(self) : 

        (width_menu, height_menu) = (self.width_screen/6, self.height_screen / 5)
        (left_menu, top_menu) = (self.width_screen, 2 * self.height_screen / 5)
        (width_text_name, height_text_name) = (width_menu, height_menu / 3)
        (left_text, top_text) = (left_menu*.250, top_menu*0.650)
        text_font = pygame.font.Font(
            "GUI/Fonts/Title Screen/Berry Rotunda.ttf", 40)
        self.text["title"] = Text(left_text, top_text,
                        width_text_name, height_text_name, "DUEL !", text_font)
        
        
        (width_text_name, height_text_name) = (width_menu, height_menu / 3)
        (left_text, top_text) = (left_menu*.320, top_menu*1.1)
        self.text["myscore"] = Text(left_text, top_text,
                            width_text_name, height_text_name, str(self.my_score), text_font)
        

        (width_text_name, height_text_name) = (width_menu, height_menu / 3)
        (left_text, top_text) = (left_menu*.490, top_menu*1.1)
        self.text["enemyscore"] = Text(left_text, top_text,
                            width_text_name, height_text_name, str(self.enemy_score), text_font)

        
    
    def init_duel(self) : 

        #other player name
        self.enemy_name = ""

        #game score
        self.my_score = 0
        self.enemy_score = 0
        
        #determine win or loss
        self.won = False
        self.lost = False
        self.draw = False

        #handle bet system
        self.my_bet_stopped = False
        self.enemy_bet_stopped =False

        #handle request for duels
        self.duel_request = 0

        #handle game rounds and network sync
        self.duel_accepted = 0 # 1 accepted, 2 refused, 0 pending
        self.game_round = 0
        self.enemy_game_round = 0
        


    def display(self) : 
        self.update_score()
        self.screen.blit(pygame.transform.scale(self.duel_sprite["background"], (self.width_screen*.450, self.height_screen*.450)),
                         (self.width_screen*.25, self.height_screen*.25))
        
        self.text["title"].draw(self.screen)
        self.text["myscore"].draw(self.screen)
        self.text["enemyscore"].draw(self.screen)

   
    
    def update_score(self) :
        self.text["myscore"].text = str(self.my_score)
        self.text["enemyscore"].text = str(self.enemy_score)
        
    def continue_bet(self) :
        if self.game_round == self.enemy_game_round :
            if not self.my_bet_stopped : self.my_score += rd.randint(1, 13)
            if self.my_score > 21 : self.stop_bet()

            self.game_round += 1

    def continue_bet_enemy_proto(self) :
        if not self.enemy_bet_stopped : self.enemy_score += rd.randint(1, 13)
        if self.enemy_score > 21 : self.stop_bet_enemy_proto()

    def stop_bet(self) : 
        if self.game_round == self.enemy_game_round :
            self.my_bet_stopped = True
        


    def stop_bet_enemy_proto(self) :
        self.enemy_bet_stopped = True

    def handle_winner(self) :
        
        # print(self.my_bet_stopped, self.enemy_bet_stopped)
        if self.my_bet_stopped and self.enemy_bet_stopped : 

            if (self.my_score > 21 and self.enemy_score > 21) or (self.my_score == self.enemy_score):
                self.draw = True
            
            elif self.my_score > 21 and self.enemy_score <= 21 : self.lost = True
            elif self.enemy_score > 21 and self.my_score <= 21 : self.lost = True
            elif self.my_score > self.enemy_score : self.won = True
            else : self.lost = True

            return True
        
        return False

        # print("won : ", self.won, "|lost : ", self.lost, "|draw : ", self.draw)


    def ask_for_duel(self) : 
        pass

    def accept_duel(self) :
        pass 

    def decline_duel(self) :
        pass

    def receive_enemy_info(self) :
        pass




