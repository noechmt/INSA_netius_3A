import Class.Cell as Cell
import random
import pygame

import networkx as nx


def rm_dup_list(x):
    return list(dict.fromkeys(x))


SCREEN = None

sound_effect = {"extinguish": pygame.mixer.Sound("audio/water_bucket.wav"), "cooling": pygame.mixer.Sound("audio/cooling_fizz.wav"),
                "break": pygame.mixer.Sound("audio/break.wav")}

sound_effect["break"].set_volume(0.1)
sound_effect["cooling"].set_volume(0.1)
sound_effect["extinguish"].set_volume(0.1)


def set_SCREEN_walker(screen):
    global SCREEN
    SCREEN = screen


class Walker():

    def __init__(self, job, building, state):
        self.job = job  # le métier (migrant, worker, etc) : string
        self.building = building  # string (prefecture, engineer post, house)
        self.currentCell = building  # La cellule de départ de l'entity : Cell
        self.previousCell = None
        self.inBuilding = state
        self.path = []
        self.ttl = 50
        self.wait = 0
        print("Walker spawn")

        self.walker_sprites = {}
        self.alive = False
        self.isWandering = False
        self.currentSprite = 0

    def display(self):
        if not self.inBuilding and self.building.map.get_overlay() not in ("fire", "collapse"):
            if self.previousCell.x < self.currentCell.x:
                SCREEN.blit(pygame.transform.scale(self.walker_sprites["right"][self.currentSprite % 2], (
                    self.currentCell.width, self.currentCell.height)), (self.currentCell.left, self.currentCell.top))
            elif self.previousCell.x > self.currentCell.x:
                SCREEN.blit(pygame.transform.scale(self.walker_sprites["left"][self.currentSprite % 2], (
                    self.currentCell.width, self.currentCell.height)), (self.currentCell.left, self.currentCell.top))
            elif self.previousCell.y < self.currentCell.y:
                SCREEN.blit(pygame.transform.scale(self.walker_sprites["bot"][self.currentSprite % 2], (
                    self.currentCell.width, self.currentCell.height)), (self.currentCell.left, self.currentCell.top))
            elif self.previousCell.y > self.currentCell.y:
                SCREEN.blit(pygame.transform.scale(self.walker_sprites["top"][self.currentSprite % 2], (
                    self.currentCell.width, self.currentCell.height)), (self.currentCell.left, self.currentCell.top))

            self.currentSprite += 1
        # elif self.inBuilding == True :
        #     self.currentCell.display()

    def __str__(self) -> str:
        pass

    def path_finding(self, start, end):
        print("Path finding to reach", end, "from", start)
        try:
            self.path = nx.dijkstra_path(
                self.building.map.path_graph, start, end)
        except:
            self.path = []
        self.isWandering = False

    # si la position est différente des coordonnées de la cellule, on change currentCell
    def cell_assignement(self, new_cell):
        # if (self.position_x != self.currentCell.x or self.position_y != self.currentCell.y ) :
        self.previousCell = self.currentCell
        self.currentCell = new_cell

    # if (self.building.employees == self.building.required_employees) :
    def leave_building(self):
        if self.building.type == "ruin" : return
        self.isWandering = True
        # print(self.isWandering)
        path = self.currentCell.check_cell_around(Cell.Path)
        if len(path) == 0:
            return
        self.cell_assignement(random.choice(path))
        self.inBuilding = False
        # if not isinstance(self, Prefect) and not isinstance(self, Engineer) :
        if not self.alive:
            self.building.map.walkers.append(self)
            self.alive = True

        print("Walker is leaving the building on the cell " +
              str(self.currentCell.x) + ";" + str(self.currentCell.y))

    def enter_building(self):
        # assert self.building in self.currentCell.check_cell_around(
        #     type(self.building))
        self.cell_assignement(self.building)
        self.inBuilding = True
        self.currentCell.display()
        self.previousCell.display()
        print("walker enters")

        if not isinstance(self, Prefect) and not isinstance(self, Engineer):
            self.building.map.walkers.remove(self)

    def move(self):
        path = self.currentCell.check_cell_around(Cell.Path)
        assert len(path) != 0
        if (len(path) == 1):
            self.cell_assignement(path[0])
        else:
            if isinstance(self.previousCell, Cell.Path):
                path.remove(self.previousCell)
            self.cell_assignement(random.choice(path))
        print("walker is moving on the cell " +
              str(self.currentCell.x) + ";" + str(self.currentCell.y))

    def movePathFinding(self):
        assert len(self.path) != 0
        self.cell_assignement(self.path.pop(0))

    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop("walker_sprites")
        return state

    def __setstate__(self, state):
        match state["job"]:
            case "migrant":
                state["walker_sprites"] = dict((k, pygame.image.load(
                    "walker_sprites/migrant_sprites/mg_" + k + ".png").convert_alpha()) for k in ["top", "bot", "left", "right"])
                self.__dict__.update(state)
            case "labor advisor":
                state["walker_sprites"] = dict(
                    (k, [0, 0]) for k in ["top", "bot", "left", "right"])
                for i in state["walker_sprites"]:
                    for j in range(2):
                        state["walker_sprites"][i][j] = pygame.image.load(
                            "walker_sprites/LA_sprites/LA_" + i + "_" + str(j) + ".png").convert_alpha()
                self.__dict__.update(state)
            case "prefect":
                state["walker_sprites"] = dict((k, [0, 0])
                                               for k in ["top", "bot", "left", "right"])
                self.__dict__.update(state)
                for i in self.walker_sprites:
                    for j in range(2):
                        self.walker_sprites[i][j] = pygame.image.load(
                            "walker_sprites/prefect_sprites/prefect_" + i + "_" + str(j) + ".png").convert_alpha()

            case "engineer":
                state["walker_sprites"] = dict((k, [0, 0])
                                               for k in ["top", "bot", "left", "right"])
                self.__dict__.update(state)
                for i in self.walker_sprites:
                    for j in range(2):
                        self.walker_sprites[i][j] = pygame.image.load(
                            "walker_sprites/engineer_sprites/engineer_" + i + "_" + str(j) + ".png").convert_alpha()

        self.__dict__.update(state)


