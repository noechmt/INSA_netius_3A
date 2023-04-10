import socket
from time import sleep
import select
from OpenSSL import SSL

MSGLEN =  10

# adresse IP et port de l'hôte distant
remote_host = '127.0.0.1'
remote_port = 1236

# Initialiser le contexte SSL
context = SSL.Context(SSL.TLSv1_2_METHOD)
context.use_privatekey_file('p2p/server.key')
context.use_certificate_file('p2p/server.crt')
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
    ssl_sock = ssl_wrap_socket(Socket)
    print("Connected")
    ssl_sock.mysend(data.encode())
    ssl_sock.close()
    

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
                ssl_conn = SSL.Connection(context, client_socket)
                ssl_conn.set_accept_state()
                ssl_conn.do_handshake()
                Server.data = ssl_conn.recv(2048)
                Server.data = Server.data.decode()
                print(f"Data received: ",Server.data)
                
                # Ajouter la connexion cliente à la liste de surveillance
                inputs.append(ssl_conn)

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

def ssl_wrap_socket(sock):
    # créer un contexte SSL/TLS
    context = SSL.Context(SSL.TLSv1_2_METHOD)

    # charger les certificats et clés nécessaires
    context.set_default_verify_paths()

    # envelopper le socket avec SSL/TLS
    ssl_sock = SSL.Connection(context, sock)
    ssl_sock.set_connect_state()
    ssl_sock.set_tlsext_host_name(remote_host.encode())
    ssl_sock.do_handshake()

    return ssl_sock