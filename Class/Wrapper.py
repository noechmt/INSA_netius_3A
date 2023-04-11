import json
from this import d

import Class.Cell as Cell
import Class.Walker as Walker
import Class.Encoder as encode
import time

# TODO
# Protocole d'apparition sur la map :
# Quand un joueur se connecte il demande aux autres s'ils sont là et en fonction du nombre de réponses
# un point de spawn est attribué


class Wrapper:

    def __init__(self, map, panel):
        self.map = map
        self.panel = panel

    def wrap(self, data_json):
        if len(data_json) == 0:
            return
        try:
            data = json.loads(data_json)
        except:
            encode.row_received(self.map.name_user, False)
            return
        match data["header"]:
            case 'join':
                # Add here spawnpoints checker
                self.map.players_online += 1
                # Add the username to the list of players
                self.map.players[self.map.players_online -
                                 1] = data["username"]
                encode.joinResponse(self.map.name_user,
                                    self.map.players_online,
                                    self.map.players)
                time.sleep(1)
                encode.join_start(self.map.name_user, data["username"])
                self.map.encode(data["username"])
                encode.end_join(self.map.name_user)
                print(self.map.players)
            case 'start_join':
                self.map.display_join_message(
                    data["username"], data["new_player"])
            case 'responseJoin':
                self.map.players_online = data["players_online"]
                self.map.players = data["players"]
            case 'build':
                self.map.get_cell(data["x"], data["y"]).build(
                    data["type"], data["username"], True)
                self.map.get_cell(data["x"], data["y"]
                                  ).owner = data["username"]
            case 'clear':
                for cell in data["row"]:
                    self.map.get_cell(cell["x"], cell["y"]).clear(
                        data["username"])
                    self.map.get_cell(cell["x"], cell["y"]
                                      ).owner = data["username"]
                encode.row_received(self.map.name_user, True)
            case 'levelup':
                self.map.get_cell(data["x"], data["y"]).nextLevel()
                self.map.get_cell(data["x"], data["y"]
                                  ).owner = data["username"]
                assert (self.map.get_cell(
                    data["x"], data["y"]).level == data["level"])
            case 'risk':
                if data["type"] == "fire":
                    building = self.map.get_cell(
                        data["building"][0], data["building"][1])
                    building.risk.happened = True
                    building.risk.fireCounter = data["fireCounter"]
                    if isinstance(building, Cell.EngineerPost):
                        if building.labor_advisor in building.map.walkers:
                            building.labor_advisor.currentCell.display()
                            building.map.walkers.remove(
                                building.labor_advisor)
                        else:
                            building.engineer.currentCell.display()
                            if building.engineer in building.map.walkers:
                                building.map.walkers.remove(
                                    building.engineer)
                elif data["type"] == "collapse":
                    building = self.map.get_cell(
                        data["building"][0], data["building"][1])
                    building.risk.happened = True
                    if isinstance(building, Cell.Prefecture):
                        if building.labor_advisor in building.map.walkers:
                            building.labor_advisor.currentCell.display()
                            building.map.walkers.remove(
                                building.labor_advisor)
                        else:
                            building.prefect.currentCell.display()
                            if building.prefect in building.map.walkers:
                                building.map.walkers.remove(building.prefect)
                elif data["type"] == "burnt":
                    self.map.get_cell(
                        data["building"][0], data["building"][1]).risk.fireCounter = data["fireCounter"]
                    self.map.get_cell(
                        data["building"][0], data["building"][1]).burn()
            case 'extinguish':
                walker_ghost = self.map.get_cell(
                    data["building"][0], data["building"][1]).prefect
                walker_ghost.cell_assignement(self.map.get_cell(
                    data["currentCell"][0], data["currentCell"][1]))
                walker_ghost.isWorking = True
                # walker_ghost.extinguishCounter = data["extinguishCounter"]
                # walker_ghost.waterCounter = data["waterCounter"]
                # walker_ghost.extinguishFire()

            case 'walker':
                for walker in data["array"]:
                    building = self.map.get_cell(
                        walker["building"][0], walker["building"][1])
                    if walker["action"] == "move":
                        match walker["type"]:
                            case "Migrant":
                                if building.migrant == None:
                                    walker_ghost = Walker.Migrant(
                                        building, data["username"])
                                    building.migrant = walker_ghost
                                    self.map.walkers.append(walker_ghost)
                                building.migrant.cell_assignement(self.map.get_cell(
                                    walker["currentCell"][0], walker["currentCell"][1]))
                            case "Labor Advisor":
                                if building.labor_advisor == None:
                                    walker_ghost = Walker.LaborAdvisor(
                                        building, data["username"])
                                    building.labor_advisor = walker_ghost
                                    self.map.walkers.append(walker_ghost)
                                building.labor_advisor.inBuilding = False
                                building.labor_advisor.cell_assignement(self.map.get_cell(
                                    walker["currentCell"][0], walker["currentCell"][1]))
                            case "Prefect":
                                if building.prefect == None:
                                    walker_ghost = Walker.Prefect(
                                        building, data["username"])
                                    building.prefect = walker_ghost
                                    self.map.walkers.append(walker_ghost)
                                building.prefect.inBuilding = False
                                building.prefect.cell_assignement(self.map.get_cell(
                                    walker["currentCell"][0], walker["currentCell"][1]))
                            case "Engineer":
                                if building.engineer == None:
                                    walker_ghost = Walker.Engineer(
                                        building, data["username"])
                                    building.engineer = walker_ghost
                                    self.map.walkers.append(walker_ghost)
                                building.engineer.inBuilding = False
                                building.engineer.cell_assignement(self.map.get_cell(
                                    walker["currentCell"][0], walker["currentCell"][1]))

                    elif walker["action"] == "enter":
                        match walker["type"]:
                            case 'Migrant':
                                building.migrant.enter_building()
                            case 'Labor Advisor':
                                building.labor_advisor.enter_building()
                            case 'Prefect':
                                building.prefect.enter_building()
                            case 'Engineer':
                                building.engineer.enter_building()

            case 'chat':
                self.panel.chat.history_append(data['message'])

            case 'pchat':
                if self.map.name_user == data['username']:
                    self.panel.chat.history_append(data['message'])

            case 'duel_request':
                if self.panel.duel.player_name == data['username'] and self.panel.duel.duel_request == 0:
                    self.panel.duel.enemy_name = data['my_name']
                    print("afezafzafazaf", self.panel.duel.enemy_name)
                    self.panel.duel.duel_request += 1

            case 'duel_answer':
                if data['username'] == self.panel.duel.player_name:
                    self.panel.duel.duel_accepted = data['accept']
                    # self.panel.duel.enemy_name = data['username']
                    self.panel.duelON = True
                    self.map.wallet -= self.panel.duel.bet

            case 'update_round':
                if self.panel.duel.duel_round > self.panel.duel.enemy_game_round:
                    self.panel.duel.enemy_game_round += 1
                self.panel.duel.enemy_score = data['score']

            case 'finish_duel':
                self.panel.duel.enemy_bet_stopped = True

            case 'send_bet':
                self.panel.duel.bet = data['value']

            case 'cell_init':
                for cell in data["row"]:
                    if cell["type"] == "path" or cell["type"] == "house" or cell["type"] == "well" \
                            or cell["type"] == "prefecture" or cell["type"] == "engineer post" \
                            or cell["type"] == "farm" or cell["type"] == "granary":
                        self.map.get_cell(cell["x"], cell["y"]).build(
                            cell["type"], cell["owner"], True)
                    if cell["type_empty"] != "":
                        self.map.get_cell(
                            cell["x"], cell["y"]).type_empty = cell["type_empty"]
                        self.map.get_cell(
                            cell["x"], cell["y"]).type_sprite = cell["type_empty"]
                        self.map.get_cell(
                            cell["x"], cell["y"]).init_random_sprites()
                    self.map.get_cell(
                        cell["x"], cell["y"]).owner = cell["owner"]
                    if isinstance(self.map.get_cell(cell["x"], cell["y"]), Cell.House):
                        for i in range(cell["level"]):
                            self.map.get_cell(cell["x"], cell["y"]).nextLevel()
            case 'row_received':
                self.map.row_received = data["received"]
            case 'row_received_2':
                self.map.row_received_2 = data["received"]
            case 'owner':
                for cell in data["row"]:
                    self.map.get_cell(
                        cell["x"], cell["y"]).owner = cell["owner"]
                    self.map.get_cell(cell["x"], cell["y"]).price = self.map.get_cell(
                        cell["x"], cell["y"]).price * 2
                    if (self.map.get_cell(cell["x"], cell["y"]).owner != cell["owner"]):
                        self.map.get_cell(
                            cell["x"], cell["y"]).owner = cell["owner"]
                encode.row_received(self.map.name_user, True)
            case 'governor':
                if self.map.governors[data["num_player"] - 1].owner == None:
                    encode.governor(
                        self.map.name_user, self.map.num_player, self.map.governor.currentCell)
                self.map.governors[data["num_player"] -
                                   1].owner = data["username"]
                self.map.governors[data["num_player"] -
                                   1].previousCell = self.map.governors[data["num_player"] - 1].currentCell
                self.map.governors[data["num_player"] -
                                   1].currentCell = self.map.get_cell(data["x"], data["y"])
                self.map.governors[data["num_player"] - 1].display()

            case 'pillage':
                if self.map.name_user == data['username']:
                    Cell.Granary.pillaged = True
                    Cell.Granary.pillager = data['player']

            case 'gain_stack':
                if self.map.name_user == data['username']:
                    Cell.Granary.stack += 1

            case 'crop_state':
                for i in self.map.buildings:
                    if isinstance(i, Cell.Crop) and i.x == data['x'] and i.y == data['y']:
                        self.map.get_cell(
                            data['x'], data['y']).grow_state = data['state']

            case 'quit':
                self.map.players_online -= 1
                print("Player on line = ", self.map.players_online)
