import Class.Cell as Cell
import Class.Encoder as encode
import random as rd
import pygame

sound_effect = {"extinguish": pygame.mixer.Sound("audio/water_bucket.wav"), "cooling": pygame.mixer.Sound("audio/cooling_fizz.wav"),
                "break": pygame.mixer.Sound("audio/break.wav")}

sound_effect["break"].set_volume(0.1)
sound_effect["cooling"].set_volume(0.1)
sound_effect["extinguish"].set_volume(0.1)


class RiskEvent():

    riskTreshold = 200

    def __init__(self, eType, building):
        self.riskCounter = 0
        self.happened = False
        self.type = eType
        self.tmpbool = True
        self.fireCounter = 0
        self.fire_sprites = [{"sprite": pygame.image.load("risks_sprites/house_fire/fire_" + str(k) + ".png").convert_alpha(),
                              "path": "risks_sprites/house_fire/fire_" + str(k) + ".png"} for k in range(0, 10)]
        self.building = building

    def riskIncrease(self):
        if self.building.destroyed:
            return
        if isinstance(self.building, Cell.House) and (self.building.migrant in self.building.map.walkers or self.building.migrant in self.building.map.migrantQueue):
            return
        if self.type == "fire":
            self.riskCounter += rd.randint(0, 3)
        else:
            self.riskCounter += rd.randint(0, 1)

        if self.riskCounter >= self.riskTreshold:
            if self.building.map.players_online > 1 and self.building.owner == self.building.map.name_user: 
                encode.risk(self.building.map.name_user, self.type, self.building, self.fireCounter)
            self.happened = True
            self.building.type = "ruin"
            if self.type == "fire" or self.type == "collapse":
                # Au cas où il faut changer de sprite pour le collapse
                self.building.sprite = pygame.image.load(
                    "risks_sprites/house_fire/fire_8.png").convert_alpha()
                self.building.path_sprite = "risks_sprites/house_fire/fire_8.png"
            if isinstance(self.building, Cell.House):
                self.building.nb_occupants, self.building.unemployedCount = 0, 0
            elif isinstance(self.building, Cell.Prefecture):
                if self.building.labor_advisor in self.building.map.walkers:
                    self.building.labor_advisor.currentCell.display()
                    self.building.map.walkers.remove(
                        self.building.labor_advisor)
                else:
                    self.building.prefect.currentCell.display()
                    if self.building.prefect in self.building.map.walkers:
                        self.building.map.walkers.remove(self.building.prefect)
            elif isinstance(self.building, Cell.EngineerPost):
                if self.building.labor_advisor in self.building.map.walkers:
                    self.building.labor_advisor.currentCell.display()
                    self.building.map.walkers.remove(
                        self.building.labor_advisor)
                else:
                    self.building.engineer.currentCell.display()
                    if self.building.engineer in self.building.map.walkers:
                        self.building.map.walkers.remove(
                            self.building.engineer)

    def burn(self):
        if not self.happened or self.building.destroyed:
            return
        if self.fireCounter >= 500:
            if self.building.map.players_online > 1 and self.building.owner == self.building.map.name_user: 
                encode.risk(self.building.map.name_user, "burnt", self.building, self.fireCounter)
            # self.building.screen.blit(pygame.transform.scale(pygame.image.load("game_screen/game_screen_sprites/dirt_0.png"), (self.building.width, self.building.height)), (self.building.left, self.building.top))
            if self.building.sprite != pygame.image.load("risks_sprites/house_fire/fire_9.png").convert_alpha():
                # self.building.screen.blit(pygame.transform.scale(self.fire_sprites[9], (self.building.width, self.building.height)), (self.building.left, self.building.top))
                self.building.sprite = pygame.image.load(
                    "risks_sprites/house_fire/fire_9.png").convert_alpha()
                self.building.path_sprite = "risks_sprites/house_fire/fire_9.png"
                self.building.update_sprite_size()
                self.building.display()
            self.fireCounter = 0
            self.building.destroyed = True
            sound_effect["cooling"].set_volume(0.2)
            sound_effect["cooling"].play()

        else:
            self.building.sprite = self.fire_sprites[self.fireCounter %
                                                     8]["sprite"]
            self.building.path_sprite = self.fire_sprites[self.fireCounter %
                                                          8]["path"]
            self.building.update_sprite_size()
            self.building.display()
            # self.building.screen.blit(pygame.transform.scale(self.fire_sprites[self.fireCounter%8], (self.building.width, self.building.height)), (self.building.left, self.building.top))
            if self.building.y <= 38 and self.building.map.array[self.building.x][self.building.y + 1].type != "ruin":
                self.building.map.array[self.building.x][self.building.y + 1].display()
            self.fireCounter += 1
            if self.tmpbool:
                self.tmpbool = False

        # if self.fireCounter >= 400 :
        #     arr = self.building.check_cell_around(Cell.Building)
        #     for i in arr :
        #         i.risk.happened = True
        #         i.type = "ruin"
        #         i.sprite = pygame.image.load("risks_sprites/house_fire/fire_9.png")

    def collapse(self):
        if not self.happened or self.building.destroyed:
            return
        self.building.destroyed = True
        # self.building.sprite = pygame.image.load("game_screen/game_screen_sprites/dirt_0.png"), (self.building.width, self.building.height)), (self.building.left, self.building.top))
        self.building.sprite = self.fire_sprites[8]["sprite"]
        self.building.path_sprite = self.fire_sprites[8]["path"]
        self.building.update_sprite_size()
        self.building.display()
        sound_effect["break"].play()
        # self.building.map.buildings.remove(self.building)

    def resetEvent(self):
        self.riskCounter = 0

    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop("fire_sprites")
        return state

    def __setstate__(self, state):
        state["fire_sprites"] = [{"sprite": pygame.image.load("risks_sprites/house_fire/fire_" + str(k) + ".png").convert_alpha(),
                                  "path": "risks_sprites/house_fire/fire_" + str(k) + ".png"} for k in range(0, 10)]
        self.__dict__.update(state)
