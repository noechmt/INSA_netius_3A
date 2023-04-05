import socket

from socket_python import *
    

s1 = MySocket()
s1.bind("127.0.0.1", 1235)
s1.listen()
s1.accept()
sleep(1)
s1.myreceive()
sleep(3)
s1.close()