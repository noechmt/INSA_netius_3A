#include "lan_connect.h"


void so_linger(int server_fd, int local_fd){

    struct linger so_linger;
    so_linger.l_onoff = 1;
    so_linger.l_linger = 1;
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &so_linger, sizeof(so_linger)) == -1)
    {
        perror("erreur solinger");
        close(server_fd);
    }
    if (setsockopt(local_fd, SOL_SOCKET, SO_REUSEADDR, &so_linger, sizeof(so_linger)) == -1)
    {
        perror("erreur solinger");
        close(local_fd);
    }

}

void server_connect(int server_fd)
{
    struct sockaddr_in address;
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(1234);

    

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0)
    {
        perror("bind failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }
    if (listen(server_fd, 5) < 0)
    {
        perror("listen");
        close(server_fd);
        exit(EXIT_FAILURE);
    }
}
void local_connect(int local_fd)
{

    struct sockaddr_in address_local;
    address_local.sin_family = AF_INET;
    address_local.sin_addr.s_addr = inet_addr("127.0.0.1");
    address_local.sin_port = htons(1236);

    if (bind(local_fd, (struct sockaddr *)&address_local, sizeof(address_local)) < 0)
    {
        perror("bind failed");
        close(local_fd);
        exit(EXIT_FAILURE);
    }
    if (listen(local_fd, 5) < 0)
    {
        perror("listen");
        close(local_fd);
        exit(EXIT_FAILURE);
    }
}
