import json
import p2p.socket_python as p2p

def encodeJSON(data):
   p2p.Client.sendData(json.dumps(data))
   # p2p.send_data(json.dumps(data))

def join(username):
   encodeJSON({"header": "join",
      "username": username
   })

def joinResponse(username, players_online):
   encodeJSON({"header": "responseJoin",
      "username": username,
      "players_online": players_online
   })

def build(username, x, y, type):
   encodeJSON({"header": "build",
      "username": username,
      "x": x,
      "y": y, 
      "type": type})

def levelup(username, cell, level):
   encodeJSON({"header": "levelup",
      "username": username,
      "x": cell.x,
      "y": cell.y, 
      "level": level})
   
def clear(username, cell):
   encodeJSON({"header": "clear",
      "username": username,
      "x": cell.x,
      "y": cell.y})
   
def risk(username, type, building, fireCounter):
   encodeJSON({"header": type,
      "username": username,
      "building": (building.x, building.y),
      "fireCounter": fireCounter
   })
   
def chat(message) :
   encodeJSON({"header" : "chat", 
      "message" : message})

class WalkerBuffer:  

   def __init__(self, username):
      self.username = username
      self.buffer = {"header": "walker", "username": username, "array": []}

   def add(self, action, walker):
      self.buffer["array"].append({
             "action": action,
             "building": (walker.building.x, walker.building.y),
             "currentCell": (walker.currentCell.x, walker.currentCell.y) if walker.currentCell != None else None,
             "previousCell": (walker.previousCell.x, walker.previousCell.y) if walker.previousCell != None else None,
             "type": str(walker)})
   
   def send(self):
      encodeJSON(self.buffer)
      self.buffer = {"header": "walker", "username": self.username, "array": []}
