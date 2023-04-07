import socket
from time import sleep
import select

LanProcess = None

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
   
   
class Client : 
    
    socket = None
    
    def __init__(self,addr,port) :
        
        Client.socket = socket.socket()
        Client.socket.connect((addr,port))
        
            
    def sendData(data) :
        Client.socket.send(data.encode())
        
    def close() : 
        Client.socket.close()
        
class Server:

    socket=None
    data=""
        
    def __init__(self,port,number):
        Server.socket= MySocket()
        Server.socket.bind("127.0.0.1", port)
        Server.socket.listen(number)




def send_data(data,addr="127.0.0.1",port=1236):
    
    Socket = MySocket()
    Socket.connect(addr,port)
    print("Connected")
    Socket.mysend(data.encode())
    Socket.close()
    

def recv_data(server_socket,freq=1):

    while True :
        sleep(freq)
        print(server_socket)
        inputs = [server_socket.getSock()]
        
        # Utiliser select pour surveiller les canaux prêts à être lus
        readable, writable, exceptional = select.select(inputs, [], [])
        
        # Traiter les connexions prêtes à être lues
        
        for s in readable:
            
            if s is server_socket.getSock():
                
                # Nouvelle connexion entrante
                client_socket = server_socket.accept()
                Server.data = client_socket.recv(2048)
                Server.data = Server.data.decode()
                print(f"Data received: ",Server.data)
                
                # Ajouter la connexion cliente à la liste de surveillance
                inputs.append(client_socket)

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
    
def get_data():
    tmp = []
    if Server.data :
        tmp = Server.data
        Server.data = ""
    
    return tmp

def close_socket(socket):
    socket.close()


        