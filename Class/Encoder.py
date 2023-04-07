import json

def send_data(data):
   json.dumps(data)

def join(username):
   send_data({"header": "join",
      "username": username
   })

def build(username, x, y, type):
   send_data({"header": "build",
      "username": username,
      "x": x,
      "y": y, 
      "type": type})

def levelup(username, x, y, level):
   send_data({"header": "levelup",
      "username": username,
      "x": x,
      "y": y, 
      "level": level})
   
def clear(username, x, y):
   send_data({"header": "clear",
      "username": username,
      "x": x,
      "y": y})
   
def chat(message) :
   send_data({"header" : "chat", 
      "message" : message})

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
