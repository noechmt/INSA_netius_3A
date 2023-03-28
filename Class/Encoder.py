import json
from p2p.connect import send

def send_data(data):
   send(json.dumps(data))

def build(username, x, y, type):
   send_data({"header": "build",
      "username": username,
      "x": x,
      "y": y, 
      "type": type})

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
      send_data(self.buffer)
      self.buffer = {"header": "walker", "username": self.username, "array": []}
