import json
import p2p.socket_python as p2p

def encodeJSON(data):
   p2p.send_data(json.dumps(data))

def join(username):
   encodeJSON({"header": "join",
      "username": username
   })

def build(username, x, y, type):
   encodeJSON({"header": "build",
      "username": username,
      "x": x,
      "y": y, 
      "type": type})

def levelup(username, x, y, level):
   encodeJSON({"header": "levelup",
      "username": username,
      "x": x,
      "y": y, 
      "level": level})
   
def clear(username, x, y):
   encodeJSON({"header": "clear",
      "username": username,
      "x": x,
      "y": y})

class WalkerBuffer:

   def __init__(self, username):
      self.username = username
      self.buffer = {"header": "walker", "username": username, "array": []}

   def add(self, action, currentCell, previousCell, type):
      self.buffer["array"].append({
             "action": action,
             "currentCell": currentCell,
             "previousCell": previousCell,
             "type": type})
   
   def send(self):
      encodeJSON(self.buffer)
      self.buffer = {"header": "walker", "username": self.username, "array": []}
