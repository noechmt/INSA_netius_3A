import ctypes as ct
import os
import threading as thread

libc = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libc.so')
clibrary = ct.CDLL(libc)
IP = b"192.168.206.185"
str2="None"
server_fd = clibrary.serveur(IP, ct.c_int(1234))

clibrary.serveur(b"192.168.206.134",ct.c_int(1234))
