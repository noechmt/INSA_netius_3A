#include "lan_connect.h"

// Sending messages to port
int sending(char *ip_adress, int port, char *msg, int server_fd)
{

    // Fetching port number
    /*struct sockaddr_in serv_addr;

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = inet_addr(ip_adress); // INADDR_ANY always gives an IP of 0.0.0.0
    serv_addr.sin_port = htons(port);*/
    // printf("Waiting for connection\n");
    if (strlen(msg) != 0)
    {
        if (strncmp(msg, "/quit", strlen("/quit")) == 0)
        {
            return -1;
        }
        if (send(server_fd, msg, strlen(msg), 0) < 0)
        {
            perror("send error ");
        };
    }
    return 1;
}

void initialize_player(player *play)
{
    play->fd = 0;
    play->ip_adress = calloc(sizeof(char), 15);
    bzero(play->ip_adress, 15);
}

int sending_local(char *msg, int local_fd)
{
    struct linger so_linger;
    so_linger.l_onoff = 1;
    so_linger.l_linger = 1;
    if (setsockopt(local_fd, SOL_SOCKET, SO_LINGER, &so_linger, sizeof(so_linger)) == -1)
    {
        close(local_fd);
    }

    // printf("Waiting for connection\n");

    if (strlen(msg) != 0)
    {
        if (strncmp(msg, "/quit", strlen("/quit")) == 0)
        {
            close(local_fd);
            return -1;
        }
        if (send(local_fd, msg, strlen(msg), 0) < 0)
        {
            perror("send error ");
        }
    }
    return 1;
}

void flush_list(player *player)
{
    while (player->next_player != NULL)
    {
        close(player->fd);
        player = player->next_player;
    }
}