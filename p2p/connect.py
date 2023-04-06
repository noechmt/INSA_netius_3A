import threading as thread
from socket_python import *

server = set_server(1235,4)

thread_recv = thread.Thread(target=recv_data, args=(server,))
thread_send = thread.Thread(target=send_data, args=("dataDePython",))
thread_recv.start()
thread_send.start()

# print("ok")
# server = set_server(1235)

# data ="Mes datas"
# thread_recv = thread.Thread(target=recv_data, args=(server,))

# thread_recv.start()
# # data = "je suis une data"
# # thread_recv = thread.Thread(target=recv_data, args=(server,))
# # thread_recv.start()
# # print("ok")

# # close_socket(client)
# close_socket(server)
    
