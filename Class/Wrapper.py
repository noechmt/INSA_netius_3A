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
            case 'clear':
                self.map.get_cell(data["x"], data["y"]).clear()
            case 'levelup':
                self.map.get_cell(data["x"], data["y"]).nextLevel()
                assert (self.map.get_cell(
                    data["x"], data["y"]).level == data["level"])
            case 'risk':
                if data["type"] == "burn":
                    self.map.get_cell(
                        data["building"][0], data["building"][0]).risk.burn()
                    self.map.get_cell(
                        data["building"][0], data["building"][0]).risk.fireCounter = data["fireCounter"]
                else:
                    self.map.get_cell(
                        data["building"][0], data["building"][0]).risk.collapse()
            case 'walker':
                for walker in data["array"]:
                    if walker["action"] == "move":
                        match walker["type"]:
                            case "Migrant":
                                walker_ghost = Walker.Migrant(self.map.get_cell(
                                    walker["building"][0], walker["building"][1]), data["username"])
                            case "Labor Advisor":
                                walker_ghost = Walker.LaborAdvisor(self.map.get_cell(
                                    walker["building"][0], walker["building"][1]), data["username"])
                            case "Prefect":
                                walker_ghost = Walker.Prefect(self.map.get_cell(
                                    walker["building"][0], walker["building"][1]), data["username"])
                            case "Engineer":
                                walker_ghost = Walker.Engineer(self.map.get_cell(
                                    walker["building"][0], walker["building"][1]), data["username"])

                        walker_ghost.currentCell = self.map.get_cell(
                            walker["currentCell"][0], walker["currentCell"][1])
                        walker_ghost.previousCell = self.map.get_cell(
                            walker["previousCell"][0], walker["previousCell"][1])
                        self.map.walkers.append(walker_ghost)

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
