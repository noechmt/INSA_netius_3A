import socket
from time import sleep

MSGLEN =  10

class MySocket:
    
    def __init__(self, sock=None):
        self.data = []
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setblocking(False)
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

    def myreceive(self):
        recv = self.conn.recv(2048, socket.MSG_WAITALL)
        return recv.decode()
        

def set_server():
    server= MySocket()
    server.bind("127.0.0.1", 1235)
    server.listen(4)
    server.accept()

    return server
    
    
def set_client():
    client = MySocket()
    client.connect("127.0.0.1", 1235)
    return client
    

def send_data(socket, data):
    socket.mysend(data.encode())
    
def recv_data(socket):
    recv = socket.myreceive()
    print(recv)
    socket.data += recv
    return recv
    
def get_data(socket):
    tmp = socket.data 
    socket.data = []
    return tmp

def close_socket(socket):
    socket.close()
