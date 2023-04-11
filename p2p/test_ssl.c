#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <openssl/ssl.h>
#include <openssl/bio.h>
#include <openssl/err.h>
#include <unistd.h>

#define BUF_SIZE 1024

int main(int argc, char *argv[]) {
    SSL_CTX *ctx;
    SSL *ssl;
    BIO *bio;
    int sockfd, connfd;
    struct sockaddr_in serv_addr, peer_addr;

    // Initialisation du contexte SSL
    SSL_library_init();
    ctx = SSL_CTX_new(SSLv23_method());

    // Création de la socket
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1) {
        printf("Erreur lors de la création de la socket\n");
        return 1;
    }

    // Configuration de l'adresse locale
    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    serv_addr.sin_port = htons(8888); // Port local

    // Attachement de la socket à l'adresse locale
    if (bind(sockfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) != 0) {
        printf("Erreur lors de l'attachement de la socket\n");
        return 1;
    }

    // Écoute de la socket
    if (listen(sockfd, 5) != 0) {
        printf("Erreur lors de l'écoute de la socket\n");
        return 1;
    }

    // Attente de la connexion d'un pair
    int len = sizeof(peer_addr);
    connfd = accept(sockfd, (struct sockaddr*)&peer_addr, &len);
    if (connfd < 0) {
        printf("Erreur lors de l'acceptation de la connexion du pair\n");
        return 1;
    }

    // Initialisation de la connexion SSL
    bio = BIO_new_socket(connfd, BIO_NOCLOSE);
    ssl = SSL_new(ctx);
    SSL_set_bio(ssl, bio, bio);
    SSL_accept(ssl);

    // Réception de données chiffrées SSL
    char buffer[BUF_SIZE];
    int n = SSL_read(ssl, buffer, BUF_SIZE);
    buffer[n] = '\0';
    printf("Message reçu du pair : %s\n", buffer);

    // Envoi de données chiffrées SSL
    char *message = "Bonjour, pair !";
    SSL_write(ssl, message, strlen(message));

    // Libération des ressources
    SSL_shutdown(ssl);
    SSL_free(ssl);
    SSL_CTX_free(ctx);
    close(connfd);
    close(sockfd);

    return 0;
}