class Migrant(Walker):
    def __init__(self, building):
        super().__init__("migrant", building, False)
        self.cell_assignement(self.currentCell.map.array[27][39])
        self.currentCell.map.migrantQueue.append(self)
        # building.map.walkers.append(self)
        self.walker_sprites = dict((k, pygame.image.load(
            "walker_sprites/migrant_sprites/mg_" + k + ".png").convert_alpha()) for k in ["top", "bot", "left", "right"])
        self.cart_sprites = dict((k, pygame.image.load("walker_sprites/migrant_sprites/mg_cart_" +
                                 k + ".png").convert_alpha()) for k in ["top", "bot", "left", "right"])
        # SCREEN.blit(pygame.transform.scale(self.walker_sprites["top"],
        # (self.currentCell.width, self.currentCell.height)), (self.currentCell.left, self.currentCell.top))
        self.spawnCount = 0

    def display(self):

        if self.previousCell.x < self.currentCell.x:
            if not self.inBuilding:
                SCREEN.blit(pygame.transform.scale(self.walker_sprites["right"], (
                    self.currentCell.width, self.currentCell.height)), (self.currentCell.left, self.currentCell.top))
                SCREEN.blit(pygame.transform.scale(self.cart_sprites["right"], (
                    self.currentCell.width, self.currentCell.height)), (self.previousCell.left, self.previousCell.top))
            if 0 < self.previousCell.x < 39:
                self.currentCell.map.array[self.previousCell.x -
                                           1][self.currentCell.y].display()
                self.currentCell.map.get_cell(
                    self.previousCell.x-1, self.currentCell.y).display_around()
        elif self.previousCell.x > self.currentCell.x:
            if not self.inBuilding:
                SCREEN.blit(pygame.transform.scale(self.walker_sprites["left"], (
                    self.currentCell.width, self.currentCell.height)), (self.currentCell.left, self.currentCell.top))
                SCREEN.blit(pygame.transform.scale(self.cart_sprites["left"], (
                    self.currentCell.width, self.currentCell.height)), (self.previousCell.left, self.previousCell.top))
            if 0 < self.previousCell.x < 39:
                self.currentCell.map.array[self.previousCell.x +
                                           1][self.currentCell.y].display()
                self.currentCell.map.get_cell(
                    self.previousCell.x+1, self.currentCell.y).display_around()
        elif self.previousCell.y < self.currentCell.y:
            if not self.inBuilding:
                SCREEN.blit(pygame.transform.scale(self.walker_sprites["bot"], (
                    self.currentCell.width, self.currentCell.height)), (self.currentCell.left, self.currentCell.top))
                SCREEN.blit(pygame.transform.scale(self.cart_sprites["bot"], (
                    self.currentCell.width, self.currentCell.height)), (self.previousCell.left, self.previousCell.top))
            if 0 < self.previousCell.y < 39:
                self.currentCell.map.array[self.currentCell.x][self.previousCell.y - 1].display()
                self.currentCell.map.get_cell(
                    self.currentCell.x, self.previousCell.y-1).display_around()
        elif self.previousCell.y > self.currentCell.y:
            if not self.inBuilding:
                SCREEN.blit(pygame.transform.scale(self.walker_sprites["top"], (
                    self.currentCell.width, self.currentCell.height)), (self.currentCell.left, self.currentCell.top))
                SCREEN.blit(pygame.transform.scale(self.cart_sprites["top"], (
                    self.currentCell.width, self.currentCell.height)), (self.previousCell.left, self.previousCell.top))
            if 0 < self.previousCell.y < 39:
                self.currentCell.map.array[self.currentCell.x][self.previousCell.y + 1].display()
                self.currentCell.map.get_cell(
                    self.currentCell.x, self.previousCell.y+1).display_around()

        if (len(self.currentCell.check_cell_around(Cell.Path)) >= 2 and not (self.previousCell.x == self.path[0].x or self.previousCell.y == self.path[0].y)) or self.building in self.currentCell.check_cell_around(Cell.House):
            for i in self.currentCell.check_cell_around(Cell.Path):
                i.display()

    def __str__(self):
        return "Migrant"

    def move(self):
        if not self.inBuilding:
            if len(self.path) == 1:
                self.enter_building()
                self.building.nextLevel()
                self.building.nb_occupants += 5
                self.building.unemployedCount += 5
                if self.building.nb_occupants == self.building.max_occupants and self.building.water:
                    self.building.nextLevel()
            elif len(self.path) != 0:
                self.movePathFinding()

    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop("walker_sprites")
        state.pop("cart_sprites")
        return state

    def __setstate__(self, state):
        super().__setstate__(state)
        state["cart_sprites"] = dict((k, pygame.image.load("walker_sprites/migrant_sprites/mg_cart_" +
                                                           k + ".png").convert_alpha()) for k in ["top", "bot", "left", "right"])
        self.__dict__.update(state)


