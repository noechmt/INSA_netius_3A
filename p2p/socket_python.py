import socket
from time import sleep
import select
import threading as thread
MSGLEN = 10
import subprocess

class MySocket:

    def __init__(self, sock=None):
        self.data = []
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            # self.sock.setblocking(False)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def bind(self, host, port):
        self.sock.bind((host, port))

    def listen(self, number):
        self.sock.listen(number)

    def mysend(self, data):
        sent = self.sock.send(data)
        return sent

    def close(self):
        self.sock.close()

    def accept(self):
        self.conn, self.addr = self.sock.accept()
        return self.conn

    def myreceive(self):
        recv = self.conn.recv(15)
        return recv

    def getSock(self):
        return self.sock


class Server:

    socket = None
    data = ""

    def __init__(self, port, number):
        Server.socket = MySocket()
        Server.socket.bind("127.0.0.1", port)
        Server.socket.listen(number)


def send_data(data, addr="127.0.0.1", port=1236):

    Socket = MySocket()
    Socket.connect(addr, port)
    Socket.mysend(data.encode())
    Socket.close()


def recv_data(server_socket, freq=.001):

    while not Spython.stopEvent.is_set():
        sleep(freq)


        inputs = [server_socket.getSock()]

        # Utiliser select pour surveiller les canaux prêts à être lus
        readable, writable, exceptional = select.select(inputs, [], [])

        # Traiter les connexions prêtes à être lues
        print(input)
        for s in readable:

            if s is server_socket.getSock():

                # Nouvelle connexion entrante
                client_socket = server_socket.accept()
                Server.data = client_socket.recv(10000)
                Server.data = Server.data.decode()


                # Ajouter la connexion cliente à la liste de surveillance
                inputs.append(client_socket)

            else:
                print("Else")
                # Données prêtes à être lues
                data = s.recv(10000)

                print(data)
                if data:
                    # Traiter les données reçues
                    pass
                else:
                    # Fermer la connexion et la retirer de la liste de surveillance
                    s.close()
                    inputs.remove(s)


def get_data():
    tmp = []
    if Server.data:
        tmp = Server.data
        Server.data = ""

    return tmp


def close_socket(socket):
    socket.close()



stopEvent = thread.Event()

class Spython :
    
    thread_recv = None
    LanProcess = None
    stopEvent = None
    
    
    def __init__(self) :
        Spython.stopEvent = thread.Event()
    
    def startThread() : 
        Spython.thread_recv = thread.Thread(target=recv_data, args=(Server.socket,))
        Spython.thread_recv.start()
    
    
    def startLanProcess(txt) : Spython.LanProcess = subprocess.Popen(['p2p/lan_connect',txt])
      
    def endThread() : 
        Spython.stopEvent.set()
        sleep(.1)
        send_data("Bye",port=1235)
        
        
    
    def endLanProcess() : Spython.LanProcess.kill()