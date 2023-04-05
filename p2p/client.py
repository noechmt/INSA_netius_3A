from socket_python import *

client = set_client()

for i in range(20) :
    send_data(client,"Message pour le server\n")
    sleep(1)

    
close_socket(client)