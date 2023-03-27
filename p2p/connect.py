import ctypes as ct
import os

libc = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libc.so')
clibrary = ct.CDLL(libc)

clibrary.serveur()