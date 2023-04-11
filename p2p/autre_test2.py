import socket
import ssl

# Créer une connexion TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 8000))

# Initialiser le contexte SSL
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# Utiliser le contexte pour initialiser la connexion SSL
ssl_conn = context.wrap_socket(sock, server_hostname='localhost')

# Envoyer des données à l'autre partie
ssl_conn.send(b'Hello, world!')

# Recevoir des données de l'autre partie
data = ssl_conn.recv(1024)
print('Données reçues:', data)

# Fermer la connexion SSL et la connexion TCP/IP
ssl_conn.shutdown()
sock.close()
