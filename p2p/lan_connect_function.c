#include "lan_connect.h"




// Sending messages to port
int sending(char *ip_adress, int port, char *msg)
{

    // Fetching port number

    int sock = 0;
    struct sockaddr_in serv_addr;
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        close(sock);
        printf("\n Socket creation error \n");
        return -1;
    }
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = inet_addr(ip_adress); // INADDR_ANY always gives an IP of 0.0.0.0
    serv_addr.sin_port = htons(port);
    // printf("Waiting for connection\n");
    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
        sleep(0.01);
        return 1;
    }
    if (strlen(msg) != 0)
    {
        if (strncmp(msg, "/quit", strlen("/quit")) == 0)
        {
            return -1;
        }
        if (send(sock, msg, strlen(msg), 0) < 0)
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
        sleep(0.01);
        return 1;
    }
    if (strlen(msg) != 0)
    {
        if (strncmp(msg, "/quit", strlen("/quit")) == 0)
        {
            close(sock_local);
            return -1;
        }
        if (send(sock_local, msg, strlen(msg), 0) < 0)
        {
            perror("send error ");
        }
    }
    close(sock_local);
    return 1;
}



