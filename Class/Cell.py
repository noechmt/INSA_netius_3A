from email.policy import default
from Class.Walker import *
from Class.RiskEvent import *
import pygame
from random import *
from math import sqrt, floor
import random
import time

SCREEN = None


def set_SCREEN_cell(screen):
    global SCREEN
    SCREEN = screen


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

    def __init__(self, x, y, height, width, screen, map):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.map = map
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

    def update_sprite_size(self):
        pass

    def isBuildable(self):
        return isinstance(self, Empty) and self.type_empty == "dirt"

    def init_screen_coordonates(self):
        # Compute the x and y screen position of the cell
        self.left = (self.WIDTH_SCREEN/2 - self.WIDTH_SCREEN/12) + \
            self.width*self.x/2 - self.width*self.y/2 - self.map.offset_left
        self.top = self.HEIGHT_SCREEN/6 + self.x * \
            self.height/2 + self.y * self.height/2 + self.map.offset_top

    def display(self):
        pass

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
        else:
            draw_polygon_alpha(SCREEN, (0, 0, 0, 85),
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
        path = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if abs(i) != abs(j) and self.map.inMap(self.x + i, self.y + j):
                    if isinstance(self.map.get_cell(self.x + i, self.y + j), type):
                        path.append(self.map.get_cell(self.x + i, self.y + j))
        return path

    def build(self, type):
        if isinstance(self, Empty) and self.type_empty != "dirt":
            print("This cell is already taken")
        else:
            match type:
                case "path":
                    self.map.set_cell_array(self.x, self.y, Path(
                        self.x, self.y, self.height, self.width, SCREEN, self.map))
                    self.map.get_cell(self.x, self.y).handle_sprites()
                    self.map.get_cell(self.x, self.y).display()
                    self.map.wallet -= 4
                case "house":
                    self.map.set_cell_array(self.x, self.y, House(
                        self.x, self.y, self.height, self.width, SCREEN, self.map))
                    self.map.wallet -= 10
                case "well":
                    self.map.set_cell_array(self.x, self.y, Well(
                        self.x, self.y, self.height, self.width, SCREEN, self.map))
                    self.map.wallet -= 5
                case "prefecture":
                    self.map.set_cell_array(self.x, self.y, Prefecture(
                        self.x, self.y, self.height, self.width, SCREEN, self.map))
                    self.map.wallet -= 30
                case "engineer post":
                    self.map.set_cell_array(self.x, self.y, EngineerPost(
                        self.x, self.y, self.height, self.width, SCREEN, self.map))
                    self.map.wallet -= 30
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
        if not isinstance(self, Empty) and self.type_empty != "rock" and self.type_empty != "water":
            if isinstance(self, Building):
                self.map.buildings.remove(self)
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
            self.map.set_cell_array(self.x, self.y, Empty(
                self.x, self.y, self.height, self.width, SCREEN, self.map, "dirt", 1))
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

    def __init__(self, x, y, height, width, screen, map, path_level=0):
        super().__init__(x, y, height, width, screen, map)
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

    def update_sprite_size(self):
        self.sprite_display = pygame.transform.scale(
            self.sprite, (self.width+2*sqrt(2), self.height+2))

    def display(self):
        SCREEN.blit(self.sprite_display, (self.left-sqrt(2), self.top-1))
        self.display_overlay()

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
    def __init__(self, x, y, height, width, screen, map, type_empty="dirt", boolean_first_generation=0):
        super().__init__(x, y, height, width, screen, map)
        self.type_empty = type_empty  # "dirt", "trees"
        self.type = "empty"
        self.tree_or_dirt_list = ["tree", "dirt", "dirt"]
        self.rock_or_dirt_list = ["rock", "dirt", "dirt", "dirt"]
        self.path_sprite = ""

        if boolean_first_generation == 0:
            # place the trees
            self.type_empty = random.choice(self.tree_or_dirt_list)
            if self.type_empty == "tree":
                self.type_sprite = "tree"
                self.type = "empty_tree"
            else:
                self.type_sprite = "dirt"

            # place the rocks
            if ((27 < x < 36 and 12 < y < 16) or (27 < x < 31 and 15 < y < 23) or (x > 30 and y > 25) or (x > 35 and y < 5) or (x > 35 and y > 30)):
                self.type_empty = random.choice(self.rock_or_dirt_list)
                if self.type_empty == "rock":
                    self.type_sprite = "rock"
                    self.type = "empty_rock"
                else:
                    self.type_sprite = "dirt"

        # place the water with conditions for sprites
            # river at the top
                # line under the first river
            if (y == x+10 and x < 5) or (y == x+14 and 5 < x < 8) or (y == x+15 and 8 < x < 13) or (y == x+18 and 14 < x < 17) or (y == x+20 and 17 < x < 20):
                self.type_sprite = "watersiderightD"
                self.type_empty = "water"
            elif (y == x+11 and x < 5) or (y == x+15 and 4 < x < 8) or (y == x+16 and (7 < x < 13)) or (x, y) == (13, 31) or (y == x+19 and 13 < x < 17) or (y == x+21 and 16 < x < 19):
                self.type_sprite = "watersiderightW"
                self.type_empty = "water"
            elif (x, y) == (5, 15) or (x, y) == (8, 22) or (x, y) == (13, 28) or (x, y) == (14, 31) or (x, y) == (17, 35):
                self.type_sprite = "watersidecornerA"
                self.type_empty = "water"
            elif ((x, y) == (5, x) and 15 < x < 20) or (x, y) == (8, 23) or (x, y) == (13, 29) or (x, y) == (13, 30) or (x, y) == (14, 32) or (x, y) == (17, 36) or (x, y) == (17, 37):
                self.type_sprite = "watersideunder"
                self.type_empty = "water"

            # line behind the first river
            elif (y == x+19 and x < 10) or (y == x+26 and 9 < x < 14):
                self.type_sprite = "watersideleftW"
                self.type_empty = "water"
            elif (y == x+20 and x < 9) or (y == x+27 and 8 < x < 13):
                self.type_sprite = "watersideleftD"
                self.type_empty = "water"
            elif (x == 9 and 28 < y < 36):
                self.type_sprite = "watersideupper"
                self.type_empty = "water"

            elif ((x == y+31 and y < 5) or (x == y+28 and 8 < y < 12)):
                self.type_sprite = "watersiderightD"
                self.type_empty = "water"
            elif ((x == y+30 and y < 6) or (x == y+27 and 8 < y < 13)):
                self.type_sprite = "watersiderightW"
                self.type_empty = "water"
            elif (x, y) == (36, 5):
                self.type_sprite = "watersidecornerA"
                self.type_empty = "water"
            elif ((x == 5 and 15 < y < 20) or (x == 36 and 5 < y < 9)):
                self.type_sprite = "watersideunder"
                self.type_empty = "water"

            # line behind the second river
            elif ((x == y+24 and 8 < y < 16) or (x == y+27 and y < 6)):
                self.type_sprite = "watersideleftD"
                self.type_empty = "water"
            elif ((x == y+25 and 8 < y < 15) or (x == y+28 and y < 6)):
                self.type_sprite = "watersideleftW"
                self.type_empty = "water"
            elif ((x == 33 and 5 < y < 9)):
                self.type_sprite = "watersideupper"
                self.type_empty = "water"

            # full water in the second river
            elif ((x == y+26 and 7 < y < 14) or (x == y+27 and 6 < y < 9) or (x == y+28 and 5 < y < 9) or (x == y+29 and y < 7)):
                self.type_sprite = "water"
                self.type_empty = "water"

            # full water in the first river
            if ((x < 5 and 11+x < y < 19+x) or (4 < x < 8 and 15+x < y < 19+x) or (7 < x < 10 and 16+x < y < 19+x) or (9 < x < 13 and 16+x < y < 26+x)
                    or (x == 13 and 18+x < y < 26+x) or (13 < x < 17 and 19+x < y < 26+x) or (x == 17 and y == 39)):
                self.type_sprite = "water"
                self.type_empty = "water"
        else:
            self.type_sprite = "dirt"

        # select the sprites randomly
        if (self.type_empty == "rock") or (self.type_empty == "tree"):
            aleatoire = randint(1, 4)
        elif (self.type_empty == "dirt"):
            aleatoire = randint(1, 13)
        else:
            aleatoire = randint(1, 2)
        super().set_aleatoire(aleatoire)
        self.path_sprite = "game_screen/game_screen_sprites/" + \
            self.type_sprite + "_" + str(aleatoire) + ".png"
        self.sprite = pygame.image.load(self.path_sprite).convert_alpha()
        self.sprite_display = ""
        self.update_sprite_size()
        self.display()

    def __str__(self):
        return self.type_empty

    def update_sprite_size(self):
        if self.type_empty == "tree":
            if self.aleatoire == 1:
                self.sprite_display = pygame.transform.scale(
                    self.sprite, (self.width, self.height*42/30))
            elif self.aleatoire == 2:
                self.sprite_display = pygame.transform.scale(
                    self.sprite, (self.width, self.height*41/30))
            elif self.aleatoire == 3:
                self.sprite_display = pygame.transform.scale(
                    self.sprite, (self.width, self.height*44/30))
            elif self.aleatoire == 4:
                self.sprite_display = pygame.transform.scale(
                    self.sprite, (self.width, self.height*45/30))
        elif self.type_empty == "rock":
            self.sprite_display = pygame.transform.scale(
                self.sprite, (self.width, self.height*35/30))
        else:
            self.sprite_display = pygame.transform.scale(
                self.sprite, (self.width+2*sqrt(2), self.height+2))

    def display(self):
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
        elif self.type_empty == "rock":
            SCREEN.blit(
                self.sprite_display, (self.left, self.top-self.height*5/30))
        else:
            SCREEN.blit(self.sprite_display,
                        (self.left-sqrt(2), self.top-1))
        self.display_overlay()

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
        # To-do display around

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
    def __init__(self, x, y, height, width, screen, my_map):
        super().__init__(x, y, height, width, screen, my_map)
        self.map.buildings.append(self)
        self.destroyed = False
        path_around = self.check_cell_around(Path)
        house_around = self.check_cell_around(House)
        self.path_sprite = ""
        for j in path_around:
            self.map.path_graph.add_edge(j, self)
            self.map.path_graph.add_edge(self, j, weight=2000)
            if isinstance(self, House) and len(house_around) != 0:
                for k in house_around:
                    self.map.path_graph.add_edge(j, k, weight=2000)

    def destroy(self):
        self.destroyed = 1


class House(Building):  # la maison fils de building (?)
    def __init__(self, x, y, height, width, screen, my_map, level=0, nb_occupants=0):
        super().__init__(x, y, height, width, screen, my_map)
        self.level = level  # niveau de la maison : int
        self.nb_occupants = nb_occupants  # nombre d'occupants: int
        # nombre max d'occupant (dépend du niveau de la maison) : int
        self.max_occupants = 5
        self.unemployedCount = 0
        self.migrant = Migrant(self)
        # test_pickle(self.migrant)
        self.risk = RiskEvent("fire", self)
        # Temporary
        self.path_sprite = "game_screen/game_screen_sprites/house_" + \
            str(self.level) + ".png"
        self.sprite = pygame.image.load(self.path_sprite).convert_alpha()
        self.sprite_display = ""
        self.update_sprite_size()
        self.type = "house"
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

    def nextLevel(self):
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
    def __init__(self, x, y, height, width, screen, my_map):
        super().__init__(x, y, height, width, screen, my_map)
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
    def __init__(self, x, y, height, width, screen, my_map):
        super().__init__(x, y, height, width, screen, my_map)
        self.labor_advisor = LaborAdvisor(self)
        self.employees = 0
        self.prefect = Prefect(self)
        self.requiredEmployees = 5
        self.risk = RiskEvent("collapse", self)
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
    def __init__(self, x, y, height, width, screen, my_map):
        super().__init__(x, y, height, width, screen, my_map)
        self.labor_advisor = LaborAdvisor(self)
        self.employees = 0
        self.engineer = Engineer(self)
        self.requiredEmployees = 5
        self.risk = RiskEvent("fire", self)
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
