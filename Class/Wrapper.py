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
                encode.joinResponse(self.map.name_user,
                                    self.map.players_online)
                time.sleep(3)
                self.map.encode()
            case 'responseJoin':
                self.map.players_online = data["players_online"]
            case 'build':
                self.map.get_cell(data["x"], data["y"]).build(
                    data["type"], data["username"])
            case 'clear':
                self.map.get_cell(data["x"], data["y"]).clear()
            case 'levelup':
                self.map.get_cell(data["x"], data["y"]).nextLevel()
                assert (self.map.get_cell(
                    data["x"], data["y"]).level == data["level"])
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
                if data["type"] == "path" or data["type"] == "house" or data["type"] == "well" \
                        or data["type"] == "prefecture" or data["type"] == "engineer post" \
                        or data["type"] == "farm" or data["type"] == "granary":
                    self.map.get_cell(data["x"], data["y"]).build(
                        data["type"], data["owner"], True)
                if data["type_empty"] != "":
                    self.map.get_cell(
                        data["x"], data["y"]).type_empty = data["type_empty"]
                    self.map.get_cell(
                        data["x"], data["y"]).type_sprite = data["type_empty"]
                    self.map.get_cell(
                        data["x"], data["y"]).init_random_sprites()
                self.map.get_cell(
                    data["x"], data["y"]).owner = data["owner"]
                print(data["x"], data["y"], data["type"],
                      data["type_empty"], data["owner"])
