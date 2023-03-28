import json
from this import d


class Wrapper:
   
   def __init__(self, map):
      self.map = map

   def wrap(self, data_json):
      print(data_json)
      data = json.loads(data_json)
      match data["header"]:
         case 'build':
            self.map.get_cell(data["x"], data["y"]).build(data["type"], data["username"])
         case 'walker':
            pass