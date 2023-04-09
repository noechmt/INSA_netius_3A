#include "lan_connect.h"

// Sending messages to port
int sending(char *ip_adress, int port, char *msg, int server_fd)
{

    // Fetching port number

    /*int sock = 0;
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
    }*/
    if (strlen(msg) != 0)
    {
        if (strncmp(msg, "/quit", strlen("/quit")) == 0)
        {
            return -1;
        }
        printf("fd %i\n", server_fd);
        if (send(server_fd, msg, strlen(msg), 0) < 0)
        {
            perror("send error server ");
        };
        printf("aezr\n");
    }
    return 1;
}

void initialize_player(player *play)
{
    play->ip_adress = calloc(sizeof(char), 15);
    bzero(play->ip_adress, 15);
    play->fd = 0;
}


int sending_local(char *msg)
{

    int sock_local = 0;
    
    if (strlen(msg) != 0)
    {
        if (strncmp(msg, "/quit", strlen("/quit")) == 0)
        {
            close(sock_local);
            return -1;
        }
        if (send(sock_local, msg, strlen(msg), 0) < 0)
        {
            perror("send error local");
        }
    }
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
