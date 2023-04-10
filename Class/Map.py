from concurrent.futures import thread
import numpy as np
import math as m
import random as rd
import networkx as nx
import _thread as thread
import Class.Encoder as encode
import time
from Class.Cell import *
from Class.Wrapper import *
import p2p.socket_python as p2p
import json
import Class.Encoder as encoder
from Class.Button import Button

SCREEN = None


def set_SCREEN(screen):
    global SCREEN
    SCREEN = screen
    set_SCREEN_walker(screen)
    set_SCREEN_cell(screen)


sound_effect = {"extinguish": pygame.mixer.Sound("audio/water_bucket.wav"), "cooling": pygame.mixer.Sound("audio/cooling_fizz.wav"),
                "break": pygame.mixer.Sound("audio/break.wav")}

sound_effect["break"].set_volume(0.1)
sound_effect["cooling"].set_volume(0.1)
sound_effect["extinguish"].set_volume(0.1)


class Map:  # Un ensemble de cellule

    def __init__(self, size, height, width, username, load_map=False, wrapper=None, first_online=True):
        self.size = size  # La taille de la map est size*size : int
        self.height_land = height
        self.width_land = width
        self.button_activated = {"house": False, "shovel": False, "road": False,
                                 "prefecture": False, "engineerpost": False, "well": False, "farm": False, "granary": False, "ownership": False, "stop": False, "continue": False}
        self.players = ["Player1", "Player2", "Player3", "Player4"]
        # TO-DO request the num
        self.players_online = 1
        self.row_received = False
        self.row_received_2 = False
        WIDTH_SCREEN, HEIGHT_SCREEN = SCREEN.get_size()
        self.fps_font = pygame.font.Font(
            "GUI/Fonts/Title Screen/Berry Rotunda.ttf", 50)
        background = pygame.image.load(
            "game_screen/game_screen_sprites/loading_map.png")
        background = pygame.transform.scale(
            background, (SCREEN.get_width(), SCREEN.get_height()))
        if not first_online:
            text_loading = self.fps_font.render(
                f"Load map : {0}/{self.size}", 1, (0, 0, 0))
            SCREEN.blit(background, (0, 0))
            SCREEN.blit(text_loading, (WIDTH_SCREEN/2 - text_loading.get_width()/2,
                                       HEIGHT_SCREEN/2 - text_loading.get_height()/2))
            pygame.display.flip()
            wrapper = Wrapper(self, None)
            receive_num = False
            while not receive_num:
                data = p2p.get_data()
                if len(data) != 0:
                    if json.loads(data)["header"] == "responseJoin":
                        wrapper.wrap(data)
                        receive_num = True
        self.num_player = self.players_online
        # TO-DO put names in array and do function to fill it after init
        self.name_user = username
        self.players[self.num_player - 1] = username
        self.offset_top = 0
        self.offset_left = 0
        self.overlay = ""
        self.array = [[Empty(j, i, self.height_land, self.width_land, self, None) for i in range(
            size)] for j in range(size)]  # tableau de cellule (voir classe cellule) : list
        self.walkers = []
        self.migrantQueue = []
        self.laborAdvisorQueue = []
        self.buildings = []
        self.path_graph = nx.DiGraph()
        self.init_paths()
        if not first_online:
            print("In cell_init")
            if load_map:
                # Local version : reading from a file
                # f = open("map", 'r')
                # lines = f.readlines()
                # for line in lines:
                #     wrapper.wrap(line)

                # Online version : reading from the requests
                num_cell_init = 0
                while num_cell_init != self.size:
                    text_loading = self.fps_font.render(
                        f"Load map : {num_cell_init}/{self.size}", 1, (0, 0, 0))
                    # protocol to receive packet and if it's cell_init header, decode it
                    data = p2p.get_data()
                    if len(data) != 0:
                        try:
                            header = json.loads(data)["header"]
                            if header == "cell_init":
                                wrapper.wrap(data)
                                print("num_cell_init =", num_cell_init)
                                encoder.row_received(self.name_user, True)
                                num_cell_init += 1
                                SCREEN.blit(background, (0, 0))
                                SCREEN.blit(text_loading, (WIDTH_SCREEN/2 - text_loading.get_width()/2,
                                                           HEIGHT_SCREEN/2 - text_loading.get_height()/2))
                                pygame.display.flip()
                            else:
                                encoder.row_received(self.name_user, False)
                        except:
                            encoder.row_received(self.name_user, False)
        self.init_ownership()
        self.spawn_cells = [self.array[0][self.size//10],
                            self.array[0][self.size - self.size//10],
                            self.array[self.size -
                                       1][self.size - self.size//10],
                            self.array[self.size - 1][self.size//10]]
        self.governors = [Governor(self.spawn_cells[0], None),
                          Governor(self.spawn_cells[1], None),
                          Governor(self.spawn_cells[2], None),
                          Governor(self.spawn_cells[3], None)]
        # Replace 0 with the player number - 1
        self.spawn_cell = self.spawn_cells[self.num_player - 1]
        # Init a governor at spawn_cell
        # To-do spawn at the city-hall
        self.init_city_halls()
        self.governor = Governor(self.spawn_cell, username)
        self.governors[self.num_player - 1] = self.governor
        if not first_online:
            encode.governor(self.name_user, self.num_player,
                            self.governor.currentCell)
        self.wallet = 5000
        self.update_hover = 0
        self.zoom = 1
        self.zoom_coef = 1
        self.population = 0
        self.month_index = 0
        self.year = 150
        self.transaction = {"cells": [], "amount": 0, "Done": False}
        self.sound_effect = sound_effect

    def display_governors(self):
        for governor in self.governors:
            if governor.owner != None and governor.owner != self.name_user:
                governor.display()

    def set_spawn_point_governor(self):
        Governor.currentCell = self.spawn_cells[self.num_player - 1]

    def display_join_message(self, user, new_player):
        if self.name_user == user or self.name_user == new_player:
            print("In the return")
            return
        WIDTH_SCREEN, HEIGHT_SCREEN = SCREEN.get_size()
        background = pygame.image.load(
            "game_screen/game_screen_sprites/chat_background.jpg")
        new_player = Button(WIDTH_SCREEN/4, HEIGHT_SCREEN/3,
                            WIDTH_SCREEN/2, HEIGHT_SCREEN/3,
                            text=f"{new_player} just landed in the map. Waiting for him to load the map...",
                            image=background)
        new_player.draw(SCREEN)
        pygame.display.flip()
        done = False
        while not done:
            # Wait for the end_join protocol to arrive
            data = p2p.get_data()
            if len(data) != 0:
                try:
                    header = json.loads(data)["header"]
                    if header == "end_join":
                        done = True
                except:
                    pass

    def encode(self, user_confirmation):
        wrapper = Wrapper(self, None)
        WIDTH_SCREEN, HEIGHT_SCREEN = SCREEN.get_size()
        background = pygame.image.load(
            "game_screen/game_screen_sprites/chat_background.jpg")
        new_player = Button(WIDTH_SCREEN/4, HEIGHT_SCREEN/3,
                            WIDTH_SCREEN/2, HEIGHT_SCREEN/3,
                            text=f"{user_confirmation} just landed in the map. Loading : 0/75",
                            image=background)
        new_player.draw(SCREEN)
        pygame.display.flip()
        time.sleep(1)
        for x in range(self.size):
            new_player.draw(SCREEN)
            pygame.display.flip()
            row = []
            self.row_received = False
            response = False
            data_received = []
            self.row_received_2 = False
            for y in range(self.size):
                row.append(self.array[x][y].encode())
            encoder.cell_init_row(self.name_user, row, self.players_online)
            while not response:
                data = p2p.get_data()
                if len(data) != 0:
                    try:
                        data_received = json.loads(data)
                        if data_received["header"] == "row_received":
                            if data_received["username"] == user_confirmation:
                                wrapper.wrap(data)
                                if self.row_received:
                                    new_player.text = f"{user_confirmation} just landed in the map. Loading : {x}/{75}"
                                    new_player.draw(SCREEN)
                                    pygame.display.flip()
                                    response = True
                                else:
                                    encoder.cell_init_row(
                                        self.name_user, row, self.players_online)
                    except:
                        pass
        self.init_ownership(self.players_online)

    def add_transaction(self, cell):
        # if cell.owner == None:
        if cell not in self.transaction["cells"]:
            self.transaction["cells"].append(cell)
            self.transaction["amount"] += cell.price

    def reset_transaction(self):
        self.transaction["cells"] = []
        self.transaction["amount"] = 0
        self.transaction["Done"] = False

    def buy_cells(self):
        if self.check_valid_buy():
            for cell in self.transaction["cells"]:
                cell.owner = self.name_user
                self.wallet -= cell.price
                cell.price = cell.price * 2
                encoder.owner(self.name_user, cell, self.name_user)
            self.transaction["Done"] = True

        return self.transaction["Done"]

    def check_valid_buy(self):
        if self.transaction["amount"] <= self.wallet:
            for cell in self.transaction["cells"]:
                # if cell.owner == None or cell.owner == self.name_user:
                if cell.owner == None or (cell.owner != self.name_user and isinstance(cell, Empty)):
                    cell_around = cell.get_cells_around()
                    for i in cell_around:
                        if i.owner == self.name_user:
                            return True
        return False

    # Permet d'initialiser le chemin de terre sur la map.

    def init_paths(self):
        # Generate the init path of player 1 (top of the map)
        for x in range(self.size // 10):
            self.array[x][self.size // 10] = Path(
                x, self.size // 10, self.height_land, self.width_land, self, None)
            self.array[x][self.size // 10].handle_sprites()
        for y in range((self.size // 10) + 1):
            self.array[self.size // 10][y] = Path(
                self.size // 10, y, self.height_land, self.width_land, self, None)
            self.array[self.size // 10][y].handle_sprites()

        # Generate the init path of player 2 (left of the map)
        for x in range(self.size // 10):
            self.array[x][self.size - (self.size // 10)] = Path(
                x, self.size - (self.size // 10), self.height_land, self.width_land, self, None)
            self.array[x][self.size - (self.size // 10)].handle_sprites()
        for y in range((self.size // 10)):
            self.array[self.size // 10][(self.size - 1) - y] = Path(
                self.size // 10, (self.size - 1) - y, self.height_land, self.width_land, self, None)
            self.array[self.size // 10][(self.size - 1) - y].handle_sprites()

        # Generate the init path of player 3 (bottom of the map)
        for x in range(self.size - (self.size // 10), self.size):
            self.array[x][self.size - (self.size // 10)] = Path(
                x, self.size - (self.size // 10), self.height_land, self.width_land, self, None)
            self.array[x][self.size - (self.size // 10)].handle_sprites()
        for y in range((self.size // 10)):
            self.array[self.size - (self.size // 10)][(self.size - 1) - y] = Path(
                self.size - (self.size // 10), (self.size - 1) - y, self.height_land, self.width_land, self, None)
            self.array[self.size - (self.size // 10)
                       ][(self.size - 1) - y].handle_sprites()

        # Generate the init path of player 4 (right of the map)
        for x in range(self.size - (self.size // 10), self.size):
            self.array[x][self.size // 10] = Path(
                x, self.size // 10, self.height_land, self.width_land, self, None)
            self.array[x][self.size // 10].handle_sprites()
        for y in range((self.size // 10) + 1):
            self.array[self.size - (self.size // 10)][y] = Path(
                self.size - (self.size // 10), y, self.height_land, self.width_land, self, None)
            self.array[self.size - (self.size // 10)][y].handle_sprites()

        self.display_map()

    def init_ownership(self, players_online=0):
        if players_online != 0:
            num_player = self.num_player
            self.num_player = players_online
        if self.num_player == 1:
            for x in range(self.size // 10 + 1):
                for y in range(self.size // 10 + 1):
                    self.array[x][y].owner = self.players[self.num_player - 1]
        elif self.num_player == 2:
            for x in range(self.size // 10 + 1):
                for y in range(self.size - (self.size // 10), self.size):
                    self.array[x][y].owner = self.players[self.num_player - 1]
        elif self.num_player == 3:
            for x in range(self.size - (self.size // 10), self.size):
                for y in range(self.size - (self.size // 10), self.size):
                    self.array[x][y].owner = self.players[self.num_player - 1]
        elif self.num_player == 4:
            for x in range(self.size - (self.size // 10), self.size):
                for y in range(self.size // 10 + 1):
                    self.array[x][y].owner = self.players[self.num_player - 1]
        if players_online != 0:
            self.num_player = num_player

    def init_city_halls(self):
        self.array[self.size//10 - 1][self.size//10 - 1] = CityHall(
            self.size//10 - 1, self.size//10 - 1, self.height_land, self.width_land, self, self.players[1 - 1])
        self.array[self.size//10 - 1][self.size - (self.size//10 - 1)]
        self.array[self.size//10 - 1][self.size - (self.size//10 - 2)] = CityHall(
            self.size//10 - 1, self.size - (self.size//10 - 2), self.height_land, self.width_land, self, self.players[2 - 1])
        self.array[self.size - (self.size//10 - 2)][self.size - (self.size//10 - 2)] = CityHall(
            self.size - (self.size//10 - 2), self.size - (self.size//10 - 2), self.height_land, self.width_land, self, self.players[3 - 1])
        self.array[self.size - (self.size//10 - 2)][self.size//10 - 1] = CityHall(
            self.size - (self.size//10 - 2), self.size//10 - 1, self.height_land, self.width_land, self, self.players[4 - 1])

    def __str__(self):
        s = f"Map {self.size}*{self.size}\n"
        for j in range(self.size):
            for i in range(self.size):

                for k in self.walkers:
                    if k.currentCell == self.getCell(i, j):
                        s += f"{(str(self.getCell(i,j)) + ' ' + str(k)):^20}"
                        break
                else:
                    s += f"{str(self.getCell(i,j)):^20}"
            s += "\n"
        return s

    def center_camera_governor(self):
        # Center the scene into the cell where the governor is, it is a 2.5D game
        self.offset_left = (SCREEN.get_width()/2 - SCREEN.get_width()/12) + self.width_land*self.governor.currentCell.x/2 \
            - self.width_land*self.governor.currentCell.y/2 - SCREEN.get_width() / \
            2.25  # 2.25 because the panel take 1/4 of the screen so it needs to be centered
        self.offset_top = SCREEN.get_height()/2 - SCREEN.get_height()/6 - self.governor.currentCell.x*self.height_land/2 \
            - self.governor.currentCell.y*self.height_land/2
        self.init_screen_coordinates()

    def count_population(self):
        self.population = 0
        for b in self.buildings:
            if (isinstance(b, House)):
                self.population += b.nb_occupants

    def handle_button(self, button):
        self.button_activated = dict.fromkeys(self.button_activated, False)
        self.button_activated[button] = True

    def handle_esc(self):
        self.button_activated = dict.fromkeys(self.button_activated, False)

    def handle_zoom(self, zoom_in):
        if zoom_in:
            self.zoom_coef *= 1.05
            self.height_land *= 1.05
            self.width_land *= 1.05
        else:
            self.zoom_coef /= 1.05
            self.height_land /= 1.05
            self.width_land /= 1.05
        for x in range(self.size):
            for y in range(self.size):
                self.get_cell(x, y).handle_zoom(zoom_in)
        self.center_camera_governor()

    def init_screen_coordinates(self):
        for x in range(self.size):
            for y in range(self.size):
                self.get_cell(x, y).init_screen_coordonates()

    def handle_move(self, move, m):
        for x in range(self.size):
            for y in range(self.size):
                self.get_cell(x, y).handle_move(move, m)

    def inMap(self, x, y):
        return (0 <= x and x <= self.size-1 and 0 <= y and y <= self.size-1)

    def update_walkers(self):
        waitfornext = False

        def threading_update(i):
            nonlocal waitfornext
            if len(i.path) == 0:
                i.path_finding(i.currentCell, i.building)
            if len(i.path) != 0 and ((rd.randint(0, 9) == 9 and not waitfornext) or i.spawnCount == 20):
                self.walkers.append(i)
                self.migrantQueue.remove(i)
                SCREEN.blit(pygame.transform.scale(i.walker_sprites["top"],
                                                   (i.currentCell.width, i.currentCell.height)), (i.currentCell.left, i.currentCell.top))
                waitfornext = True
            elif i.spawnCount == 100:
                i.building.clear()
            else:
                i.spawnCount += 1

        if len(self.migrantQueue) != 0:
            for i in self.migrantQueue:
                thread.start_new_thread(threading_update, (i,))

        if len(self.laborAdvisorQueue) != 0:
            for i in self.laborAdvisorQueue:
                if any(house.nb_occupants != 0 for house in self.buildings if isinstance(house, House)):
                    i.leave_building()

        if self.players_online > 1 and len(self.walkers) > 0:
            walkerBuffer = encode.WalkerBuffer(self.name_user)
        for walker in self.walkers:
            if walker.owner == self.name_user:
                walker.move()
                if self.players_online > 1:
                    walkerBuffer.add("move", walker)
            else:
                self.walkers.remove(walker)

            # if self.get_overlay() not in ("fire", "collapse") and not isinstance(walker, Prefect) or (isinstance(walker, Prefect) and not walker.isWorking):
            #    walker.display()
            """if not isinstance(i, Migrant):
                if i.previousCell is not None:
                    i.previousCell.display()"""

        if self.players_online > 1 and len(self.walkers) > 0:
            walkerBuffer.send()

        for i in self.buildings:
            if i.risk and not i.risk.happened and i.owner == self.name_user:
                i.risk.riskIncrease()

    def display_walkers(self):
        for i in self.walkers:
            if self.get_overlay() not in ("fire", "collapse") and not isinstance(i, Prefect) or (isinstance(i, Prefect) and not i.isWorking):
                i.display()
            """if not isinstance(i, Migrant):
                if i.previousCell is not None:
                    i.previousCell.display()"""
            if isinstance(i, Prefect) and i.isWorking:
                i.extinguishFire(0)

    def update_fire(self):
        for i in self.buildings:
            if i.risk and i.risk.happened and i.risk.type == "fire":
                i.risk.burn()
                if self.players_online > 1 and i.owner == self.name_user:
                    encode.risk(self.name_user, "burn", i, i.risk.fireCounter)

    def update_collapse(self):
        for i in self.buildings:
            if i.risk and i.risk.happened and i.risk.type == "collapse":
                i.risk.collapse()
                if self.map.players_online > 1 and i.owner == self.map.name_user:
                    encode.risk(self.name_user, "collapse", i, None)

    def set_cell_array(self, x, y, cell):
        self.array[x][y] = cell
        self.array[x][y].display()

    def get_cell(self, x, y):
        if (x < 0 or x >= self.size) or (y < 0 or y >= self.size):
            return None
        return self.array[x][y]

    def display(self):
        pass

    def display_map(self):
        for i in range(self.size):
            for j in range(self.size):
                self.array[i][j].display()

    def get_overlay(self):
        return self.overlay

    def check_overlay(self, overlay):
        return self.overlay == overlay

    def set_overlay(self, overlay):
        if (self.overlay == overlay):
            self.overlay = ""
        else:
            self.overlay = overlay
        self.display_overlay()

    def display_overlay(self, pushed=1):
        match self.overlay:
            case "grid" | "water":
                for x in range(self.size):
                    for y in range(self.size):
                        self.array[x][y].display_overlay()

            case "fire" | "collapse":
                self.display_map()
                sorted_building = sorted(
                    self.buildings, key=lambda i: (i.x, i.y))
                for i in sorted_building:
                    i.display_overlay()

            case _:
                self.display_map()

    def update_farm(self):
        for i in self.buildings:
            if isinstance(i, Farm):
                if i.farmer.isWandering:
                    return
                i.crop_grow()

    def get_housed(self):
        return self.button_activated["house"]

    def get_shoveled(self):
        return self.button_activated["shovel"]

    def get_road_button_activated(self):
        return self.button_activated["road"]

    def get_prefectured(self):
        return self.button_activated["prefecture"]

    def get_engineered(self):
        return self.button_activated["engineerpost"]

    def get_welled(self):
        return self.button_activated["well"]

    def get_farmed(self):
        return self.button_activated["farm"]

    def get_granaried(self):
        return self.button_activated["granary"]

    def get_continued(self):
        return self.button_activated["continue"]

    def get_stopped(self):
        return self.button_activated["stop"]

    def get_ownershiped(self):
        return self.button_activated["ownership"]

    def get_height_land(self):
        return self.height_land

    def get_width_land(self):
        return self.width_land

    def get_name_user(self):
        return self.name_user
