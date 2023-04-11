import threading as thread
from socket_python import *

def socket_init():
   Server(1235,4)
   
   thread_recv = thread.Thread(target=recv_data, args=(Server.socket,))
   thread_send = thread.Thread(target=send_data, args=("dataDePython",))
   thread_recv.start()
   thread_send.start()

Server(1235, 4)
send_data("coucou")