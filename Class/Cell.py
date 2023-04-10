from email.policy import default
from Class.Walker import *
from Class.RiskEvent import *
import pygame
from random import *
from math import sqrt, floor
import random
import time
from Class.Sprites import *
import Class.Encoder as encode

SCREEN = None


def set_SCREEN_cell(screen):
    global SCREEN
    SCREEN = screen


sprites = Sprites()

overlay_risk = [
    {"sprite": pygame.image.load(
        "risks_sprites/overlay/overlay_0.png").convert_alpha(), "width": 58, "height": 30},
    {"sprite": pygame.image.load(
        "risks_sprites/overlay/overlay_1.png").convert_alpha(), "width": 48, "height": 63},
    {"sprite": pygame.image.load(
        "risks_sprites/overlay/overlay_2.png").convert_alpha(), "width": 48, "height": 73},
    {"sprite": pygame.image.load(
        "risks_sprites/overlay/overlay_3.png").convert_alpha(), "width": 48, "height": 83},
    {"sprite": pygame.image.load("risks_sprites/overlay/overlay_4.png").convert_alpha(), "width": 48, "height": 93}]


def draw_polygon_alpha(surface, color, points):
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.polygon(shape_surf, color, [
                        (x - min_x, y - min_y) for x, y in points])
    surface.blit(shape_surf, target_rect)


house_0 = pygame.image.load(
    "game_screen/game_screen_sprites/house_0.png").convert_alpha()


