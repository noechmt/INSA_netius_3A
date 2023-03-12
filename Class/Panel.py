import pygame
from Class.Button import Button


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


class Panel():
    def __init__(self, screen):
        self.screen = screen
        self.width_screen, self.height_screen = self.screen.get_size()
        self.init_sprites()
        self.init_buttons()
        self.window_current = self.window_none
        self.display()
        pass

    def init_sprites(self):
        self.figure_1 = pygame.image.load(
            "game_screen/game_screen_sprites/figure_2.png").convert_alpha()
        self.background = pygame.image.load(
            "game_screen/game_screen_sprites/panel_background.png").convert_alpha()
        self.overlays = pygame.image.load(
            "game_screen/game_screen_sprites/paneling_overlays.png").convert_alpha()
        self.window_none = pygame.image.load(
            "game_screen/game_screen_sprites/panel_window_none.png").convert_alpha()
        self.window_house = pygame.image.load(
            "game_screen/game_screen_sprites/panel_window_home.png").convert_alpha()
        self.window_road = pygame.image.load(
            "game_screen/game_screen_sprites/panel_window_road.png").convert_alpha()
        self.window_prefecture = pygame.image.load(
            "game_screen/game_screen_sprites/panel_window_prefecture.png").convert_alpha()
        self.window_engineerpost = pygame.image.load(
            "game_screen/game_screen_sprites/panel_window_engineerpost.png").convert_alpha()
        self.window_well = pygame.image.load(
            "game_screen/game_screen_sprites/panel_window_well.png").convert_alpha()
        self.window_shovel = pygame.image.load(
            "game_screen/game_screen_sprites/panel_window_shovel.png").convert_alpha()
        self.grid_button_sprite = pygame.image.load(
            "game_screen/game_screen_sprites/paneling_grid_button.png").convert_alpha()
        self.fire_button_sprite = pygame.image.load(
            "game_screen/game_screen_sprites/paneling_fire.png").convert_alpha()
        self.collapse_button_sprite = pygame.image.load(
            "game_screen/game_screen_sprites/paneling_collapse.png").convert_alpha()
        self.home_button_sprite = pygame.image.load(
            "game_screen/game_screen_sprites/paneling_home_button.png").convert_alpha()
        self.shovel_button_sprite = pygame.image.load(
            "game_screen/game_screen_sprites/paneling_shovel_button.png").convert_alpha()
        self.road_button_sprite = pygame.image.load(
            "game_screen/game_screen_sprites/paneling_road_button.png").convert_alpha()
        self.bottom = pygame.image.load(
            "game_screen/game_screen_sprites/paneling_bot.png").convert_alpha()
        self.prefecture_button_sprite = pygame.image.load(
            "game_screen/game_screen_sprites/paneling_prefecture_button.png").convert_alpha()
        self.engineerpost_button_sprite = pygame.image.load(
            "game_screen/game_screen_sprites/paneling_engineerpost_button.png").convert_alpha()
        self.well_button_sprite = pygame.image.load(
            "game_screen/game_screen_sprites/paneling_well_button.png").convert_alpha()
        self.button_up_sprite = pygame.image.load(
            "game_screen/game_screen_sprites/paneling_up.png").convert_alpha()
        self.button_down_sprite = pygame.image.load(
            "game_screen/game_screen_sprites/paneling_down.png").convert_alpha()
        self.button_played_sprite = pygame.image.load(
            "game_screen/game_screen_sprites/paneling_played.png").convert_alpha()
        self.button_paused_sprite = pygame.image.load(
            "game_screen/game_screen_sprites/paneling_paused.png").convert_alpha()
        self.button_save_sprite = pygame.image.load(
            "game_screen/game_screen_sprites/paneling_save.png").convert_alpha()
        self.button_exit_sprite = pygame.image.load(
            "game_screen/game_screen_sprites/paneling_exit.png").convert_alpha()

    def init_buttons(self):
        self.grid_button = Button(177*self.width_screen/192, 0.345*self.height_screen,
                                  self.width_screen/48, self.height_screen / 40, self.grid_button_sprite)
        self.fire_button = Button(182*self.width_screen/192, 0.345*self.height_screen,
                                  self.width_screen/48, self.height_screen / 40, self.fire_button_sprite)
        self.collapse_button = Button(187*self.width_screen/192, 0.345*self.height_screen,
                                      self.width_screen/48, self.height_screen / 40, self.collapse_button_sprite)
        self.house_button = Button(177*self.width_screen/192, 0.25*self.height_screen,
                                   self.width_screen/48, self.height_screen/40, self.home_button_sprite)
        self.shovel_button = Button(182*self.width_screen/192, 0.25*self.height_screen,
                                    self.width_screen/48, self.height_screen/40, self.shovel_button_sprite)
        self.road_button = Button(187*self.width_screen/192, 0.25*self.height_screen,
                                  self.width_screen/48, self.height_screen/40, self.road_button_sprite)
        self.prefecture_button = Button(177*self.width_screen/192, 0.25*self.height_screen+3*self.height_screen/80,
                                        self.width_screen/48, self.height_screen/40, self.prefecture_button_sprite)
        self.engineerpost_button = Button(182*self.width_screen/192, 0.25*self.height_screen+3*self.height_screen/80,
                                          self.width_screen/48, self.height_screen/40, self.engineerpost_button_sprite)
        self.well_button = Button(187*self.width_screen/192, 0.25*self.height_screen+3*self.height_screen/80,
                                  self.width_screen/48, self.height_screen/40, self.well_button_sprite)
        self.up_button = Button(
            177*self.width_screen/192, 0.25*self.height_screen+12*self.height_screen/80, self.width_screen/48, self.height_screen/40, self.button_up_sprite)
        self.down_button = Button(
            177*self.width_screen/192 + 1.2*self.width_screen/48, 0.25*self.height_screen+12*self.height_screen/80, self.width_screen/48, self.height_screen/40, self.button_down_sprite)
        self.pause_button = Button(177*self.width_screen/192 + 0.55*self.width_screen/48, 0.25*self.height_screen +
                                   15*self.height_screen/80, self.width_screen/48, self.height_screen/40, self.button_played_sprite)
        self.save_button = Button(self.width_screen - self.width_screen / 13, 0.25*self.height_screen +
                                  34.75*self.height_screen/80, 1.25*self.width_screen/48, 1.5*self.height_screen/40, self.button_save_sprite)
        self.exit_button = Button(self.width_screen - self.width_screen / 13 + self.width_screen / 48, 0.25*self.height_screen +
                                  41*self.height_screen/80, 1.5*self.width_screen/48, 1.75*self.height_screen/40, self.button_exit_sprite)

    def display(self):
        for i in range(2):
            for j in range(9):
                self.screen.blit(pygame.transform.scale(self.background, (self.width_screen/24,
                                                                          self.height_screen/10)), ((((i+22)/24)*self.width_screen), (j/10)*self.height_screen))
        draw_rect_alpha(self.screen, (50, 50, 50, 60), (self.width_screen *
                                                        (11/12), 0, self.width_screen/12, self.height_screen*9/10))
        # self.screen.blit(pygame.transform.scale(self.overlays, (self.width_screen/18,
        #                                                       self.height_screen/36)), (11*self.width_screen/12+5, self.height_screen/32+2))

        self.screen.blit(pygame.transform.scale(
            self.figure_1, (81, 91)), (180*self.width_screen/192, self.height_screen/16))

        draw_rect_alpha(self.screen, (255, 255, 255, 127), (177*self.width_screen/192-2,
                        0.25*self.height_screen-2, (self.width_screen)/48+4, (self.height_screen)/40+4))
        draw_rect_alpha(self.screen, (255, 255, 255, 127), (182*self.width_screen/192-2,
                        0.25*self.height_screen-2, (self.width_screen)/48+4, (self.height_screen)/40+4))
        draw_rect_alpha(self.screen, (255, 255, 255, 127), (187*self.width_screen/192-2,
                        0.25*self.height_screen-2, (self.width_screen)/48+4, (self.height_screen)/40+4))
        draw_rect_alpha(self.screen, (255, 255, 255, 127), (177*self.width_screen/192-2,
                                                            0.25*self.height_screen+3*self.height_screen/80-1, (self.width_screen)/48+4, (self.height_screen)/40+3))
        draw_rect_alpha(self.screen, (255, 255, 255, 127), (182*self.width_screen/192-2,
                                                            0.25*self.height_screen+3*self.height_screen/80-2, (self.width_screen)/48+4, (self.height_screen)/40+4))
        draw_rect_alpha(self.screen, (255, 255, 255, 127), (187*self.width_screen/192-1,
                                                            0.25*self.height_screen+3*self.height_screen/80-2, (self.width_screen)/48+4, (self.height_screen)/40+4))
        draw_rect_alpha(self.screen, (255, 255, 255, 127), (177*self.width_screen/192-1.5, 0.25 *
                        self.height_screen+12*self.height_screen/80-1.5, self.width_screen/48+3, self.height_screen/40+3))
        draw_rect_alpha(self.screen, (255, 255, 255, 127), (177*self.width_screen/192-1.5 + 1.2*self.width_screen/48,
                        0.25*self.height_screen+12*self.height_screen/80-1.5, self.width_screen/48+3, self.height_screen/40+3))
        draw_rect_alpha(self.screen, (255, 255, 255, 127), (177*self.width_screen/192 + 0.55*self.width_screen/48-1.5, 0.25*self.height_screen +
                                                            15*self.height_screen/80-1.5, self.width_screen/48+3, self.height_screen/40+3))
        draw_rect_alpha(self.screen, (255, 255, 255, 127), (177*self.width_screen/192-1.5, 0.345*self.height_screen-1.5,
                                                            self.width_screen/48+4, self.height_screen/40+3))
        draw_rect_alpha(self.screen, (255, 255, 255, 127), (182*self.width_screen/192-1.5, 0.345*self.height_screen-1.5,
                                                            self.width_screen/48+4, self.height_screen/40+3))
        draw_rect_alpha(self.screen, (255, 255, 255, 127), (187*self.width_screen/192-1.5, 0.345*self.height_screen-1.5,
                                                            self.width_screen/48+4, self.height_screen/40+3))

        self.screen.blit(pygame.transform.scale(self.window_current, (self.width_screen /
                                                                      12-10, self.height_screen/17)), (11*self.width_screen/12+5, 0.18*self.height_screen))

        self.grid_button.draw(self.screen)

        self.fire_button.draw(self.screen)

        self.collapse_button.draw(self.screen)

        self.house_button.draw(self.screen)

        self.shovel_button.draw(self.screen)

        self.road_button.draw(self.screen)

        self.prefecture_button.draw(self.screen)

        self.engineerpost_button.draw(self.screen)

        self.well_button.draw(self.screen)

        draw_rect_alpha(self.screen, (25, 25, 25, 127), (self.width_screen*(11/12)+2,
                        self.height_screen*(8/17), self.width_screen/12-4, 3*self.height_screen/7-2))

        self.screen.blit(pygame.transform.scale(self.bottom, (self.width_screen/12,
                                                              self.height_screen/10)), (((11/12)*self.width_screen), (0.9*self.height_screen)))

        self.up_button.draw(self.screen)
        self.down_button.draw(self.screen)
        self.pause_button.draw(self.screen)
        self.save_button.draw(self.screen)
        self.exit_button.draw(self.screen)

    def set_window(self, choice):
        if choice == "road":
            self.window_current = self.window_road
        if choice == "house":
            self.window_current = self.window_house
        if choice == "prefecture":
            self.window_current = self.window_prefecture
        if choice == "engineer post":
            self.window_current = self.window_engineerpost
        if choice == "well":
            self.window_current = self.window_well
        if choice == "shovel":
            self.window_current = self.window_shovel
        if choice == "none":
            self.window_current = self.window_none
        self.screen.blit(pygame.transform.scale(self.window_current, (self.width_screen /
                                                                      12-10, self.height_screen/17)), (11*self.width_screen/12+5, 0.18*self.height_screen))

    def set_paused_button(self):
        self.pause_button.change_image(self.button_paused_sprite)

    def set_played_button(self):
        self.pause_button.change_image(self.button_played_sprite)

    def get_grid_button(self):
        return self.grid_button

    def get_fire_button(self):
        return self.fire_button

    def get_collapse_button(self):
        return self.collapse_button

    def get_home_button(self):
        return self.house_button

    def get_shovel_button(self):
        return self.shovel_button

    def get_road_button(self):
        return self.road_button

    def get_prefecture_button(self):
        return self.prefecture_button

    def get_engineerpost_button(self):
        return self.engineerpost_button

    def get_well_button(self):
        return self.well_button

    def get_up_button(self):
        return self.up_button

    def get_down_button(self):
        return self.down_button

    def get_pause_button(self):
        return self.pause_button

    def get_save_button(self):
        return self.save_button

    def get_exit_button(self):
        return self.exit_button
