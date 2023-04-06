# Write a function to write in a file
import pygame
import os


class Sprites:
    def __init__(self) -> dict:
        self.sprites = dict()
        self.init_sprites()

    def init_sprites(self):
        for name_sprite in os.listdir('Sprites/'):
            if os.path.isfile(os.path.join('Sprites/', name_sprite)):
                self.sprites[name_sprite.split('.')[0]] = {'path': 'Sprites/' + name_sprite,
                                                           'sprite_ori': pygame.image.load('Sprites/' + name_sprite).convert_alpha(),
                                                           'sprite_display': pygame.image.load('Sprites/' + name_sprite).convert_alpha()}

    def update_size_sprites(self, key, height, width):
        if self.sprites[key]['sprite_display'].get_size()[0] != int(height) \
                and self.sprites[key]['sprite_display'].get_size()[1] != int(width):
            self.sprites[key]['sprite_display'] = pygame.transform.scale(
                self.sprites[key]['sprite_ori'], (height, width))

    def get_sprites(self):
        return self.sprites