class Cell:  # Une case de la map

    def __init__(self, x, y, height, width, map, owner):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.map = map
        self.owner = owner
        self.type = ""
        self.water = 0
        self.sprite = ""
        self.path = ""
        self.aleatoire = 0
        self.hovered = 0
        self.type_empty = None
        self.house_mode = False
        self.WIDTH_SCREEN, self.HEIGHT_SCREEN = SCREEN.get_size()
        self.init_screen_coordonates()
        self.path_sprite = ""
        self.price = 5
        self.explored = False

    def update_sprite_size(self):
        pass

    def get_cells_around(self):
        return [self.map.get_cell(self.x-1, self.y) if self.map.inMap(self.x-1, self.y) else self,
                self.map.get_cell(
                    self.x+1, self.y) if self.map.inMap(self.x+1, self.y) else self,
                self.map.get_cell(
                    self.x, self.y-1) if self.map.inMap(self.x, self.y-1) else self,
                self.map.get_cell(self.x, self.y+1) if self.map.inMap(self.x, self.y+1) else self]

    def isBuildable(self, type=""):
        if type == "Farm":
            # print("putain")
            checkedArray = []
            for x in range(self.x-1, self.x+2):
                for y in range(self.y-1, self.y+2):
                    if self.map.inMap(x, y):
                        checkedArray.append(
                            self.map.get_cell(x, y).isBuildable())
                    else:
                        return False
            return all(checkedArray)

        elif type == "Granary":
            # print("salut")
            checkedArray = []
            for x in range(self.x-1, self.x+1):
                for y in range(self.y-1, self.y+1):
                    if self.map.inMap(x, y):
                        print(self.map.array[x][y])
                        checkedArray.append(
                            self.map.get_cell(x, y).isBuildable())
                    else:
                        return False
            return all(checkedArray)
        else:
            # print("ta mère")
            return isinstance(self, Empty) and self.type_empty == "dirt"

    def init_screen_coordonates(self):
        # Compute the x and y screen position of the cell
        self.left = (self.WIDTH_SCREEN/2 - self.WIDTH_SCREEN/12) + \
            self.width*self.x/2 - self.width*self.y/2 - self.map.offset_left
        self.top = self.HEIGHT_SCREEN/6 + self.x * \
            self.height/2 + self.y * self.height/2 + self.map.offset_top

    def display(self):
        if self.map.get_ownershiped() == True:
            self.display_ownership()

    def display_ownership(self):
        if self.owner == self.map.players[0]:
            draw_polygon_alpha(SCREEN, (0, 100, 255, 95),
                               self.get_points_polygone())
        elif self.owner == self.map.players[1]:
            draw_polygon_alpha(SCREEN, (255, 255, 50, 95),
                               self.get_points_polygone())
        elif self.owner == self.map.players[2]:
            draw_polygon_alpha(SCREEN, (255, 50, 0, 95),
                               self.get_points_polygone())
        elif self.owner == self.map.players[3]:
            draw_polygon_alpha(SCREEN, (255, 50, 255, 95),
                               self.get_points_polygone())

    def display_around(self):
        if (self.y+1 < 40 and (self.map.get_cell(self.x, self.y+1).type_empty != "dirt") and self.map.get_cell(self.x, self.y+1).type != "path"):
            if (self.map.get_cell(self.x, self.y+1).type_empty != "water"):
                self.map.get_cell(self.x, self.y+1).display()
                self.map.get_cell(self.x, self.y+1).display_around()
        if (self.x+1 < 40 and self.map.get_cell(self.x+1, self.y).type_empty != "dirt" and self.map.get_cell(self.x+1, self.y).type != "path"):
            if (self.map.get_cell(self.x+1, self.y).type_empty != "water"):
                self.map.get_cell(self.x+1, self.y).display()
                self.map.get_cell(self.x+1, self.y).display_around()
        if (self.x+1 < 40 and self.y+1 < 40 and self.map.get_cell(self.x+1, self.y+1).type_empty != "dirt" and self.map.get_cell(self.x+1, self.y+1).type != "path"):
            if (self.map.get_cell(self.x+1, self.y+1).type_empty != "water"):
                self.map.get_cell(self.x+1, self.y+1).display()
                self.map.get_cell(self.x+1, self.y+1).display_around()

    def display_around_shovel(self):
        if (self.x-1 > 0 and self.y-1 > 0):
            self.map.get_cell(self.x-1, self.y-1).display()
        if (self.y-1 > 0):
            self.map.get_cell(self.x, self.y-1).display()
        if (self.x-1 > 0):
            self.map.get_cell(self.x-1, self.y).display()
        if (self.x-1 > 0 and self.y+1 < 40 and self.map.get_cell(self.x-1, self.y+1).type_empty != "dirt" and self.map.get_cell(self.x-1, self.y+1).type != "path"):
            self.map.get_cell(self.x-1, self.y+1).display()
            self.map.get_cell(self.x-1, self.y+1).display_around()
        if (self.y-1 > 0 and self.x+1 < 40 and self.map.get_cell(self.x+1, self.y-1).type_empty != "dirt" and self.map.get_cell(self.x+1, self.y-1).type != "path"):
            self.map.get_cell(self.x+1, self.y-1).display()
            self.map.get_cell(self.x+1, self.y-1).display_around()
        if (self.y+1 < 40 and self.map.get_cell(self.x, self.y+1).type_empty != "dirt" and self.map.get_cell(self.x, self.y+1).type != "path"):
            self.map.get_cell(self.x, self.y+1).display()
            self.map.get_cell(self.x, self.y+1).display_around()
        if (self.x+1 < 40 and self.map.get_cell(self.x+1, self.y).type_empty != "dirt" and self.map.get_cell(self.x+1, self.y).type != "path"):
            self.map.get_cell(self.x+1, self.y).display()
            self.map.get_cell(self.x+1, self.y).display_around()
        if (self.x+1 < 40 and self.y+1 < 40 and self.map.get_cell(self.x+1, self.y+1).type_empty != "dirt" and self.map.get_cell(self.x+1, self.y+1).type != "path"):
            self.map.get_cell(self.x+1, self.y+1).display()
            self.map.get_cell(self.x+1, self.y+1).display_around()

    def handle_zoom(self, zoom_in):
        if zoom_in:
            self.height *= 1.05
            self.width *= 1.05
        else:
            self.height /= 1.05
            self.width /= 1.05
        self.init_screen_coordonates()
        self.update_sprite_size()
        self.display()

    def handle_move(self, move, m):
        if move == "up":
            self.top += 5 * m
        if move == "down":
            self.top -= 5 * m
        if move == "right":
            self.left -= 5 * m
        if move == "left":
            self.left += 5 * m

    def handle_hover_button(self):
        if (self.map.get_housed()):
            SCREEN.blit(pygame.transform.scale(
                house_0, (self.width, self.height)), (self.left, self.top))
            if self.isBuildable():
                draw_polygon_alpha(SCREEN, (0, 0, 0, 85),
                                   self.get_points_polygone())
            else:
                draw_polygon_alpha(SCREEN, (255, 0, 0, 85),
                                   self.get_points_polygone())
        elif self.map.get_road_button_activated() and not self.isBuildable():
            draw_polygon_alpha(SCREEN, (255, 0, 0, 85),
                               self.get_points_polygone())
        elif self.map.get_farmed() and not self.isBuildable("Farm"):
            draw_polygon_alpha(SCREEN, (255, 0, 0, 85),
                               self.get_points_polygone())
        else:
            if self.map.name_user == self.owner or self.map.get_ownershiped():
                draw_polygon_alpha(SCREEN, (0, 0, 0, 85),
                                   self.get_points_polygone())
            else:
                draw_polygon_alpha(SCREEN, (255, 0, 0, 85),
                                   self.get_points_polygone())

    def get_points_polygone(self):
        return ((self.left + self.width / 2, self.top), (self.left, self.top + self.height / 2),
                (self.left + self.width/2, self.top + self.height), (self.left + self.width, self.top + self.height / 2))

    def get_points_rectangle(self):
        return (self.left, self.top, self.left + self.width, self.top + self.height)

    def get_size(self):
        return (self.width, self.height)

    def get_pos(self):
        return (self.left, self.top)

    def get_hover(self):
        return self.hover

    def set_hover(self, hover):
        self.hover = hover

    def set_aleatoire(self, ent):
        self.aleatoire = ent

    def get_aleatoire(self):
        return self.aleatoire

    # Return an cell array which match with the class type (ex: Path, Prefecture (not a string)) in argument
    def check_cell_around(self, type):
        # print("farmPart", self.x, self.y)
        path = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if abs(i) != abs(j) and self.map.inMap(self.x + i, self.y + j):
                    if isinstance(self.map.get_cell(self.x + i, self.y + j), type):
                        # print("chemin ? ", self.map.get_cell(self.x + i, self.y + j))
                        path.append(self.map.get_cell(self.x + i, self.y + j))

        return path

    def build(self, type, owner=None):
        if owner == None:
            owner = self.owner
        if isinstance(self, Empty) and self.type_empty != "dirt":
            print("This cell is already taken")
            return
        if self.map.name_user != self.owner:
            print("The cell is not yours, you can't build on it")
        else:
            if self.map.players_online > 1 and owner == self.map.name_user: 
                encode.build(owner, self.x, self.y, type)
            match type:
                case "path":
                    self.map.set_cell_array(self.x, self.y, Path(
                        self.x, self.y, self.height, self.width, self.map, owner))
                    self.map.get_cell(self.x, self.y).handle_sprites()
                    self.map.get_cell(self.x, self.y).display()
                    self.map.wallet -= 4
                case "house":
                    self.map.set_cell_array(self.x, self.y, House(
                        self.x, self.y, self.height, self.width, self.map, owner))
                    self.map.wallet -= 10
                case "well":
                    self.map.set_cell_array(self.x, self.y, Well(
                        self.x, self.y, self.height, self.width, self.map, owner))
                    self.map.wallet -= 5
                case "prefecture":
                    self.map.set_cell_array(self.x, self.y, Prefecture(
                        self.x, self.y, self.height, self.width, self.map, owner))
                    self.map.wallet -= 30
                case "engineer post":
                    self.map.set_cell_array(self.x, self.y, EngineerPost(
                        self.x, self.y, self.height, self.width, self.map, owner))
                    self.map.wallet -= 30
                case "farm":
                    self.map.set_cell_array(self.x, self.y, Farm(
                        self.x, self.y, self.height, self.width, self.map, owner))
                    self.map.wallet -= 100
                case "granary":
                    self.map.set_cell_array(self.x, self.y, Granary(
                        self.x, self.y, self.height, self.width, self.map, owner))
                    self.map.wallet -= 100
            for i in range(-2, 3):
                for j in range(-2, 3):
                    if (37 > self.x > 3 and 37 > self.y > 3 and self.map.get_cell(self.x+i, self.y+j).type == "well"):
                        self.map.get_cell(self.x, self.y).set_water(1)

    def display_overlay(self):
        overlay = self.map.overlay
        match overlay:
            case "grid":
                pygame.draw.polygon(SCREEN, (25, 25, 25),
                                    self.get_points_polygone(), 2)

            case "fire" | "collapse":
                if isinstance(self, Building) and self.risk.type == self.map.overlay and self.risk.riskCounter < self.risk.riskTreshold:
                    i = floor(self.risk.riskCounter*5/self.risk.riskTreshold)
                    SCREEN.blit(pygame.transform.scale(overlay_risk[i]["sprite"], (
                        overlay_risk[i]["width"], overlay_risk[i]["height"])), (self.left, self.top+self.height-overlay_risk[i]["height"]))

            case "water":
                if self.water and self.map.get_welled() and self.type != "well":
                    draw_polygon_alpha(SCREEN, (0, 0, 255, 85),
                                       self.get_points_polygone())

    def clear(self):
        if isinstance(self, Path) and self.x == self.map.governor.currentCell.x and self.y == self.map.governor.currentCell.y:
            pass
        if isinstance(self, CityHall) or isinstance(self, CityHallPart) or isinstance(self, GranaryPart) or isinstance(self, FarmPart):
            pass
        elif not isinstance(self, Empty) and self.type_empty != "rock" and self.type_empty != "water":
            if self.map.players_online > 1 and self.owner == self.map.name_user: encode.clear(self.owner, self)
            for i in self.map.walkers:
                if i.building == self:
                    self.map.walkers.remove(i)
                    i.currentCell.display()
                    if isinstance(self, House):
                        i.previousCell.display()
            for i in self.map.migrantQueue:
                if i.building == self:
                    self.map.migrantQueue.remove(i)
                    i.currentCell.display()
            for i in self.map.laborAdvisorQueue:
                if i.building == self:
                    self.map.laborAdvisorQueue.remove(i)
                    i.currentCell.display()
            self.type_empty = "dirt"

            if isinstance(self, Granary):
                for i in range(-1, 1):
                    for j in range(-1, 1):
                        # print(self.map.array[self.x+i][self.y+j].x, self.map.array[self.x+i][self.y+j].y)
                        self.map.buildings.remove(
                            self.map.array[self.x+i][self.y+j])
                        self.map.set_cell_array(self.x+i, self.y+j, Empty(
                            self.x+i, self.y+j, self.height, self.width, self.map, self.owner, "dirt", 1))

            elif isinstance(self, GranaryPart):
                print(self.map.buildings)
                for i in range(-1, 1):
                    for j in range(-1, 1):
                        self.map.buildings.remove(
                            self.map.array[self.granary.x+i][self.granary.y+j])
                        self.map.set_cell_array(self.granary.x+i, self.granary.y+j, Empty(
                            self.granary.x+i, self.granary.y+j, self.height, self.width, self.map, self.owner, "dirt", 1))

            elif isinstance(self, Farm):
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        self.map.buildings.remove(
                            self.map.array[self.x+i][self.y+j])
                        self.map.set_cell_array(self.x+i, self.y+j, Empty(
                            self.x+i, self.y+j, self.height, self.width, self.map, self.owner, "dirt", 1))

            elif isinstance(self, Crop):
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        self.map.buildings.remove(
                            self.map.array[self.building.x+i][self.building.y+j])
                        self.map.set_cell_array(self.building.x+i, self.building.y+j, Empty(
                            self.building.x+i, self.building.y+j, self.height, self.width, self.map, self.owner, "dirt", 1))

            elif isinstance(self, FarmPart):
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        self.map.buildings.remove(
                            self.map.array[self.farm.x+i][self.farm.y+j])
                        self.map.set_cell_array(self.farm.x+i, self.farm.y+j, Empty(
                            self.farm.x+i, self.farm.y+j, self.height, self.width, self.map, self.owner, "dirt", 1))

            else:
                if isinstance(self, Building):
                    self.map.buildings.remove(self)
                self.map.set_cell_array(self.x, self.y, Empty(
                    self.x, self.y, self.height, self.width, self.map, self.owner, "dirt", 1))

            arr = self.check_cell_around(Cell)
            for i in arr:
                if not isinstance(i, Building):
                    i.display()
                for j in i.check_cell_around(Cell):
                    if j.x < self.x + 2 and j.y < self.y + 2:
                        # and not (j in [i.map.array[i.x-1][i.y], i.map.array[i.x - 1][i.y - 1]]) and (isinstance(i, Cell.Prefecture) or isinstance(i, Cell.EngineerPost)):
                        if not isinstance(j, Building):
                            j.display()
            self.map.wallet -= 2

    def set_type(self, type):
        self.type = type

    def set_water(self, bool):
        self.water = bool

    def get_water(self):
        return self.water


