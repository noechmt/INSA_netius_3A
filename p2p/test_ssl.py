import socket
from OpenSSL import SSL

# Créer une connexion TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 1236))
sock.listen(1)

# Attendre une connexion entrante
print('En attente de connexion...')
conn, addr = sock.accept()
print('Connexion établie:', conn)

# Initialiser le contexte SSL
context = SSL.Context(SSL.TLSv1_2_METHOD)
context.use_privatekey_file('p2p/server.key')
context.use_certificate_file('p2p/server.crt')

# Utiliser le contexte pour initialiser la connexion SSL
ssl_conn = SSL.Connection(context, conn)
ssl_conn.set_accept_state()
ssl_conn.do_handshake()

# Envoyer des données à l'autre partie
ssl_conn.send(b'Hello, world!')

# Recevoir des données de l'autre partie
data = ssl_conn.recv(1024)
print('Données reçues:', data)

# Fermer la connexion SSL et la connexion TCP/IP
ssl_conn.shutdown()
sock.close()
