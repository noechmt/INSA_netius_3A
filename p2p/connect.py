import threading as thread
from socket_python import *
print("ok")
server = set_server(1235)
thread_recv = thread.Thread(target=recv_data, args=(server,))
thread_recv.start()



# client = set_client(1236)
# data = "je suis une data"

# thread_send= thread.Thread(target=send_data, args=(client, data,))
# thread_send.start()
# thread_recv = thread.Thread(target=recv_data, args=(server,))
# thread_recv.start()
# print("ok")

# close_socket(client)
close_socket(server)
    