path_hori = "game_screen/game_screen_sprites/road_straight_hori.png"
sprite_hori = pygame.image.load(path_hori).convert_alpha()

path_verti = "game_screen/game_screen_sprites/road_straight_verti.png"
sprite_verti = pygame.image.load(path_verti).convert_alpha()

path_all_turn = "game_screen/game_screen_sprites/road_turn_all.png"
sprite_all_turn = pygame.image.load(path_all_turn).convert_alpha()

path_bot_left = "game_screen/game_screen_sprites/road_turn_bot_left.png"
sprite_turn_bot_left = pygame.image.load(path_bot_left).convert_alpha()

path_bot_right = "game_screen/game_screen_sprites/road_turn_bot_right.png"
sprite_turn_bot_right = pygame.image.load(path_bot_right).convert_alpha()

path_hori_bot = "game_screen/game_screen_sprites/road_turn_hori_bot.png"
sprite_turn_hori_bot = pygame.image.load(path_hori_bot).convert_alpha()

path_hori_top = "game_screen/game_screen_sprites/road_turn_hori_top.png"
sprite_turn_hori_top = pygame.image.load(path_hori_top).convert_alpha()

path_left_top = "game_screen/game_screen_sprites/road_turn_left_top.png"
sprite_turn_left_top = pygame.image.load(path_left_top).convert_alpha()

path_right_top = "game_screen/game_screen_sprites/road_turn_right_top.png"
sprite_turn_right_top = pygame.image.load(path_right_top).convert_alpha()

path_verti_left = "game_screen/game_screen_sprites/road_turn_verti_left.png"
sprite_turn_verti_left = pygame.image.load(path_verti_left).convert_alpha()

path_verti_right = "game_screen/game_screen_sprites/road_turn_verti_right.png"
sprite_turn_verti_right = pygame.image.load(path_verti_right).convert_alpha()


