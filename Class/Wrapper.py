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
        try:
            data = json.loads(data_json)
        except:
            return
        match data["header"]:
            case 'join':
                # Add here spawnpoints checker
                self.map.players_online += 1
                # Add the username to the list of players
                self.map.players[self.map.players_online - 1] = data["username"]
                encode.joinResponse(self.map.name_user,
                                    self.map.players_online,
                                    self.map.players)
                time.sleep(3)
                self.map.encode()
                print(self.map.players)
            case 'responseJoin':
                self.map.players_online = data["players_online"]
                self.map.players = data["players"]
            case 'build':
                self.map.get_cell(data["x"], data["y"]).build(
                    data["type"], data["username"], True)
                self.map.get_cell(data["x"], data["y"]).owner = data["username"]
            case 'clear':
                self.map.get_cell(data["x"], data["y"]).clear(data["username"])
                self.map.get_cell(data["x"], data["y"]).owner = data["username"]
            case 'levelup':
                self.map.get_cell(data["x"], data["y"]).nextLevel()
                self.map.get_cell(data["x"], data["y"]).owner = data["username"]
                assert (self.map.get_cell(
                    data["x"], data["y"]).level == data["level"])
            case 'risk':
                if data["type"] == "fire":
                    self.map.get_cell(
                        data["building"][0], data["building"][1]).risk.happened = True
                    self.map.get_cell(
                        data["building"][0], data["building"][1]).risk.fireCounter = data["fireCounter"]
                elif data["type"] == "collapse":
                    self.map.get_cell(
                        data["building"][0], data["building"][1]).risk.happened = True
                elif data["type"] == "burnt":
                    self.map.get_cell(
                        data["building"][0], data["building"][1]).risk.fireCounter = data["fireCounter"]
                    self.map.get_cell(
                        data["building"][0], data["building"][1]).burn()
            case 'extinguish':
                walker_ghost = self.map.get_cell(data["building"][0], data["building"][1]).prefect
                walker_ghost.cell_assignement(self.map.get_cell(data["currentCell"][0], data["currentCell"][1]))
                walker_ghost.isWorking = True
                # walker_ghost.extinguishCounter = data["extinguishCounter"]
                # walker_ghost.waterCounter = data["waterCounter"]
                # walker_ghost.extinguishFire()

            case 'walker':
                for walker in data["array"]:
                    building = self.map.get_cell(walker["building"][0], walker["building"][1])
                    if walker["action"] == "move":
                        match walker["type"]:
                            case "Migrant":
                                if building.migrant == None:
                                    walker_ghost = Walker.Migrant(building, data["username"])
                                    building.migrant = walker_ghost
                                    self.map.walkers.append(walker_ghost)
                                building.migrant.cell_assignement(self.map.get_cell(walker["currentCell"][0], walker["currentCell"][1]))
                            case "Labor Advisor":
                                if building.labor_advisor == None:
                                    walker_ghost = Walker.LaborAdvisor(building, data["username"])
                                    building.labor_advisor = walker_ghost
                                    self.map.walkers.append(walker_ghost)
                                walker_ghost.inBuilding = False
                                building.labor_advisor.cell_assignement(self.map.get_cell(walker["currentCell"][0], walker["currentCell"][1]))
                            case "Prefect":
                                if building.prefect == None:
                                    walker_ghost = Walker.Prefect(building, data["username"])
                                    building.prefect = walker_ghost
                                    self.map.walkers.append(walker_ghost)
                                walker_ghost.inBuilding = False
                                building.prefect.cell_assignement(self.map.get_cell(walker["currentCell"][0], walker["currentCell"][1]))
                            case "Engineer":
                                if building.engineer == None:
                                    walker_ghost = Walker.Engineer(building, data["username"])
                                    building.engineer = walker_ghost
                                    self.map.walkers.append(walker_ghost)
                                walker_ghost.inBuilding = False
                                building.engineer.cell_assignement(self.map.get_cell(walker["currentCell"][0], walker["currentCell"][1]))
                    
                    elif walker["action"] == "enter":
                        match walker["type"]:
                            case 'Migrant':
                                building.migrant.enter_building()
                                print("Le migrant est entré dans la maison")
                            case 'Labor Advisor':
                                building.labor_advisor.enter_building()
                            case 'Prefect':
                                building.prefect.enter_building()
                            case 'Engineer':
                                building.engineer.enter_building()

            case 'chat':
                self.panel.chat.history_append(data['message'])

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
            case 'row_received':
                self.map.row_received = data["received"]
            case 'row_received_2':
                self.map.row_received_2 = data["received"]
            case 'owner':
                self.map.get_cell(data["x"], data["y"]).owner = data["owner"]
                if (self.map.get_cell(data["x"], data["y"]).owner != data["owner"]):
                    self.map.get_cell(data["x"], data["y"]).owner = data["owner"]
            case 'governor':
                if self.map.governors[data["num_player"] - 1].owner == None:
                    encode.governor(self.map.name_user, self.map.num_player, self.map.governor.currentCell)
                self.map.governors[data["num_player"] - 1].owner = data["username"]
                self.map.governors[data["num_player"] - 1].previousCell = self.map.governors[data["num_player"] - 1].currentCell
                self.map.governors[data["num_player"] - 1].currentCell = self.map.get_cell(data["x"], data["y"])
                self.map.governors[data["num_player"] - 1].display()
