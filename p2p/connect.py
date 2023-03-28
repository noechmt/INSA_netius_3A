import ctypes as ct
import os
import threading as thread

libc = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libc.so')
clibrary = ct.CDLL(libc)
IP = b"192.168.206.185"
str2="None"
server_fd = clibrary.serveur(IP, ct.c_int(1234))

get_funct = clibrary.recup_4_python
get_funct.restype = ct.POINTER(ct.c_char)

t = thread.Thread(target=clibrary.receive_thread, args=(server_fd,))
t.start()

def send(data):
    t_send = thread.Thread(target=clibrary.sending, args=(IP, data))
    t_send.start()

def listener():
    string = get_funct()
    str = ct.c_char_p.from_buffer(string)
    if(str.value != str2):
        str2 = str.value
        return str.value.decode()
            # clibrary.sending(IP)
    """clibrary.receiving.restype = ct.c_char_p
            clibrary.receiving.argtypes = [ct.c_int]"""
    #   print(hex(clibrary.recup_4_python()))

    # clibrary.close_socket(server_fd)