class Path(Cell):

    def __init__(self, x, y, height, width, map, owner, path_level=0):
        super().__init__(x, y, height, width, map, owner)
        self.path_sprite = path_verti
        self.sprite = sprite_verti
        self.sprite_display = ""
        self.level = path_level
        self.handle_sprites()
        self.update_sprite_size()
        self.type = "path"
        # Get an array of all neighbor path
        cell_around = self.check_cell_around(Path)
        # Loop through this array
        for i in cell_around:
            self.map.path_graph.add_edge(self, i)
            self.map.path_graph.add_edge(i, self)

        house_around = self.check_cell_around(House)
        for j in house_around:
            self.map.path_graph.add_edge(self, j)
            self.map.path_graph.add_edge(j, self, weight=2000)
            house_around_house = j.check_cell_around(House)
            for k in house_around_house:
                self.map.path_graph.add_edge(j, k, weight=2000)

        farm_around = self.check_cell_around(FarmPart)
        for l in farm_around:
            self.map.path_graph.add_edge(self, l.farm)

        granary_around = self.check_cell_around(Granary)
        for m in granary_around:
            self.map.path_graph.add_edge(self, m, weight=2000)

    def update_sprite_size(self):
        self.sprite_display = pygame.transform.scale(
            self.sprite, (self.width+2*sqrt(2), self.height+2))

    def display(self):
        SCREEN.blit(self.sprite_display, (self.left-sqrt(2), self.top-1))
        self.display_overlay()
        super().display()

    def handle_sprites(self, r=0):
        if r < 2:
            # Check if the road is in all turns
            if self.check_surrondings([1, 1, 1, 1]):
                self.path_sprite = path_all_turn
                self.set_sprite(sprite_all_turn)
                self.map.get_cell(self.x - 1, self.y).handle_sprites(r + 1)
                self.map.get_cell(self.x + 1, self.y).handle_sprites(r + 1)
                self.map.get_cell(self.x, self.y - 1).handle_sprites(r + 1)
                self.map.get_cell(self.x, self.y + 1).handle_sprites(r + 1)
                return

            # Check if the road is a turn bottom to left
            if self.check_surrondings([1, 0, 1, 0]):
                self.path_sprite = path_bot_left
                self.set_sprite(sprite_turn_bot_left)
                self.map.get_cell(self.x - 1, self.y).handle_sprites(r + 1)
                self.map.get_cell(self.x, self.y + 1).handle_sprites(r + 1)
                return

            # Check if the road is a turn bottom to right
            if self.check_surrondings([0, 0, 1, 1]):
                self.path_sprite = path_bot_right
                self.set_sprite(sprite_turn_bot_right)
                self.map.get_cell(self.x + 1, self.y).handle_sprites(r + 1)
                self.map.get_cell(self.x, self.y + 1).handle_sprites(r + 1)

                return
            # Check if the road is a turn horizontal to bottom
            if self.check_surrondings([1, 0, 1, 1]):
                self.path_sprite = path_hori_bot
                self.set_sprite(sprite_turn_hori_bot)
                self.map.get_cell(self.x + 1, self.y).handle_sprites(r + 1)
                self.map.get_cell(self.x - 1, self.y).handle_sprites(r + 1)
                self.map.get_cell(self.x, self.y + 1).handle_sprites(r + 1)

                return
            # Check if the road is a turn horizontal to top
            if self.check_surrondings([1, 1, 0, 1]):
                self.path_sprite = path_hori_top
                self.set_sprite(sprite_turn_hori_top)
                self.map.get_cell(self.x + 1, self.y).handle_sprites(r + 1)
                self.map.get_cell(self.x - 1, self.y).handle_sprites(r + 1)
                self.map.get_cell(self.x, self.y - 1).handle_sprites(r + 1)

                return
            # Check if the road is a turn letf to top
            if self.check_surrondings([1, 1, 0, 0]):
                self.path_sprite = path_left_top
                self.set_sprite(sprite_turn_left_top)
                self.map.get_cell(self.x - 1, self.y).handle_sprites(r + 1)
                self.map.get_cell(self.x, self.y - 1).handle_sprites(r + 1)

                return
            # Check if the road is a turn right to top
            if self.check_surrondings([0, 1, 0, 1]):
                self.path_sprite = path_right_top
                self.set_sprite(sprite_turn_right_top)
                self.map.get_cell(self.x + 1, self.y).handle_sprites(r + 1)
                self.map.get_cell(self.x, self.y - 1).handle_sprites(r + 1)

                return
            # Check if the road is a turn vertical to left
            if self.check_surrondings([1, 1, 1, 0]):
                self.path_sprite = path_verti_left
                self.set_sprite(sprite_turn_verti_left)
                self.map.get_cell(self.x - 1, self.y).handle_sprites(r + 1)
                self.map.get_cell(self.x, self.y - 1).handle_sprites(r + 1)
                self.map.get_cell(self.x, self.y + 1).handle_sprites(r + 1)

                return
            # Check if the road is a turn vertical to right
            if self.check_surrondings([0, 1, 1, 1]):
                self.path_sprite = path_verti_right
                self.set_sprite(sprite_turn_verti_right)
                self.map.get_cell(self.x + 1, self.y).handle_sprites(r + 1)
                self.map.get_cell(self.x, self.y - 1).handle_sprites(r + 1)
                self.map.get_cell(self.x, self.y + 1).handle_sprites(r + 1)

                return

            # Check horizontal road
            if self.check_surrondings([2, 0, 0, 1]):
                self.path_sprite = path_hori
                self.set_sprite(sprite_hori)
                self.map.get_cell(self.x + 1, self.y).handle_sprites(r + 1)
                if isinstance(self.map.get_cell(self.x - 1, self.y), Path):
                    self.map.get_cell(self.x - 1, self.y).handle_sprites(r + 1)

                return
            if self.check_surrondings([1, 0, 0, 2]):
                self.path_sprite = path_hori
                self.set_sprite(sprite_hori)
                self.map.get_cell(self.x - 1, self.y).handle_sprites(r + 1)
                if isinstance(self.map.get_cell(self.x + 1, self.y), Path):
                    self.map.get_cell(self.x + 1, self.y).handle_sprites(r + 1)

                return
            # Check vertical road
            if self.check_surrondings([0, 2, 1, 0]):
                self.path_sprite = path_verti
                self.set_sprite(sprite_verti)
                self.map.get_cell(self.x, self.y + 1).handle_sprites(r + 1)
                if isinstance(self.map.get_cell(self.x, self.y - 1), Path):
                    self.map.get_cell(self.x, self.y - 1).handle_sprites(r + 1)

                return
            if self.check_surrondings([0, 1, 2, 0]):
                self.path_sprite = path_verti
                self.set_sprite(sprite_verti)
                self.map.get_cell(self.x, self.y - 1).handle_sprites(r + 1)
                if isinstance(self.map.get_cell(self.x, self.y + 1), Path):
                    self.map.get_cell(self.x, self.y + 1).handle_sprites(r + 1)

                return

    def check_surrondings(self, check):
        i = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if abs(dx) != abs(dy):
                    if check[i] != 2 and isinstance(self.map.get_cell(self.x + dx, self.y + dy), Path) != check[i]:
                        return 0
                    i += 1
        return 1

    def set_sprite(self, sprite):
        self.sprite = sprite
        self.update_sprite_size()
        self.display()

    def __str__(self):
        return f"Chemin { self.level}"

    def __getstate__(self):
        state = self.__dict__.copy()
        sprite = state.pop("sprite")
        spriye_display = state.pop("sprite_display")
        state["path_sprite"] = self.path_sprite
        return state

    def __setstate__(self, state):
        path_sprite = state.pop("path_sprite")
        self.path_sprite = path_sprite
        state["sprite"] = pygame.image.load(path_sprite).convert_alpha()
        state["sprite_display"] = None
        self.__dict__.update(state)
        self.update_sprite_size()


