import socket
from time import sleep
import select

MSGLEN =  10

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
    
    def listen(self,number):
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
    
    def getSock(self) :
        return self.sock
        

def set_server(port,number):
    server= MySocket()
    server.bind("127.0.0.1", port)
    server.listen(number)
    return server
    
    
def set_client(port):
    client = MySocket()
    client.connect("127.0.0.1", port)
    return client
    

def send_data(data,addr="127.0.0.1",port=1234):
    Socket = MySocket()
    Socket.connect(addr,port)
    print("Connected")
    Socket.mysend(data.encode())
    Socket.close()
    

def recv_data(server_socket,freq=1):

    while True :
        sleep(freq)

        inputs = [server_socket.getSock()]
        
        # Utiliser select pour surveiller les canaux prêts à être lus
        readable, writable, exceptional = select.select(inputs, [], [])
        
        # Traiter les connexions prêtes à être lues
        print(inputs)
        for s in readable:
            print("Je suis dans redable")
            if s is server_socket.getSock():
                print("If")
                # Nouvelle connexion entrante
                client_socket = server_socket.accept()
                data = s.recv(1024)
                print(f"Data received: {data}")
                # Ajouter la connexion cliente à la liste de surveillance
                inputs.append(client_socket)
                print(inputs)
            else:
                print("Else")
                # Données prêtes à être lues
                data = s.recv(1024)
                print(data)
                if data:
                    # Traiter les données reçues
                    print(f"Data received: {data}")
                else:
                    # Fermer la connexion et la retirer de la liste de surveillance
                    s.close()
                    inputs.remove(s)
    
def get_data(socket):
    tmp = socket.data 
    socket.data = []
    return tmp

def close_socket(socket):
    socket.close()


def th_recv(server,freq=2) :

        recv_data(server)
        