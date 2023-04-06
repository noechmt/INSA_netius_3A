import json
from this import d

import Class.Walker as Walker

#TODO
#Protocole d'apparition sur la map :
#Quand un joueur se connecte il demande aux autres s'ils sont là et en fonction du nombre de réponses
#un point de spawn est attribué

class Wrapper:
   
   def __init__(self, map):
      self.map = map

   def wrap(self, data_json):
      print(data_json)
      data = json.loads(data_json)
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
                        walker_ghost = Walker.Migrant(None, data["username"])
                     case "Labor Advisor":
                        walker_ghost = Walker.LaborAdvisor(None, data["username"])
                     case "Prefect":
                        walker_ghost = Walker.Prefect(None, data["username"])
                     case "Engineer":
                        walker_ghost = Walker.Engineer(None, data["username"])
                  
                  walker_ghost.currentCell = self.map.get_cell(walker["currentCell"][0], walker["currentCell"][1])
                  walker_ghost.previousCell = self.map.get_cell(walker["previousCell"][0], walker["previousCell"][1])
                  self.map.walkers.append(walker_ghost)