class Empty(Cell):
    def __init__(self, x, y, height, width, screen, map, type_empty="dirt", shoveled=0):
        super().__init__(x, y, height, width, screen, map)
        self.type_empty = type_empty  # "dirt", "trees"
        self.type = "empty"
        self.tree_or_dirt_list = ["tree", "dirt", "dirt"]
        self.path_sprite = ""
        self.type_sprite = "dirt"
        if randint(1, 3) == 1 and shoveled == 0:
            self.type_sprite = "tree"
            self.type_empty = "tree"
        if (self.type_empty == "dirt"):
            aleatoire = randint(1, 12)
        else:
            aleatoire = randint(1, 4)
        super().set_aleatoire(aleatoire)
        self.path_sprite = "game_screen/game_screen_sprites/" + \
            self.type_sprite + "_" + str(aleatoire) + ".png"
        self.sprite = sprites.get_sprites(
        )['dirt_' + str(self.aleatoire)]['sprite_ori']
        self.sprite_display = ""
        self.update_sprite_size()
        self.display()

    def __str__(self):
        return self.type_empty

    def update_sprite_size(self):
        if self.type_empty == "tree":
            if self.aleatoire == 1:
                sprites.update_size_sprites(self.type_sprite + "_" + str(self.aleatoire),
                                            self.width, self.height*42/30)
            elif self.aleatoire == 2:
                sprites.update_size_sprites(self.type_sprite + "_" + str(self.aleatoire),
                                            self.width, self.height*41/30)
            elif self.aleatoire == 3:
                sprites.update_size_sprites(self.type_sprite + "_" + str(self.aleatoire),
                                            self.width, self.height*44/30)
            elif self.aleatoire == 4:
                sprites.update_size_sprites(self.type_sprite + "_" + str(self.aleatoire),
                                            self.width, self.height*45/30)
        else:
            sprites.update_size_sprites(self.type_sprite + "_" + str(self.aleatoire),
                                        self.width+2*sqrt(2), self.height+2)
        self.sprite_display = sprites.get_sprites(
        )[str(self.type_sprite) + "_" + str(self.aleatoire)]['sprite_display']

    def display(self):
        """if self.type_empty == "tree":
            if self.aleatoire == 1:
                SCREEN.blit(
                    self.sprite_display, (self.left, self.top - self.height*12/30))
            elif self.aleatoire == 2:
                SCREEN.blit(
                    self.sprite_display, (self.left, self.top - self.height*11/30))
            elif self.aleatoire == 3:
                SCREEN.blit(
                    self.sprite_display, (self.left, self.top - self.height*14/30))
            elif self.aleatoire == 4:
                SCREEN.blit(
                    self.sprite_display, (self.left, self.top - self.height*15/30))
        elif self.type_empty == "rock":
            SCREEN.blit(
                self.sprite_display, (self.left, self.top-self.height*5/30))
        else:
            SCREEN.blit(self.sprite_display,
                        (self.left-sqrt(2), self.top-1))"""
        if self.left + self.width >= 0 and self.left - self.width <= self.WIDTH_SCREEN and self.top + self.height >= 0 and self.top - self.height <= self.HEIGHT_SCREEN:
            if self.type_empty == "tree":
                if self.aleatoire == 1:
                    SCREEN.blit(
                        self.sprite_display, (self.left, self.top - self.height*12/30))
                elif self.aleatoire == 2:
                    SCREEN.blit(
                        self.sprite_display, (self.left, self.top - self.height*11/30))
                elif self.aleatoire == 3:
                    SCREEN.blit(
                        self.sprite_display, (self.left, self.top - self.height*14/30))
                elif self.aleatoire == 4:
                    SCREEN.blit(
                        self.sprite_display, (self.left, self.top - self.height*15/30))
            else:
                SCREEN.blit(self.sprite_display,
                            (self.left-sqrt(2), self.top-1))
            self.display_overlay()
            super().display()

    def clear(self):
        if self.type_empty == "tree":
            self.type_empty = "dirt"
            self.type_sprite = "dirt"
            self.path_sprite = "game_screen/game_screen_sprites/" + \
                self.type_sprite + "_" + str(self.aleatoire) + ".png"
            self.sprite = pygame.image.load(self.path_sprite).convert_alpha()
            self.map.wallet -= 2
        self.update_sprite_size()
        self.display()

    def canBuild(self):
        return self.type_empty == "dirt"

    def __getstate__(self):
        state = self.__dict__.copy()
        sprite = state.pop("sprite")
        sprite_display = state.pop("sprite_display")
        state["path_sprite"] = self.path_sprite
        return state

    def __setstate__(self, state):
        path_sprite = state.pop("path_sprite")
        self.path_sprite = path_sprite
        state["sprite"] = pygame.image.load(path_sprite).convert_alpha()
        state["sprite_display"] = None
        self.__dict__.update(state)
        self.update_sprite_size()


class Building(Cell):  # un fils de cellule (pas encore sûr de l'utilité)
    def __init__(self, x, y, height, width, map, owner):
        super().__init__(x, y, height, width,  map, owner)

        self.destroyed = False
        path_around = self.check_cell_around(Path)
        house_around = self.check_cell_around(House)
        self.path_sprite = ""

        if self.owner == self.map.name_user:
            self.map.buildings.append(self)
            for j in path_around:
                # if isinstance
                self.map.path_graph.add_edge(j, self)
                self.map.path_graph.add_edge(self, j, weight=2000)
                if isinstance(self, House) and len(house_around) != 0:
                    for k in house_around:
                        self.map.path_graph.add_edge(j, k, weight=2000)

    def destroy(self):
        self.destroyed = 1


