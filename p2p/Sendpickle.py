import threading as thread
from socket_python import *
import subprocess
import pickle


Process = subprocess.Popen(['./lan_connect', "192.168.1.54"])

Server(1235,1)
"""
send_data("|________|"*10)
sleep(1)
print("allo")
sleep(2)

send_data("||||||||||")
send_data("/quit")
print("allo2")"""

sleep(1)
Client("127.0.0.1",1236)
sleep(1)
Client.sendData("|________|"*10)

sleep(1)

Client.sendData("123456789\0"*4)

#Client.sendData("/quit")
Client.close()
Server.close()
sleep(3)
Process.kill()

