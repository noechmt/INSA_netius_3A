#include "lan_connect.h"

// Sending messages to port
int sending(char *ip_adress, int port, char *msg)
{
    int opt = 1;
    // Fetching port number

    int sock = 0;
    struct sockaddr_in serv_addr;
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        close(sock);
        printf("\n Socket creation error \n");
        return -1;
    }
    printf("socket fd : %i\n", sock);
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = inet_addr(ip_adress); // INADDR_ANY always gives an IP of 0.0.0.0
    serv_addr.sin_port = htons(port);
    if (setsockopt(sock, SOL_SOCKET, SO_REUSEADDR, (char *)&opt, sizeof(opt)) < 0)
    {
        perror("sock option problem ");
    }
    // printf("Waiting for connection\n");
    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
        sleep(0.001);
        return 1;
    }
    if (strlen(msg) != 0)
    {
        if (strncmp(msg, "/quit", strlen("/quit")) == 0)
        {
            return -1;
        }
        /*printf("%s\n", msg);
        msg = cesar_super_open_ssl(msg, 1);*/
        if (send(sock, msg, strlen(msg), MSG_WAITALL) < 0)
        {
            perror("send error ");
        };
    }
    close(sock);
    return 1;
}

void initialize_player(player *play)
{
    play->ip_adress = calloc(sizeof(char), 15);
    bzero(play->ip_adress, 15);
}

int sending_local(char *msg)
{

    int sock_local = 0;
    struct sockaddr_in serv_addr;
    if ((sock_local = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        close(sock_local);
        printf("\n Socket creation error \n");
        return -1;
    }
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = inet_addr("127.0.0.1"); // INADDR_ANY always gives an IP of 0.0.0.0
    serv_addr.sin_port = htons(1235);

    struct linger so_linger;
    so_linger.l_onoff = 1;
    so_linger.l_linger = 1;
    if (setsockopt(sock_local, SOL_SOCKET, SO_LINGER, &so_linger, sizeof(so_linger)) == -1)
    {
        close(sock_local);
    }

    // printf("Waiting for connection\n");
    if (connect(sock_local, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
        sleep(0.001);
        return 1;
    }
    if (strlen(msg) != 0)
    {
        if (strncmp(msg, "/quit", strlen("/quit")) == 0)
        {
            close(sock_local);
            return -1;
        }
        /*printf("%s\n", msg);
        msg = cesar_super_open_ssl(msg, 1);*/
        if (send(sock_local, msg, strlen(msg), MSG_WAITALL) < 0)
        {
            perror("send error ");
        }
    }
    close(sock_local);
    return 1;
}

// Calling receiving every 2 seconds
void *receive_thread(void *fd)
{
    int s_fd = *((int *)fd);
    while (1)
    {
        sleep(0.001);
        receiving(s_fd);
    }
}

char *cesar_super_open_ssl(char *msg, int cle)
{
    for(int i=0; i<strlen(msg); i++){
        msg[i] = msg[i] + cle;
    }
    return msg;
}

char *de_cesar_super_open_ssl(char *msg, int cle)
{
    for(int i=0; i<strlen(msg); i++){
        msg[i] = msg[i] - cle;
    }
    return msg;
}