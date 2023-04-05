import socket
from time import sleep

MSGLEN =  10

class MySocket:
    
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
            #self.sock.setblocking(False)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))
        
    def bind(self, host, port):
        self.sock.bind((host, port))
    
    def listen(self):
        self.sock.listen(1)

    def mysend(self, msg):
        sent = self.sock.send(b"hello")
        
    def close(self):
        self.sock.close()
        
    def accept(self):
        self.conn, self.addr = self.sock.accept()

    def myreceive(self):
        recv = self.conn.recv(5, socket.MSG_WAITALL)
        print(recv.decode())
    
