import pygame
import sys

speed = 1


class Walker(pygame.sprite.Sprite) : 
    def __init__(self, pos_x, pos_y) :
        super().__init__()
        self.sprites = [pygame.image.load("walker_sprites/LA_sprites/top_animation/Citizen01_0000" + str(k) + ".png")  if k < 10  
        else pygame.image.load("walker_sprites/LA_sprites/top_animation/Citizen01_000"+ str(k) + ".png") for k in range(1,90,8) ]
        self.currentSprite = 0
        self.image = self.sprites[self.currentSprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]        

    def walk(self, x, y) :
        self.currentSprite += speed
        if int(self.currentSprite) >= len(self.sprites) : 
            self.currentSprite = 0
        self.image = pygame.transform.scale(self.sprites[int(self.currentSprite)], (x, y))

            



# General setup
pygame.init()
clock = pygame.time.Clock()


# Game Screen
screen_width = 400
screen_height = 400
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Sprite Animation")

# Creating the sprites and groups
moving_sprites = pygame.sprite.Group()
aWalker = Walker(200, 200)
moving_sprites.add(aWalker)


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

       
	aWalker.walk()

	# Drawing
	screen.fill((0,0,0))
	moving_sprites.draw(screen)
	moving_sprites.update(0.25)
	pygame.display.flip()
	clock.tick(60)