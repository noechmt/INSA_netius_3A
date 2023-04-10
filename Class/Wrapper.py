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
                self.map.players[self.map.players_online -
                                 1] = data["username"]
                encode.joinResponse(self.map.name_user,
                                    self.map.players_online,
                                    self.map.players)
                time.sleep(3)
                self.map.encode(data["username"])
                print(self.map.players)
            case 'responseJoin':
                self.map.players_online = data["players_online"]
                self.map.players = data["players"]
            case 'build':
                self.map.get_cell(data["x"], data["y"]).build(
                    data["type"], data["username"], True)
                self.map.get_cell(data["x"], data["y"]
                                  ).owner = data["username"]
            case 'clear':
                self.map.get_cell(data["x"], data["y"]).clear()
                self.map.get_cell(data["x"], data["y"]
                                  ).owner = data["username"]
            case 'levelup':
                self.map.get_cell(data["x"], data["y"]).nextLevel()
                self.map.get_cell(data["x"], data["y"]
                                  ).owner = data["username"]
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
                    self.panel.duel.enemy_name = data['username']
                    self.panel.duelON = True

            case 'update_round':
                self.panel.duel.enemy_game_round += 1
                self.panel.duel.enemy_score = data['score']

            case 'finish_duel':
                self.panel.duel.enemy_bet_stopped = True

            case 'send_bet':
                self.panel.duel.bet = data['value']
                self.map.wallet -= self.panel.duel.bet

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
                self.map.get_cell(data["x"], data["y"]).price = self.map.get_cell(
                    data["x"], data["y"]).price * 2
                if (self.map.get_cell(data["x"], data["y"]).owner != data["owner"]):
                    self.map.get_cell(
                        data["x"], data["y"]).owner = data["owner"]
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
