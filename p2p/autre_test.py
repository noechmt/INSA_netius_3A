import socket
import ssl

# Créer une connexion TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 8000))
sock.listen(1)

# Attendre une connexion entrante
print('En attente de connexion...')
conn, addr = sock.accept()
print('Connexion établie:', addr)

# Initialiser le contexte SSL
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile='server.crt', keyfile='server.key')

# Utiliser le contexte pour initialiser la connexion SSL
ssl_conn = context.wrap_socket(conn, server_side=True)
print('Connexion SSL établie:', ssl_conn)

# Recevoir des données de l'autre partie
data = ssl_conn.recv(1024)
print('Données reçues:', data)

# Fermer la connexion SSL et la connexion TCP/IP
ssl_conn.shutdown()
sock.close()