class House(Building):  # la maison fils de building (?)
    def __init__(self, x, y, height, width, map, owner, level=0, nb_occupants=0):
        super().__init__(x, y, height, width, map, owner)
        self.level = level  # niveau de la maison : int
        self.nb_occupants = nb_occupants  # nombre d'occupants: int
        # nombre max d'occupant (dépend du niveau de la maison) : int
        self.max_occupants = 5
        self.unemployedCount = 0
        self.risk = RiskEvent("fire", self)
        if owner == map.name_user:
            self.migrant = Migrant(self, owner)
        # Temporary
        self.path_sprite = "game_screen/game_screen_sprites/house_" + \
            str(self.level) + ".png"
        self.sprite = pygame.image.load(self.path_sprite).convert_alpha()
        self.sprite_display = ""
        self.update_sprite_size()
        self.type = "house"
        if owner == map.name_user:
            house_around = self.check_cell_around(House)
            for i in house_around:
                path_around = i.check_cell_around(Path)
                if len(path_around) != 0:
                    self.map.path_graph.add_edge(i, self, weight=2000)
        self.display()

    def __str__(self):
        return f"House { self.level}"

    def update_sprite_size(self):
        self.sprite_display = pygame.transform.scale(
            self.sprite, (self.width+2*sqrt(2), self.height+2))

    def display(self):
        SCREEN.blit(self.sprite_display, (self.left-sqrt(2), self.top-1))
        self.display_overlay()
        super().display()

    def nextLevel(self):
        if self.map.players_online > 1 and self.owner == self.map.name_user: encode.levelup(self.owner, self, self.level+1)
        self.level += 1
        self.path_sprite = "game_screen/game_screen_sprites/house_" + \
            str(self.level) + ".png"
        self.sprite = pygame.image.load(self.path_sprite).convert_alpha()
        self.update_sprite_size()
        self.display()
        match self.level:
            case 2:
                self.max_occupants = 7
            case 3:
                self.max_occupants = 9

    def __getstate__(self):
        state = self.__dict__.copy()
        sprite = state.pop("sprite")
        sprite_display = state.pop("sprite_display")
        state["path_sprite"] = self.path_sprite
        return state

    def __setstate__(self, state):
        path_sprite = state.pop("path_sprite")
        self.path_sprite = path_sprite
        state["sprite"] = pygame.image.load(path_sprite).convert_alpha()
        state["sprite_display"] = None
        self.__dict__.update(state)
        self.update_sprite_size()


class Well(Building):
    def __init__(self, x, y, height, width, map, owner):
        super().__init__(x, y, height, width, map, owner)
        # le risque est la en stand by
        self.risk = RiskEvent("collapse", self)
        for i in range(-2, 3):
            for j in range(-2, 3):
                if (39 >= self.x+i >= 0 and 39 >= self.y+j >= 0):
                    self.map.get_cell(self.x+i, self.y+j).water = 1
                    checkedCell = self.map.get_cell(self.x+i, self.y+j)
                    if isinstance(checkedCell, House) and checkedCell.level == 1 and checkedCell.max_occupants == checkedCell.nb_occupants:
                        checkedCell.nextLevel()
        self.path_sprite = "game_screen/game_screen_sprites/well.png"
        self.sprite = pygame.image.load(self.path_sprite).convert_alpha()
        self.sprite_display = ""
        self.update_sprite_size()
        self.type = "well"

    def update_sprite_size(self):
        if (self.type == "ruin"):
            self.sprite_display = pygame.transform.scale(
                self.sprite, (self.width, self.height*34/30))
        else:
            self.sprite_display = pygame.transform.scale(
                self.sprite, (self.width, self.height*53/30))

    def display(self):
        if (self.type == "ruin"):
            SCREEN.blit(self.sprite_display,
                        (self.left, self.top - self.height*4/30))
        else:
            SCREEN.blit(self.sprite_display,
                        (self.left, self.top - self.height*23/30))
        self.display_overlay()
        super().display()

    def __str__(self):
        return "Puit"

    def __getstate__(self):
        state = self.__dict__.copy()
        sprite = state.pop("sprite")
        spriye_display = state.pop("sprite_display")
        state["path_sprite"] = self.path_sprite
        return state

    def __setstate__(self, state):
        path_sprite = state.pop("path_sprite")
        self.path_sprite = path_sprite
        state["sprite"] = pygame.image.load(path_sprite).convert_alpha()
        state["sprite_display"] = None
        self.__dict__.update(state)
        self.update_sprite_size()


class Prefecture(Building):
    def __init__(self, x, y, height, width, map, owner):
        super().__init__(x, y, height, width, map, owner)
        self.labor_advisor = LaborAdvisor(self, self.owner)
        self.employees = 0
        self.requiredEmployees = 5
        self.risk = RiskEvent("collapse", self)
        if self.owner == self.map.name_user:
            self.prefect = Prefect(self, owner)
        self.path_sprite = "game_screen/game_screen_sprites/prefecture.png"
        self.sprite = pygame.image.load(self.path_sprite).convert_alpha()
        self.sprite_display = ""
        self.update_sprite_size()
        self.type = "prefecture"

    def update_sprite_size(self):
        if self.type == "ruin":
            self.sprite_display = pygame.transform.scale(
                self.sprite, (self.width, self.height*34/30))
        else:
            self.sprite_display = pygame.transform.scale(
                self.sprite, (self.width, self.height*38/30))

    def display(self):
        if self.type == "ruin":
            SCREEN.blit(
                self.sprite_display, (self.left, self.top - self.height*4/30))
        else:
            SCREEN.blit(self.sprite_display,
                        (self.left, self.top - self.height*8/30))
        self.display_overlay()
        super().display()

    def __str__(self):
        return f"Prefecture { self.employees}"

    def patrol(self):
        self.prefect.leave_building()

    def __getstate__(self):
        state = self.__dict__.copy()
        sprite = state.pop("sprite")
        spriye_display = state.pop("sprite_display")
        state["path_sprite"] = self.path_sprite
        return state

    def __setstate__(self, state):
        path_sprite = state.pop("path_sprite")
        self.path_sprite = path_sprite
        state["sprite"] = pygame.image.load(path_sprite).convert_alpha()
        state["sprite_display"] = None
        self.__dict__.update(state)
        self.update_sprite_size()


