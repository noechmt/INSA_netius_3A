import socket

from socket_python import *

s = MySocket()
s.connect("127.0.0.1", 1234)
sleep(1)
s.mysend(b"hello")
sleep(2)
s.close()