class LaborAdvisor(Walker):
    def __init__(self, building):
        super().__init__("labor advisor", building, True)
        # self.leave_building()
        self.building.map.laborAdvisorQueue.append(self)
        self.walker_sprites = dict((k, [0, 0])
                                   for k in ["top", "bot", "left", "right"])
        for i in self.walker_sprites:
            for j in range(2):
                self.walker_sprites[i][j] = pygame.image.load(
                    "walker_sprites/LA_sprites/LA_" + i + "_" + str(j) + ".png").convert_alpha()
        # self.walker_sprites = dict((k,pygame.image.load("walker_sprites/LA_sprites/LA_" + k + ".png")) for k in ["top","bot","left","right"])

    def leave_building(self):
        super().leave_building()
        self.currentCell.map.laborAdvisorQueue.remove(self)

    def __str__(self):
        return "Labor Advisor"

    def move(self):
        if self.inBuilding:
            self.leave_building()
        elif len(self.path) == 1:
            self.enter_building()
            self.building.patrol()
        else:
            if self.building.requiredEmployees == self.building.employees:
                if len(self.path) == 0:
                    self.path_finding(self.currentCell, self.building)
                self.movePathFinding()
            else:
                super().move()
                HouseList = self.currentCell.check_cell_around(Cell.House)
                for i in HouseList:
                    if i.unemployedCount > 0:
                        if i.unemployedCount >= (self.building.requiredEmployees - self.building.employees):
                            i.unemployedCount -= (
                                self.building.requiredEmployees - self.building.employees)
                            self.building.employees = self.building.requiredEmployees
                        else:
                            self.building.employees += i.unemployedCount
                            i.unemployedCount = 0

    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop("walker_sprites")
        return state

    def __setstate__(self, state):
        super().__setstate__(state)
        self.__dict__.update(state)