class EngineerPost(Building):
    def __init__(self, x, y, height, width, map, owner):
        super().__init__(x, y, height, width, map, owner)
        self.labor_advisor = LaborAdvisor(self, self.owner)
        self.employees = 0
        self.requiredEmployees = 5
        self.risk = RiskEvent("fire", self)
        if self.owner == self.map.name_user:
            self.engineer = Engineer(self, owner)
        self.path_sprite = "game_screen/game_screen_sprites/engineerpost.png"
        self.sprite = pygame.image.load(self.path_sprite).convert_alpha()
        self.sprite_display = ""
        self.update_sprite_size()
        self.type = "engineer post"

    def display(self):
        if self.type == "ruin":
            SCREEN.blit(
                self.sprite_display, (self.left, self.top))
        else:
            SCREEN.blit(
                self.sprite_display, (self.left, self.top - self.height*20/30))
        self.display_overlay()
        super().display()

    def update_sprite_size(self):
        if (self.type == "ruin"):
            self.sprite_display = pygame.transform.scale(
                self.sprite, (self.width, self.height))

        else:
            self.sprite_display = pygame.transform.scale(
                self.sprite, (self.width, self.height*50/30))

    def __str__(self):
        return "Engineer Post"

    def patrol(self):
        self.engineer.leave_building()

    def __getstate__(self):
        state = self.__dict__.copy()
        sprite = state.pop("sprite")
        sprite_display = state.pop("sprite_display")
        state["path_sprite"] = self.path_sprite
        return state

    def __setstate__(self, state):
        path_sprite = state.pop("path_sprite")
        self.path_sprite = path_sprite
        state["sprite"] = pygame.image.load(path_sprite).convert_alpha()
        state["sprite_display"] = None
        self.__dict__.update(state)
        self.update_sprite_size()


class Crop(Building):
    def __init__(self, x, y, height, width, map, owner, farm):
        super().__init__(x, y, height, width, map, owner)
        self.building = farm
        self.grow_state = 0
        self.path_sprite = "game_screen/game_screen_sprites/farm.png"
        self.sprite = dict((k, pygame.image.load(
            self.path_sprite[0:-4] + "_" + str(k) + ".png").convert_alpha()) for k in range(5))
        self.sprite_display = []
        for i in range(5):
            self.sprite_display.append(
                self.sprite[i])
        self.risk = RiskEvent("prout", self)
        self.update_sprite_size()

    def __str__(self):
        return "Crop"

    def update_sprite_size(self):
        self.sprite_display[0] = pygame.transform.scale(
            self.sprite[0], (self.width * 28/30, self.height))
        self.sprite_display[1] = pygame.transform.scale(
            self.sprite[1], (self.width * 29/30, self.height * 28/30))
        self.sprite_display[2] = pygame.transform.scale(
            self.sprite[2], (self.width * 30/30, self.height*32/30))
        self.sprite_display[3] = pygame.transform.scale(
            self.sprite[3], (self.width*25/30, self.height*35/30))
        self.sprite_display[4] = pygame.transform.scale(
            self.sprite[4], (self.width*25/30, self.height*40/30))

    def display(self):
        i = self.grow_state

        match i//10:
            case 0:
                # print(self.x,self.y, i//10)
                SCREEN.blit(
                    self.sprite_display[0], (self.left, self.top))
            case 1:
                # print(self.x,self.y, i//10)
                SCREEN.blit(
                    self.sprite_display[1], (self.left, self.top))
            case 2:
                # print(self.x,self.y, i//10)
                SCREEN.blit(
                    self.sprite_display[2], (self.left-self.width*0, self.top-self.height*0.17))
            case 3:
                # print(self.x,self.y, i//10)
                SCREEN.blit(
                    self.sprite_display[3], (self.left+self.width*0.07, self.top-self.height*0.21))
            case 4:
                # print(self.x,self.y, i//10)
                SCREEN.blit(
                    self.sprite_display[4], (self.left+self.width*0.1, self.top-self.height*0.34))
        super().display()


class CityHallPart(Building):
    def __init__(self, x, y, height, width, map, owner, my_cityhall):
        super().__init__(x, y, height, width, map, owner)
        self.cityhall = my_cityhall
        self.risk = self.cityhall.risk

        path_around = self.check_cell_around(Path)
        for i in path_around:
            if len(path_around) != 0:
                self.map.path_graph.add_edge(i, self.cityhall, weight=2000)

    def display(self):
        super().display()


class CityHall(Building):
    def __init__(self, x, y, height, width, map, owner):
        super().__init__(x, y, height, width, map, owner)
        self.risk =RiskEvent("prout", self)
        self.path_sprite = "game_screen/game_screen_sprites/cityhall.png"
        self.sprite = pygame.image.load(self.path_sprite).convert_alpha()
        self.sprite_display = ""
        self.update_sprite_size()
        self.map.array[self.x - 1][self.y] = CityHallPart(
            self.x - 1, self.y, height, width, map, owner, self)
        self.map.array[self.x][self.y - 1] = CityHallPart(
            self.x, self.y - 1, height, width, map, owner,  self)
        self.map.array[self.x - 1][self.y - 1] = CityHallPart(
            self.x - 1, self.y - 1, height, width, map, owner, self)
        self.type = "cityhall"

    def display(self):
        SCREEN.blit(
            self.sprite_display, (self.left - self.width*108/232, self.top - self.height*170/120))
        self.display_overlay()
        super().display()
        self.map.get_cell(self.x - 1, self.y).display()
        self.map.get_cell(self.x, self.y - 1).display()
        self.map.get_cell(self.x - 1, self.y - 1).display()

    def update_sprite_size(self):
        self.sprite_display = pygame.transform.scale(
            self.sprite, (self.width*356/232*1.25, self.height*230/120*1.25))

    def __str__(self):
        return "City Hall"

    def patrol(self):
        self.guard.leave_building()

    def __getstate__(self):
        state = self.__dict__.copy()
        sprite = state.pop("sprite")
        sprite_display = state.pop("sprite_display")
        state["path_sprite"] = self.path_sprite
        return state

    def __setstate__(self, state):
        path_sprite = state.pop("path_sprite")
        self.path_sprite = path_sprite
        state["sprite"] = pygame.image.load(path_sprite).convert_alpha()
        state["sprite_display"] = None
        self.__dict__.update(state)
        self.update_sprite_size()


class FarmPart(Building):
    def __init__(self, x, y, height, width, map, owner, my_farm):
        super().__init__(x, y, height, width, map, owner)
        self.farm = my_farm
        self.risk = self.farm.risk

        path_around = self.check_cell_around(Path)
        for i in path_around:
            if len(path_around) != 0:
                self.map.path_graph.add_edge(i, self.farm, weight=2000)

    def display(self):
        super().display()


