import json
import p2p.socket_python as p2p
import time


def encodeJSON(data):
    print("Sending :" + str(len(json.dumps(data))) + " bytes")
    if data["header"] != "cell_init" and data["header"] != "row_received":
        for i in range(3):
            time.sleep(0.01)
            p2p.send_data(json.dumps(data))
    else:
        p2p.send_data(json.dumps(data))


def join(username):
    encodeJSON({"header": "join",
                "username": username
                })


def joinResponse(username, players_online, players):
    encodeJSON({"header": "responseJoin",
                "username": username,
                "players_online": players_online,
                "players": players
                })


def join_start(username, new_player):
    encodeJSON({"header": "start_join",
                "username": username,
                "new_player": new_player})


def end_join(username):
    encodeJSON({"header": "end_join",
                "username": username})


def cell_init_single(x, y, type, type_empty, owner, level):
    return ({"x": x,
            "y": y,
             "type": type,
             "type_empty": type_empty,
             "owner": owner,
             "level": level})


def cell_init_row(username, row, num_online):
    if num_online > 2:
        time.sleep(0.35)
    encodeJSON({"header": "cell_init",
                "username": username,
                "row": row})


def row_received(username, received):
    encodeJSON({"header": "row_received",
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


def clear(username, row):
    encodeJSON({"header": "clear",
                "username": username,
                "row": row})


def clear_single(cell):
    return ({"x": cell[0],
            "y": cell[1]})


def risk(username, type, building, fireCounter):
    encodeJSON({"header": "risk",
                "username": username,
                "type": type,
                "building": (building.x, building.y),
                "fireCounter": fireCounter
                })


def extinguish(username, building, currentCell, extinguishCounter, waterCounter):
    encodeJSON({"header": "extinguish",
                "username": username,
                "building": (building.x, building.y),
                "currentCell": (currentCell.x, currentCell.y),
                "extinguishCounter": extinguishCounter,
                "waterCounter": waterCounter
                })


def chat(message):
    encodeJSON({"header": "chat",
                "message": message})


def owner(username, row):
    encodeJSON({"header": "owner",
                "username": username,
                "row": row})


def owner_single(cell, owner):
    return ({"x": cell.x,
            "y": cell.y,
             "owner": owner})


def governor(username, num_player, cell):
    encodeJSON({"header": "governor",
                "username": username,
                "num_player": num_player,
                "x": cell.x,
                "y": cell.y})


def chat(message):
    encodeJSON({"header": "chat",
                "message": message})


def pchat(message, username):
    encodeJSON({"header": "pchat",
                "message": message,
                "username": username})


def duel_request(username, my_name):
    encodeJSON({"header": "duel_request",
                "username": username,
                "my_name": my_name})


def duel_answer(answer, username):
    encodeJSON({"header": "duel_answer",
                "accept": answer,
                "username": username})  # 1 accept or 2 decline


def update_round(score):
    encodeJSON({"header": "update_round",
                "score": score})


def finish_duel():
    encodeJSON({"header": "finish_duel"})


def send_bet(value):
    encodeJSON({"header": "send_bet",
                "value": value})


def pillage(username, player):
    encodeJSON({"header": "pillage",
                "username": username,
                "player": player})


def quit(Username):
    encodeJSON({"header": "quit", "username": Username})


def crop_state(x, y, state):
    encodeJSON({"header": "cropt_state",
                "x": x,
                "y": y,
                "state": state})


def gain_stack(username):
    encodeJSON({"header": "gain_stack",

                "username": username})


class WalkerBuffer:

    username = None
    buffer = {"header": "walker", "username": username, "array": []}

    def __init__(self, username):
        WalkerBuffer.username = username
        WalkerBuffer.buffer = {"header": "walker",
                               "username": username, "array": []}

    def add(action, walker):
        WalkerBuffer.buffer["array"].append({
            "action": action,
            "building": (walker.building.x, walker.building.y),
            "currentCell": (walker.currentCell.x, walker.currentCell.y) if walker.currentCell != None else None,
            "previousCell": (walker.previousCell.x, walker.previousCell.y) if walker.previousCell != None else None,
            "type": str(walker)})

    def send():
        encodeJSON(WalkerBuffer.buffer)
        WalkerBuffer.buffer = {"header": "walker",
                               "username": WalkerBuffer.username, "array": []}
