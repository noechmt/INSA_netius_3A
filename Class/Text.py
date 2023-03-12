import pygame


class Text():
    def __init__(self, left, top, width, height, text, font, color_text=(0, 0, 0), color_hover=(136, 136, 136)):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.text = text
        self.color_text = color_text
        self.color_hover = color_hover
        self.font = font
        self.darken = False

    def draw(self, screen):
        text = self.font.render(self.text, 1, self.color_text)
        screen.blit(text, (self.left + (self.width/2 - text.get_width()/2),
                           self.top + ((self.height/2 - text.get_height()/2))))

    def is_hovered(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.left and pos[0] < self.left + self.width:
            if pos[1] > self.top and pos[1] < self.top + self.height:
                return True
        return False

    def handle_hover_text(self, pos, screen):
        # Darken the button when hovered
        # Darken the button if mouse is hover and the button is not darken
        if self.is_hovered(pos) and not self.darken:
            self.darken = True
            text = self.font.render(self.text, 1, self.color_hover)
            screen.blit(text, (self.left + (self.width/2 - text.get_width()/2),
                               self.top + ((self.height/2 - text.get_height()/2))))
        # Clear the button if the button not hovered and the button is darken
        if not self.is_hovered(pos) and self.darken:
            self.darken = False
            # Find a better way
            self.draw(screen)