class Farm(Building):
    def __init__(self, x, y, height, width, map, owner):
        super().__init__(x, y, height, width, map, owner)
        if self.owner == self.map.name_user:
            self.farmer = Farmer(self, owner)
        self.risk = RiskEvent("prout", self)
        self.path_sprite = "game_screen/game_screen_sprites/farm.png"
        self.sprite = pygame.image.load(self.path_sprite).convert_alpha()
        self.sprite_display = ""
        self.update_sprite_size()
        self.farmParts = []
        self.map.array[self.x - 1][self.y] = FarmPart(
            self.x - 1, self.y, height, width, map, owner, self)
        self.farmParts.append(self.map.array[self.x - 1][self.y])
        self.map.array[self.x][self.y -
                               1] = FarmPart(self.x, self.y-1, height, width, map, owner, self)
        self.farmParts.append(self.map.array[self.x][self.y-1])
        self.map.array[self.x - 1][self.y -
                                   1] = FarmPart(self.x-1, self.y-1, height, width, map, owner, self)
        self.farmParts.append(self.map.array[self.x - 1][self.y-1])
        self.crops = []
        for x in range(2):
            self.crops.append(Crop(self.x + x - 1, self.y +
                              2 - 1, height, width, map, owner, self))
            self.map.array[self.x+x-1][self.y+2 -
                                       1] = self.crops[len(self.crops)-1]
        for y in (2, 1, 0):
            self.crops.append(Crop(self.x + 2 - 1, self.y +
                              y - 1, height, width, map, owner, self))
            self.map.array[self.x+2-1][self.y+y -
                                       1] = self.crops[len(self.crops)-1]
        # for i in self.crops :
        #     self.map.array[i.x][i.y] = i
        #     # print(i.x, i.y)

        self.update_sprite_size()

    def __str__(self):
        return "Farm"

    def update_sprite_size(self):
        self.sprite_display = pygame.transform.scale(
            self.sprite, (self.width * 60/30, self.height*95/30))

    def display(self):
        SCREEN.blit(
            self.sprite_display, (self.left - self.width*0.5, self.top - self.height*2))
        super().display()

    def crop_grow(self):
        for i in self.crops:
            if i.grow_state < 49:
                i.grow_state += 1
                i.display()
                break
        # print(i.x, i.y, i.grow_state)

        if all(i.grow_state >= 49 for i in self.crops):
            for i in self.crops:
                i.grow_state = 0
            if all(not isinstance(i, Granary) for i in self.map.buildings):
                print("allo ? ")
                return

            self.farmer.delivering = True
            # print("aslureagzea")
            ingraph = self.farmer.leave_building()
            # if not ingraph :
            #     print("salut")
            #     return
            for i in self.map.buildings:
                if isinstance(i, Granary):
                    tmpPath = nx.dijkstra_path(
                        self.map.path_graph, self.farmer.currentCell, i)
                    # print(tmpPath)
                    if len(self.farmer.path) == 0 or len(self.farmer.path) > len(tmpPath):
                        self.farmer.path = tmpPath


class Granary(Building):
    def __init__(self, x, y, height, width, map, owner):
        super().__init__(x, y, height, width, map, owner)
        self.risk = RiskEvent("prout", self)
        self.path_sprite1 = "game_screen/game_screen_sprites/granary_floor.png"
        self.path_sprite2 = "game_screen/game_screen_sprites/granary_body.png"
        self.sprite = [pygame.image.load(self.path_sprite1).convert_alpha(
        ), pygame.image.load(self.path_sprite2).convert_alpha()]
        self.sprite_display = [None, None]
        self.update_sprite_size()

        self.map.array[self.x - 1][self.y] = GranaryPart(
            self.x - 1, self.y, height, width, map, owner, self)
        self.map.array[self.x][self.y - 1] = GranaryPart(
            self.x, self.y - 1, height, width, map, owner,  self)
        self.map.array[self.x - 1][self.y - 1] = GranaryPart(
            self.x - 1, self.y - 1, height, width, map, owner, self)

    def update_sprite_size(self):

        self.sprite_display[0] = pygame.transform.scale(
            self.sprite[0], (self.width * 60/30, self.height*60/30))
        self.sprite_display[1] = pygame.transform.scale(
            self.sprite[1], (self.width * 42/30, self.height*82/30))

    def display(self):

        SCREEN.blit(
            self.sprite_display[0], (self.left-self.width*0.5, self.top-self.height))
        SCREEN.blit(
            self.sprite_display[1], (self.left-self.width*0.18, self.top-self.height*2))
        super().display()


class GranaryPart(Building):
    def __init__(self, x, y, height, width, map, owner, mygranary):
        super().__init__(x, y, height, width, map, owner)
        self.granary = mygranary
        self.risk = self.granary.risk

    def display(self):
        super().display()


def test_pickle(xThing, lTested=[]):
    import pickle
    if id(xThing) in lTested:
        return lTested
    sType = type(xThing).__name__
    print('Testing {0}...'.format(sType))

    if sType in ['type', 'int', 'str']:
        print('...too easy')
        return lTested
    if sType == 'dict':
        print('...testing members')
        for k in xThing:
            lTested = test_pickle(xThing[k], lTested)
        print('...tested members')
        return lTested
    if sType == 'list':
        print('...testing members')
        for x in xThing:
            lTested = test_pickle(x)
        print('...tested members')
        return lTested

    lTested.append(id(xThing))
    oClass = type(xThing)

    for s in dir(xThing):
        if s.startswith('_'):
            print('...skipping *private* thingy')
            continue
        # if it is an attribute: Skip it
        try:
            xClassAttribute = oClass.__getattribute__(oClass, s)
        except AttributeError:
            pass
        else:
            if type(xClassAttribute).__name__ == 'property':
                print('...skipping property')
                continue

        xAttribute = xThing.__getattribute__(s)
        print('Testing {0}.{1} of type {2}'.format(
            sType, s, type(xAttribute).__name__))
        # if it is a function make sure it is stuck to the class...
        if type(xAttribute).__name__ == 'function':
            raise Exception('ERROR: found a function')
        if type(xAttribute).__name__ == 'method':
            print('...skipping method')
            continue
        if type(xAttribute).__name__ == 'HtmlElement':
            continue
        if type(xAttribute) == dict:
            print('...testing dict values for {0}.{1}'.format(sType, s))
            for k in xAttribute:
                lTested = test_pickle(xAttribute[k])
                continue
            print(
                '...finished testing dict values for {0}.{1}'.format(sType, s))

        try:
            oIter = xAttribute.__iter__()
        except AttributeError:
            pass
        except AssertionError:
            pass  # lxml elements do this
        else:
            print('...testing iter values for {0}.{1} of type {2}'.format(
                sType, s, type(xAttribute).__name__))
            for x in xAttribute:
                lTested = test_pickle(x, lTested)
            print(
                '...finished testing iter values for {0}.{1}'.format(sType, s))

        try:
            xAttribute.__dict__
        except AttributeError:
            pass
        else:
            # this attribute should be explored seperately...
            lTested = test_pickle(xAttribute, lTested)
            continue
        pickle.dumps(xAttribute)

    print('Testing {0} as complete object'.format(sType))
    pickle.dumps(xThing)
    return lTested
