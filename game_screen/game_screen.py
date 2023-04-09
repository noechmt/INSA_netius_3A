from select import select
from tabnanny import check
import pygame
import pickle
from math import sqrt
import numpy as np
from Class.Button import Button
from Class.Map import *
from Class.Panel import Panel
from Class.Wrapper import Wrapper
import p2p.socket_python as p2p
import time
from datetime import datetime
from Class.Encoder import *

def myMap(message) : 
    return [*map(str,message.split())]

# draw a rectangle with an opacity option
def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


def game_screen():
    pygame.init()

    SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    set_SCREEN(SCREEN)
    FPS = 60

    # Re-initialize the window
    SCREEN.fill((0, 0, 0))

    pygame.mixer.init()
    pygame.mixer.music.load("audio/tunic_ost.wav")
    pygame.mixer.music.play(-1)
    # print(pygame.mixer.music.get_volume())
    pygame.mixer.music.set_volume(0.05)

    pygame.display.set_caption("Netius")
    WIDTH_SCREEN, HEIGH_SCREEN = SCREEN.get_size()
    height_land = HEIGH_SCREEN/45
    width_land = WIDTH_SCREEN*sqrt(2)/60
    SIZE = 75

    # Load new map or existing one with pickle
    file = open("Saves/temp.txt", "r")
    name_path = file.read()
    if "Saves/" in name_path:
        with open(name_path, 'rb') as f1:
            map = pickle.load(f1)
        map.display_map()
    else:
        map = Map(SIZE, height_land, width_land, name_path)
        # map.array[33][33] = Farm(33, 33, height_land, width_land, SCREEN, map)
        # map.array[37][37] = Crop(37, 37, height_land, width_land, SCREEN, map, map.array[33][33])
        # print(map.array[33][33])
        # print(map.array[34][34])

    panel = Panel(SCREEN)
    panel.duel.player_name = map.name_user
    wrapper = Wrapper(map, panel)
    #wrapper.wrap('{"header": "build", "username": "Governor", "x": 5, "y": 5, "type": "house"}')
    #wrapper.wrap('{"header": "walker", "username": "Governor", "array": [{"action": "move", "currentCell": [7, 5], "previousCell": [7, 4], "type": "Migrant"}]}')

    # Dims without left panel
    height_wo_panel = HEIGH_SCREEN
    width_wo_panel = WIDTH_SCREEN - (WIDTH_SCREEN/9)

    fps_font = pygame.font.Font("GUI/Fonts/Title Screen/Berry Rotunda.ttf", 14)
    run = 1
    clock = pygame.time.Clock()

    speeds = [0.000000001, 0.4, 0.6, 0.8, 1, 1.25, 1.5, 2, 3, 5]
    speed_index = 4
    speed = speeds[speed_index]
    speed_left = 186.5*WIDTH_SCREEN/192
    speed_top = 0.25*HEIGH_SCREEN+12.5*HEIGH_SCREEN/80
    speed_counter_text = fps_font.render(
        f"{speed * 100:.0f}%", 1, (255, 255, 255))
    SCREEN.blit(speed_counter_text, (speed_left, speed_top))
    paused = 0

    selection = {"is_active": 0, "start": tuple, "cells": []}
    hovered_cell = None
    zoom = 0.8
    move = 1
    zoom_update = 0
    move_update = 0
    fire_update_count = 0
    governor_movements = 0

    count_day = 0
    count_month = map.month_index
    day = 1
    months = ["Jan", "Fev", "Mar", "Avr", "Mai", "Juin",
              "Juil", "Aout", "Sept", "Oct", "Nov", "Dec"]
    month = months[count_month]
    year = map.year

    walker_update_count = 0
    governor_update_count = 0
    fire_upadte_count = 0
    farm_update_count = 0
    current_time = ""
    text_last_save = fps_font.render("None", 1, (255, 255, 255))
    rf = fps_font.render(f"rf", 1, (255, 255, 255))
    pf = fps_font.render(f"pf", 1, (255, 255, 255))
    rn = fps_font.render(f"rn", 1, (255, 255, 255))
    pn = fps_font.render(f"pn", 1, (255, 255, 255))
    ##############################

    map.center_camera_governor()

    while run:
        pos = pygame.mouse.get_pos()

        update_speed = 10 / (speed)

        wrapper.wrap(p2p.get_data())

        fire_update_count += 1
        if fire_update_count >= update_speed:
            map.update_fire()
            map.update_collapse()
            fire_update_count = 0

        SCREEN.fill((0, 0, 0))
        map.display_map()

        # Get position of the mouse in the map
        x = round(((pos[1]-map.offset_top-HEIGH_SCREEN/6)/map.height_land - (
            WIDTH_SCREEN/2-WIDTH_SCREEN/12-pos[0]-map.offset_left)/map.width_land))-1
        y = round(((WIDTH_SCREEN/2-WIDTH_SCREEN/12-pos[0]-map.offset_left)/map.width_land + (
            pos[1]-map.offset_top-HEIGH_SCREEN/6)/map.height_land))

        move_update += 1
        move_coeff = 6
        if move_update % 6 == 0:
            # If mouse is in the top of the screen, we move the map to the top
            if pos[1] <= 60 and map.offset_top <= 0:
                map.offset_top += 5*(3 - pos[1] / 20)/(zoom/move_coeff)
                map.handle_move("up", (3 - pos[1] / 20)/(zoom/move_coeff))
            if pos[1] >= HEIGH_SCREEN - 60 and map.offset_top >= -map.get_cell(0, 0).height * SIZE + HEIGH_SCREEN / 1.25:
                map.offset_top -= 5 * \
                    (3 - (HEIGH_SCREEN - pos[1]) / 20)/(zoom/move_coeff)
                map.handle_move(
                    "down", (3 - (HEIGH_SCREEN - pos[1]) / 20) / (zoom/move_coeff))
            if pos[0] <= 60 and map.offset_left >= (-map.get_cell(0, 0).width * SIZE / 2) + (WIDTH_SCREEN / 2) / 1.25:
                map.offset_left -= 5*(3 - pos[0] / 20)/(zoom/move_coeff)
                map.handle_move("left", (3 - pos[0] / 20)/(zoom/move_coeff))
            if pos[0] >= WIDTH_SCREEN - 60 and map.offset_left <= (map.get_cell(0, 0).width * SIZE / 2) - (WIDTH_SCREEN / 2) / 1.25:
                if not panel.get_road_button().is_hovered(pos) and not panel.get_well_button().is_hovered(pos):
                    if not panel.get_collapse_button().is_hovered(pos) and not panel.get_exit_button().is_hovered(pos):
                        if not panel.get_governor_button().is_hovered(pos):
                            map.offset_left += 5 * \
                                (3 - (WIDTH_SCREEN - pos[0]
                                      ) / 20)/(zoom/move_coeff)
                            map.handle_move(
                                "right", (3 - (WIDTH_SCREEN - pos[0]) / 20) / (zoom/move_coeff))
            move_update = 0

         # If the mouse is in the map, we display the hovered cell(s)
        if selection["is_active"]:
            for i in selection["cells"]:
                map.get_cell(i[0], i[1]).handle_hover_button()
        else:
            if map.inMap(x, y) and pos[0] < width_wo_panel:
                map.get_cell(x, y).handle_hover_button()

        zoom_update += 1
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if governor_movements == True:
                        if map.inMap(x, y):
                            map.governor.set_pathfinding(map.get_cell(x, y))
                    elif map.inMap(x, y) and not selection["is_active"] and pos[0] < width_wo_panel:
                        selection["start"] = (x, y)
                        selection["cells"].append((x, y))
                        selection["is_active"] = 1

                    if (panel.get_governor_button().is_hovered(pos)):
                        # panel.set_window("none")
                        map.handle_esc()
                        governor_movements = not governor_movements
                        panel.set_governor_sprite(governor_movements)
                    if not governor_movements and not panel.chatON and not panel.duelON:
                        if (panel.get_grid_button().is_hovered(pos)):
                            map.set_overlay("grid")
                        if panel.get_fire_button().is_hovered(pos):
                            map.set_overlay("fire")
                        if panel.get_collapse_button().is_hovered(pos):
                            map.set_overlay("collapse")
                        if (panel.house_button.is_hovered(pos)):
                            panel.set_window("house")
                            map.handle_button("house")
                            map.set_overlay("")
                        if (panel.shovel_button.is_hovered(pos)):
                            panel.set_window("shovel")
                            map.handle_button("shovel")
                            map.set_overlay("")
                        if (panel.get_road_button().is_hovered(pos)):
                            panel.set_window("road")
                            map.handle_button("road")
                            map.set_overlay("")
                        if (panel.prefecture_button.is_hovered(pos)):
                            panel.set_window("prefecture")
                            map.handle_button("prefecture")
                            map.set_overlay("")
                        if (panel.engineerpost_button.is_hovered(pos)):
                            panel.set_window("engineer post")
                            map.handle_button("engineerpost")
                            map.set_overlay("")
                        if (panel.well_button.is_hovered(pos)):
                            panel.set_window("well")
                            map.handle_button("well")
                            map.set_overlay("water")

                        if (panel.farm_button.is_hovered(pos)):
                            panel.set_window("farm")
                            map.handle_button("farm")

                            # map.display_map()
                        if (panel.granary_button.is_hovered(pos)):
                            panel.set_window("granary")
                            map.handle_button("granary")

                  
                    if panel.duelON and panel.duel.duel_accepted == 1 :
                        if panel.continue_button.is_hovered((pos)) :
                            map.handle_button("continue")

                                                      
                        if panel.stop_button.is_hovered((pos)) :
                            map.handle_button("stop")
                            
                        if map.get_continued() :
                            panel.duel.continue_bet()
                            update_round(panel.duel.my_score)
                            if panel.duel.my_bet_stopped : finish_duel()

                            # print(panel.duel.my_score)
                        if map.get_stopped() :
                            panel.duel.stop_bet()
                            finish_duel()

                    if (panel.up_button.is_hovered(pos)):
                        if speed_index < 9:
                            speed_index += 1
                            speed = speeds[speed_index]
                            panel.set_played_button()

                    if (panel.down_button.is_hovered(pos)):
                        if (speed_index > 1):
                            speed_index -= 1
                            speed = speeds[speed_index]
                            panel.set_played_button()

                    if (panel.get_pause_button().is_hovered(pos)):
                        if paused == 0:
                            paused = 1
                            speed = speeds[0]
                            panel.set_paused_button()

                        else:
                            paused = 0
                            speed = speeds[speed_index]
                            panel.set_played_button()

                    if (panel.get_save_button().is_hovered(pos)):
                        map.month_index = count_month
                        map.year = year
                        path_save = "Saves/" + \
                            str(map.get_name_user()) + ".q5"
                        with open(path_save, 'wb') as f1:
                            pickle.dump(map, f1)
                        current_time = datetime.now().strftime("%H:%M")
                        text_last_save = fps_font.render(
                            current_time, 1, (255, 255, 255))
                    if panel.get_exit_button().is_hovered(pos):
                        run = False

                if zoom_update > 0 and not panel.chatON:
                    if event.button == 4:
                        if zoom < 1.4:
                            zoom += 0.05
                            map.handle_zoom(1)

                    if event.button == 5:
                        if zoom > 0.6:
                            zoom -= 0.05
                            map.handle_zoom(0)

                    zoom_update = 0

            if event.type == pygame.MOUSEBUTTONUP:
                if selection["is_active"]:
                    for i in selection["cells"]:
                        selected_cell = map.get_cell(i[0], i[1])
                        if map.get_shoveled():
                            selected_cell.clear()
                        elif map.get_housed() and selected_cell.isBuildable():
                            selected_cell.build("house")
                        elif map.get_road_button_activated() and selected_cell.isBuildable():
                            selected_cell.build("path")
                        elif map.get_prefectured() and selected_cell.isBuildable():
                            selected_cell.build("prefecture")
                        elif map.get_engineered() and selected_cell.isBuildable():
                            selected_cell.build("engineer post")
                        elif map.get_farmed() and selected_cell.isBuildable("Farm"):
                            selected_cell.build("farm")
                        elif map.get_granaried() and selected_cell.isBuildable("Granary"):
                            selected_cell.build("granary")
                        elif map.get_welled() and selected_cell.isBuildable():
                            selected_cell.build("well")
                            for k in range(-2, 3):
                                for j in range(-2, 3):
                                    if (39 >= x+k >= 0 and 39 >= y+j >= 0):
                                        map.get_cell(i[0]+k, i[1]+j).display()

                        else:
                            selected_cell.display()

                    


                    # map.buildings.sort(key=lambda i: (i.x, i.y))
                    # print([(i.x, i.y) for i in map.buildings])
                    selection["cells"].clear()
                    selection["is_active"] = 0

            if event.type == pygame.MOUSEMOTION:
                # Display previous cell without hover
                if hovered_cell:
                    hovered_cell = map.get_cell(
                        hovered_coordinates[0], hovered_coordinates[1])
                    hovered_cell.display()
                if map.inMap(x, y) and pos[0] <= width_wo_panel and not selection["is_active"]:
                    hovered_coordinates = (x, y)
                    hovered_cell = map.get_cell(
                        hovered_coordinates[0], hovered_coordinates[1])
                    hovered_cell.handle_hover_button()

                # Selection : fill the set with hovered cell
                if map.inMap(x, y) and selection["is_active"]:
                    selection["cells"].sort()
                    # print([(i.x, i.y) for i in map.buildings])
                    for i in selection["cells"]:
                        map.get_cell(i[0], i[1]).display()
                    selection["cells"].clear()
                    range_x = range(
                        selection["start"][0], x+1, 1) if selection["start"][0] <= x else range(selection["start"][0], x-1, -1)
                    range_y = range(
                        selection["start"][1], y+1, 1) if selection["start"][1] <= y else range(selection["start"][1], y-1, -1)
                    for i in range_x:
                        for j in range_y:
                            selection["cells"].append((i, j))
                            map.get_cell(i, j).handle_hover_button()

                panel.get_grid_button().handle_hover_button(pos, SCREEN)
                panel.get_home_button().handle_hover_button(pos, SCREEN)
                panel.get_shovel_button().handle_hover_button(pos, SCREEN)
                panel.get_road_button().handle_hover_button(pos, SCREEN)
                panel.get_prefecture_button().handle_hover_button(pos, SCREEN)
                panel.get_engineerpost_button().handle_hover_button(pos, SCREEN)
                panel.get_well_button().handle_hover_button(pos, SCREEN)
                panel.get_farm_button().handle_hover_button(pos, SCREEN)
                panel.get_granary_button().handle_hover_button(pos, SCREEN)
                panel.get_up_button().handle_hover_button(pos, SCREEN)
                panel.get_down_button().handle_hover_button(pos, SCREEN)
                panel.get_pause_button().handle_hover_button(pos, SCREEN)
                panel.get_save_button().handle_hover_button(pos, SCREEN)
                panel.get_fire_button().handle_hover_button(pos, SCREEN)
                panel.get_collapse_button().handle_hover_button(pos, SCREEN)
                panel.get_exit_button().handle_hover_button(pos, SCREEN)
                panel.get_governor_button().handle_hover_button(pos, SCREEN)

            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    panel.set_window("none")
                    map.handle_esc()
                    governor_movements = False
                    panel.chatON = False
                    panel.set_governor_sprite(governor_movements)

                if pygame.key.get_pressed()[pygame.K_r]:
                    Prefect.risk_reset = not Prefect.risk_reset

                # if pygame.key.get_pressed()[pygame.K_p]:
                #     volume = pygame.mixer.music.get_volume()
                #     pygame.mixer.music.set_volume(volume + 0.05)
                #     for i in map.sound_effect:
                #         volume = map.sound_effect[i].get_volume()
                #         map.sound_effect[i].set_volume(volume + 0.05)

                # if pygame.key.get_pressed()[pygame.K_m]:
                #     volume = pygame.mixer.music.get_volume()
                #     pygame.mixer.music.set_volume(volume - 0.05)
                #     for i in map.sound_effect:
                #         volume = map.sound_effect[i].get_volume()
                #         map.sound_effect[i].set_volume(volume - 0.05)

                if pygame.key.get_pressed()[pygame.K_e] and panel.duelON :
                    panel.duel.continue_bet_enemy_proto()

                if pygame.key.get_pressed()[pygame.K_s] and panel.duelON :
                    panel.duel.stop_bet_enemy_proto()

                if pygame.key.get_pressed()[pygame.K_t] and not panel.duelON:

                    panel.chatON = True
                    panel.set_window("chat")

                    # print([panel.chat.message_history[i].text for i in range(len(panel.chat.message_history))])

            if panel.chatON :
                panel.chat.input.handle_event(event, SCREEN, True)

                ######## chat messages #########
                if panel.chat.input.message_to_send != '' and panel.chat.input.message_to_send[0] != '/' :
                    message = map.get_name_user() + " : " + panel.chat.input.message_to_send
                    panel.chat.history_append(message)
                    panel.chat.input.message_to_send = ''
                    chat(message)
                

                ######## chat commands #########        
                if (panel.chat.input.message_to_send != '' and panel.chat.input.message_to_send[0] == '/') :
                    # print(map.players)
                    command = myMap(panel.chat.input.message_to_send)

                    if (command != [] and command[0] == '/duel') : 
                        
                        # if command != [] and len(command) >=2 and """command[1] not in map.players""" : 
                        #     panel.chat.history_append("Player does not exist")
                        #     panel.chat.input.message_to_send = ''
                        if command != [] and len(command) >=2 and """command[1] in map.players""" :
                            duel_request(command[1]) #send a duel request
                            panel.duelON = True
                            panel.chat.input.message_to_send = ''
                            pchat(map.name_user + " veut te tabasser le fiac dans un duel de gambling !",command[1])

                    if (command != [] and command[0] == '/accept') and panel.duel.duel_request > 0:
                        duel_answer(1) #send confirmation for duel
                        panel.duelON = True
                        panel.duel.duel_accepted = 1
                        panel.chat.input.message_to_send = ''

                    if (command != [] and command[0] == '/decline') and panel.duel.duel_request > 0:
                        duel_answer(2) #send refusal for duel
                        panel.chat.input.message_to_send = ''

                        

                panel.chat.handle_history_scroll(event)
                 # print(panel.chat.history_index)

        

        if panel.duelON :
            panel.chatON = False

            if panel.duel.duel_accepted == 2  : 
                print("aloooo")
                panel.duelON = False
                panel.duel.init_duel()

            if panel.duel.duel_accepted == 1 :

                panel.duel.handle_duel_round()
                if panel.duel.handle_winner() :
                    panel.duel.init_duel()
                    panel.duelON = False

            


            







        # if event.type == pygame.MOUSEBUTTONDON:
        #     print(event.button)

        if map.get_overlay() in ("fire", "collapse"):
            map.display_overlay()

        # fire_upadte_count += 1
        # if fire_upadte_count >= update_speed:
        #     map.update_fire()
        #     map.update_collapse()
        #     fire_upadte_count = 0

        walker_update_count += 1
        governor_update_count += 1
        if walker_update_count >= update_speed // 2:
            # print(walker_update_count)
            map.update_walkers()
            speed_counter_text = fps_font.render(
                f"{speed * 100:.0f}%", 1, (255, 255, 255))
            SCREEN.blit(speed_counter_text,
                        (speed_left, speed_top))
            # print("break")
            walker_update_count = 0

        if governor_update_count >= update_speed // 4:
            if map.governor.move():
                map.center_camera_governor()
            governor_update_count = 0

        farm_update_count += 1
        if farm_update_count >= update_speed * 1.5:
            map.update_farm()
            farm_update_count = 0

        if not isinstance(map.governor.currentCell, Building):
            map.governor.display()
        map.display_walkers()
        panel.display()

        # Speed display
        speed_counter_text = fps_font.render(
            f"{speed * 100:.0f}%", 1, (255, 255, 255))
        SCREEN.blit(speed_counter_text,
                    (speed_left, speed_top))
        # Name display
        fps = (int)(clock.get_fps())
        text_name = fps_font.render(
            "Name : ", 1, (255, 255, 255))
        SCREEN.blit(text_name, (WIDTH_SCREEN - WIDTH_SCREEN /
                    13, HEIGH_SCREEN - HEIGH_SCREEN/1.93))
        texte_governor = fps_font.render(
            str(map.get_name_user()), 1, (255, 255, 255))
        SCREEN.blit(texte_governor, (WIDTH_SCREEN - WIDTH_SCREEN /
                    13 + WIDTH_SCREEN / 200, HEIGH_SCREEN - HEIGH_SCREEN/1.93 + 1.5*text_name.get_size()[1]))
        # Money display
        text_wallet = fps_font.render(
            f"Money : {map.wallet}", 1, (255, 255, 255))
        SCREEN.blit(text_wallet, (WIDTH_SCREEN - WIDTH_SCREEN /
                    13, HEIGH_SCREEN - HEIGH_SCREEN/2.2))
        # Population display
        map.count_population()
        text_population = fps_font.render(
            f"Citizens : {map.population}", 1, (255, 255, 255))
        SCREEN.blit(text_population, (WIDTH_SCREEN - WIDTH_SCREEN /
                    13, HEIGH_SCREEN - HEIGH_SCREEN/2.5))
        # Date display
        count_day += 1
        if (count_day > (15 / speed)):
            day += 1
            if day > 30:
                day = 1
                count_month += 1
                if (count_month > 11):
                    count_month = 0
                    year += 1
                month = months[count_month]
            count_day = 0
        text_date = fps_font.render(
            f"Date : {month} {year}", 1, (255, 255, 255))
        SCREEN.blit(text_date, (WIDTH_SCREEN - WIDTH_SCREEN /
                    13, HEIGH_SCREEN - HEIGH_SCREEN/2.8))
        # Save text display
        text_save = fps_font.render(f"Save :", 1, (255, 255, 255))
        SCREEN.blit(text_save, (WIDTH_SCREEN - WIDTH_SCREEN /
                    13 + WIDTH_SCREEN / 28, HEIGH_SCREEN - HEIGH_SCREEN/3.2))
        SCREEN.blit(text_last_save, (WIDTH_SCREEN - WIDTH_SCREEN /
                    13 + WIDTH_SCREEN / 28, HEIGH_SCREEN - HEIGH_SCREEN/3.4))
        # Coordonates display
        text_click = fps_font.render(f"x : {x}, y : {y}", 1, (255, 255, 255))
        SCREEN.blit(text_click, (WIDTH_SCREEN - WIDTH_SCREEN /
                    13, HEIGH_SCREEN - HEIGH_SCREEN/6.5))
        # FPS display
        fps = (int)(clock.get_fps())
        text_fps = fps_font.render("fps : " + str(fps), 1, (255, 255, 255))
        SCREEN.blit(text_fps, (WIDTH_SCREEN - WIDTH_SCREEN /
                    13, HEIGH_SCREEN - HEIGH_SCREEN/7.5))
        # ????
        #if RiskEvent.riskTreshold == 1_000_000 : SCREEN.blit(rf, (0, 60))
        if not Prefect.risk_reset:
            SCREEN.blit(pf, (WIDTH_SCREEN - WIDTH_SCREEN /
                             13 + WIDTH_SCREEN / 16, HEIGH_SCREEN - HEIGH_SCREEN/8.3))
        #if RiskEvent.riskTreshold == 200 : SCREEN.blit(rn, (0, 60))
        if Prefect.risk_reset:
            SCREEN.blit(pn, (WIDTH_SCREEN - WIDTH_SCREEN /
                             13 + WIDTH_SCREEN / 16, HEIGH_SCREEN - HEIGH_SCREEN/8.3))

        clock.tick(FPS)
        pygame.display.flip()
