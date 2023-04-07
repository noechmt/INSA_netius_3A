import threading as thread
from socket_python import *
import subprocess

def sendPickleFile() :
    pass

    
def recvPickleFile():
    
    Server(1235,1)
    subprocess.Popen(['p2p/lan_connect', ])
    
    
Process = subprocess.Popen(['./lan_connect', "192.168.43.201"])

Server(1235,1)
sleep(1)
Client("127.0.0.1",1236)
Client.sendData("|________|"*10)


sleep(2)

Client.sendData("||||||||||"*10)
Client.close()
sleep(3)
Process.kill()
