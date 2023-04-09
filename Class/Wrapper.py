import json
from this import d

import Class.Walker as Walker

#TODO
#Protocole d'apparition sur la map :
#Quand un joueur se connecte il demande aux autres s'ils sont là et en fonction du nombre de réponses
#un point de spawn est attribué

class Wrapper:
   
   def __init__(self, map, panel):
      self.map = map
      self.panel = panel

   def wrap(self, data_json):
      try : data = json.loads(data_json)
      except: return
      match data["header"]:
         case 'join':
            #Add here spawnpoints checker
            pass
         case 'build':
            self.map.get_cell(data["x"], data["y"]).build(data["type"], data["username"])
         case 'clear':
            self.map.get_cell(data["x"], data["y"]).clear()
         case 'levelup':
            self.map.get_cell(data["x"], data["y"]).nextLevel()
            assert(self.map.get_cell(data["x"], data["y"]).level == data["level"])
         case 'walker':
            for walker in data["array"]:
               if walker["action"] == "move":
                  match walker["type"]:
                     case "Migrant":
                        walker_ghost = Walker.Migrant(walker["building"], data["username"])
                     case "Labor Advisor":
                        walker_ghost = Walker.LaborAdvisor(walker["building"], data["username"])
                     case "Prefect":
                        walker_ghost = Walker.Prefect(walker["building"], data["username"])
                     case "Engineer":
                        walker_ghost = Walker.Engineer(walker["building"], data["username"])
                  
                  walker_ghost.currentCell = self.map.get_cell(walker["currentCell"][0], walker["currentCell"][1])
                  walker_ghost.previousCell = self.map.get_cell(walker["previousCell"][0], walker["previousCell"][1])
                  self.map.walkers.append(walker_ghost)

         case 'chat' : 
            self.panel.chat.history_append(data['message'])

         case 'duel_request' :
            if self.panel.duel.player_name == data['username'] and self.panel.duel.duel_request == 0:
               self.panel.duel.request += 1

         case 'duel_answer' :
            self.panel.duel.duel_accepted = data['accept']

         case 'update_round' :
            self.panel.duel.enemy_game_round += 1
            self.panel.duel.enemy_score = data['score']