class Prefect(Walker):
    risk_reset = True
    def __init__(self, current_prefecture):
        super().__init__("prefect", current_prefecture, True)
        self.current_building = current_prefecture
        self.extinguishCounter = 0
        self.waterCounter = 0
        self.isWorking = False
        self.orientation = None
        # self.walker_sprites = dict((k,pygame.image.load("walker_sprites/prefect_sprites/prefect_" + k + ".png")) for k in ["top","bot","left","right"])
        self.walker_sprites = dict((k, [0, 0])
                                   for k in ["top", "bot", "left", "right"])
        for i in self.walker_sprites:
            for j in range(2):
                self.walker_sprites[i][j] = pygame.image.load(
                    "walker_sprites/prefect_sprites/prefect_" + i + "_" + str(j) + ".png").convert_alpha()
        self.prefect_working_sprites = dict((k, [0 for _ in range(6)]) for k in [
                                            "top", "bot", "left", "right"])
        for i in self.prefect_working_sprites:
            for j in range(6):
                self.prefect_working_sprites[i][j] = pygame.image.load(
                    "walker_sprites/prefect_water_sprites/" + i + "/prefect_" + str(j) + ".png").convert_alpha()

    def __str__(self):
        return "Prefect"

    def move(self):
        self.wait += 1
        if self.wait <= 10:
            return
        # print("yoyoyoyo")
        if self.inBuilding:
            self.leave_building()
        elif self.isWorking:
            self.extinguishFire()

        elif any((i.risk.type == "fire" and i.risk.fireCounter > 0 and i not in self.currentCell.check_cell_around(Cell.Building))
                 for i in self.current_building.map.buildings) and not self.isWorking and not self.inBuilding:
            print(self.building.map.buildings[0].risk.fireCounter)
            self.building.map.buildings.sort(
                key=lambda x: x.risk.fireCounter, reverse=True)
            if len(self.path) == 0 or self.path[len(self.path)-1] == self.building:
                self.path_finding(self.currentCell,
                                  self.building.map.buildings[0])
            print(self.currentCell.x, self.currentCell.y)
            print(len(self.path))
            self.movePathFinding()
            if len(self.path) == 1:
                self.isWorking = True
                if self.path[0].x > self.currentCell.x:
                    self.orientation = "right"
                elif self.path[0].x < self.currentCell.x:
                    self.orientation = "left"
                elif self.path[0].y > self.currentCell.y:
                    self.orientation = "bot"
                elif self.path[0].y < self.currentCell.y:
                    self.orientation = "top"

            print(self.isWorking)

        elif len(self.path) == 1 and not self.isWandering:
            self.enter_building()
            self.wait = 0

        else:
            if self.ttl == 0:
                if len(self.path) == 0:
                    self.path_finding(self.currentCell, self.building)
                self.movePathFinding()
                if self.risk_reset : self.reset_fire_risk()
                if self.currentCell == self.current_building:
                    self.ttl = 50
            else:
                super().move()
                self.ttl -= 1
                if self.risk_reset : self.reset_fire_risk()

    def reset_fire_risk(self):
        cell = self.currentCell.check_cell_around(Cell.Building)
        for i in cell:
            if not isinstance(i, Cell.Prefecture) and not isinstance(i, Cell.Well) and not i.risk.happened:
                i.risk.resetEvent()
            for j in i.check_cell_around(Cell.Building) :
                if not isinstance(j, Cell.Prefecture) and not isinstance(j, Cell.Well) and not j.risk.happened:
                    j.risk.resetEvent()
            
           

    def extinguishFire(self):
        if self.extinguishCounter < 36:
            self.currentCell.display()
            SCREEN.blit(pygame.transform.scale(self.prefect_working_sprites[self.orientation][self.extinguishCounter % 6], (
                self.currentCell.width, self.currentCell.height)), (self.currentCell.left, self.currentCell.top))
            # print("working...")
            if self.waterCounter > 5:
                sound_effect["extinguish"].play()
                self.waterCounter = 0
            self.waterCounter += 1
            self.extinguishCounter += 1
        else:

            sound_effect["cooling"].play()
            self.extinguishCounter = 0
            self.current_building.map.buildings[0].risk.fireCounter = 0
            self.current_building.map.buildings[0].destroyed = True
            self.isWorking = False
            self.isWandering = True
            self.ttl = 3
            self.current_building.map.buildings[0].sprite = pygame.image.load(
                "risks_sprites/house_fire/fire_9.png").convert_alpha()
            self.current_building.map.buildings[0].path = "risks_sprites/house_fire/fire_9.png"
            self.current_building.map.buildings[0].update_sprite_size()
            self.current_building.map.buildings[0].display()
            # self.building.screen.blit(pygame.transform.scale(self.path[0].risk.fire_sprites[8],
            #                                                  (self.path[0].width, self.path[0].height)), (self.path[0].left, self.path[0].top))
            self.path = []
            print("Eteint")

    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop("walker_sprites")
        state.pop("prefect_working_sprites")
        return state

    def __setstate__(self, state):
        super().__setstate__(state)
        state["prefect_working_sprites"] = dict((k, [0 for _ in range(6)]) for k in [
            "top", "bot", "left", "right"])
        self.__dict__.update(state)
        for i in self.prefect_working_sprites:
            for j in range(6):
                self.prefect_working_sprites[i][j] = pygame.image.load(
                    "walker_sprites/prefect_water_sprites/" + i + "/prefect_" + str(j) + ".png").convert_alpha()
        self.__dict__.update(state)


