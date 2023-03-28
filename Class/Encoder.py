import json


def send_data(data):
   print(json.dumps(data))

def build(username, x, y, type):
   send_data({"header": "build",
      "username": username,
      "x": x,
      "y": y, 
      "type": type})

class WalkerBuffer:

   def __init__(self, username):
      self.buffer = {"header": "walker", "username": username, "array": []}

   def add(self, action, x, y, type):
      self.buffer["array"].append({
             "action": action,
             "x": x, "y": y,
             "type": type})
   
   def send(self):
      send_data(self.buffer)
      self.buffer = "walker;"
