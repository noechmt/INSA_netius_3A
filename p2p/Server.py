from socket_python import *
    
server = set_server()

for i in range(20) :
    print("\nRecved data : ",recv_data(server))
    print("\nServer.data : ",server.data)
    sleep(1)
    if i % 5 == 0 :
        get_data(server)


close_socket(server)