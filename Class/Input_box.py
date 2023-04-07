import pygame


class InputBox:
    def __init__(self, left, top, width, height, font, max_char = 50, text='',
                 color_inactive=(0, 0, 0), color_active=(240, 240, 240)):
        self.rect = pygame.Rect(left, top, width, height)
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.darken_percent = .3
        self.darken = False
        self.font = font
        self.max_char = max_char
        self.text = text
        self.color_inactive = color_inactive
        self.color_active = color_active
        self.color = color_inactive
        self.active = False
        self.message_to_send = ""

    def draw(self, screen):
        if (not self.darken):
            dark = pygame.Surface(
                self.get_size()).convert_alpha()
            dark.fill((0, 0, 0, self.darken_percent*255))
            screen.blit(dark, self.get_pos())
            # self.darken = True
        text = self.font.render(self.text, 1, self.color)
        screen.blit(text, (self.left + (self.left / 40),
                           self.top + ((self.height/2 - text.get_height()/2))))

    def handle_event(self, event, screen):
        # print(pygame.mouse.get_pressed(num_buttons=3))
        # if pygame.mouse.get_pressed(num_buttons=3) == (True, False, False):
        if event.type == pygame.MOUSEBUTTONDOWN :
            print("alo?")
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                print("Input mouse down")
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN :
            if self.active:
                # print("salut0")
                if event.key == pygame.K_RETURN:
                    # print("salut1")
                    self.message_to_send = self.text
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    # print("salut2")
                    self.text = self.text[:-1]
                elif len(self.text) <= self.max_char:
                    # print("salut4")
                    self.text += event.unicode
                
            # print("salut5")
            self.darken = False
            return True
        self.draw(screen)

    def is_hovered(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.left and pos[0] < self.left + self.width:
            if pos[1] > self.top and pos[1] < self.top + self.height:
                return True
        return False

    def get_pos(self):
        return (self.left, self.top)

    def get_size(self):
        return (self.width, self.height)

    def get_text(self):
        return self.text
