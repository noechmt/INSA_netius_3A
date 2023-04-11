import json
import p2p.socket_python as p2p


def encodeJSON(data):
    print("Sending :" + str(len(json.dumps(data))) + " bytes")
    p2p.send_data(json.dumps(data))


def join(username):
    encodeJSON({"header": "join",
                "username": username
                })


def joinResponse(username, players_online, players):
    encodeJSON({"header": "responseJoin",
                "username": username,
                "players_online": players_online,
                "players" : players
                })


def cell_init_single(x, y, type, type_empty, owner):
    return {"x": x,
            "y": y,
            "type": type,
            "type_empty": type_empty,
            "owner": owner}


def cell_init_row(username, row):
    encodeJSON({"header": "cell_init",
                "username": username,
                "row": row})


def row_received(username, received):
    encodeJSON({"header": "row_received",
                "username": username,
                "received": received})


def row_received_2(username, received):
    encodeJSON({"header": "row_received_2",
                "username": username,
                "received": received})


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


def chat(message):
    encodeJSON({"header": "chat",
                "message": message})

def owner(username, cell, owner):
    encodeJSON({"header": "owner",
                "username": username,
                "x": cell.x,
                "y": cell.y,
                "owner": owner})

def governor(username, num_player, cell):
    encodeJSON({"header": "governor",
                "username": username,
                "num_player": num_player,
                "x": cell.x,
                "y": cell.y})

   
def chat(message) :
   encodeJSON({"header" : "chat", 
      "message" : message})
   
def pchat(message, username) :
   encodeJSON({"header" : "pchat", 
      "message" : message,
      "username" : username})
   
def duel_request(username, my_name) :
   encodeJSON({"header" : "duel_request",
      "username" : username,
      "my_name" : my_name})

def duel_answer(answer,username) : 
   encodeJSON({"header" : "duel_answer", 
      "accept" : answer,
      "username" : username}) # 1 accept or 2 decline
   
def update_round(score) :
   encodeJSON({"header" : "update_round", 
      "score" : score})

def finish_duel() :
   encodeJSON({"header" : "finish_duel"})

def send_bet(value) : 
    encodeJSON({"header" : "send_bet",
        "value" : value})


def quit(Username) : 
    encodeJSON({"header":"quit","username":Username})



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
        self.buffer = {"header": "walker",
                       "username": self.username, "array": []}