class Engineer(Walker):
    def __init__(self, engineerPost):
        super().__init__("engineer", engineerPost, True)
        self.current_building = engineerPost
        # self.walker_sprites = dict((k,pygame.image.load("walker_sprites/engineer_sprites/engineer_" + k + ".png")) for k in ["top","bot","left","right"])
        self.walker_sprites = dict((k, [0, 0])
                                   for k in ["top", "bot", "left", "right"])
        for i in self.walker_sprites:
            for j in range(2):
                self.walker_sprites[i][j] = pygame.image.load(
                    "walker_sprites/engineer_sprites/engineer_" + i + "_" + str(j) + ".png").convert_alpha()

    def move(self):
        self.wait += 1
        if self.wait <= 10:
            return
        if self.inBuilding:
            self.leave_building()
        elif len(self.path) == 1 and not self.isWandering:
            self.enter_building()
            self.wait = 0
        else:
            if self.ttl == 0:
                if len(self.path) == 0:
                    self.path_finding(self.currentCell, self.building)
                self.movePathFinding()
                if self.currentCell == self.current_building:
                    self.ttl = 50
            else:
                super().move()
                self.ttl -= 1
                self.reset_collapse_risk()

    def reset_collapse_risk(self):
        cell = self.currentCell.check_cell_around(Cell.Building)
        for i in cell:
            if not isinstance(i, Cell.EngineerPost):
                i.risk.resetEvent()

    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop("walker_sprites")
        return state

    def __setstate__(self, state):
        super().__setstate__(state)
        self.__dict__.update(state)


# x increase -> right
# x decrease -> left
# y increase -> bot
# y decrease -> top
