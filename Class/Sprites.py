# Write a function to write in a file
import pygame

class Sprites:
    def __init__(self) -> dict:
        self.sprites = dict()
        self.init_sprites()
    
    def init_sprites(self):
        self.sprites['dirt_0'] = {'path' : 'game_screen/game_screen_sprites/dirt_0.png',
                                  'sprite_ori' : pygame.image.load("game_screen/game_screen_sprites/dirt_0.png").convert_alpha(),
                                  'sprite_display' : pygame.image.load("game_screen/game_screen_sprites/dirt_0.png").convert_alpha()}
    
    def update_size_sprites(self, height, width):
        self.sprites['dirt_0']['sprite_display'] = pygame.transform.scale(
                self.sprites['dirt_0']['sprite_ori'], (height, width))


    def get_sprites(self):
        return self.sprites