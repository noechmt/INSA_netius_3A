import socket
from OpenSSL import SSL

# adresse IP et port de l'hôte distant
remote_host = '127.0.0.1'
remote_port = 1236

def ssl_wrap_socket(sock):
    # créer un contexte SSL/TLS
    context = SSL.Context(SSL.TLSv1_2_METHOD)

    # charger les certificats et clés nécessaires
    context.set_default_verify_paths()

    # envelopper le socket avec SSL/TLS
    ssl_sock = SSL.Connection(context, sock)
    ssl_sock.set_connect_state()
    ssl_sock.set_tlsext_host_name(remote_host.encode())
    ssl_sock.do_handshake()

    return ssl_sock

# créer un socket client
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# se connecter à l'hôte distant
client_sock.connect((remote_host, remote_port))

# envelopper le socket client avec SSL/TLS
ssl_sock = ssl_wrap_socket(client_sock)

# envoyer des données à l'hôte distant
ssl_sock.sendall(b'Hello, remote host!')

# recevoir des données de l'hôte distant
data = ssl_sock.recv(1024)

# afficher les données reçues
print(data.decode())

# fermer la connexion SSL/TLS
ssl_sock.close()
