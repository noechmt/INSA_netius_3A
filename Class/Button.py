import pygame


class Button():
    def __init__(self, left, top, width, height, image=None, color=None, text=''):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.image = image
        self.color = color
        self.text = text
        self.darken = False
        self.house = False

    def draw(self, screen):
        if self.image != None:
            screen.blit(pygame.transform.scale(
                        self.image, (self.width, self.height)), (self.left, self.top))

        if self.color != None:
            pygame.draw.rect(screen, self.color, (self.left, self.top,
                                                  self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.Font(
                "GUI/Fonts/Title Screen/Berry Rotunda.ttf", 20)
            text = font.render(self.text, 1, (0, 0, 0))
            screen.blit(text, (self.left + (self.width/2 - text.get_width()/2),
                        self.top + ((self.height/2 - text.get_height()/2))))
        if self.darken:
            darken_percent = .075
            dark = pygame.Surface(
                self.get_size()).convert_alpha()
            dark.fill((0, 0, 0, darken_percent*255))
            screen.blit(dark, self.get_pos())

    def change_image(self, image):
        self.image = image

    def is_hovered(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.left and pos[0] < self.left + self.width:
            if pos[1] > self.top and pos[1] < self.top + self.height:
                return True
        return False

    def get_size(self):
        return (self.width, self.height)

    def get_pos(self):
        return (self.left, self.top)

    def get_hover(self):
        return self.hover

    def set_hover(self, hover):
        self.hover = hover

    def handle_hover_button(self, pos, screen):
        # Darken the button when hovered
        # Darken the button if mouse is hover and the button is not darken
        if self.is_hovered(pos) and not self.darken:
            self.darken = True
            darken_percent = .075
            dark = pygame.Surface(
                self.get_size()).convert_alpha()
            dark.fill((0, 0, 0, darken_percent*255))
            screen.blit(dark, self.get_pos())
        # Clear the button if the button not hovered and the button is darken
        if not self.is_hovered(pos) and self.darken:
            self.darken = False
            self.draw(screen)

    def get_text(self):
        return self.text
