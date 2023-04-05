// C program to demonstrate peer to peer chat using Socket Programming
#include <unistd.h>
#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <sys/select.h>
#include <errno.h>
#include <string.h>

// INADDR_ANY
char name[20];
int PORT = 1234;
int LOCAL_PORT = 1236;

int sending(char *adress, int port);
void local_connect(int local_fd);
void receiving(int fd);
void receiving_local(int local_fd);
void *receive_thread(void *fd);
void *receive_local_thread(void *local_fd);

void local_connect(int local_fd)
{

    struct sockaddr_in address_local;
    address_local.sin_family = AF_INET;
    address_local.sin_addr.s_addr = inet_addr("127.0.0.1");
    address_local.sin_port = htons(1236);

    struct linger so_linger;
    so_linger.l_onoff = 1;
    so_linger.l_linger = 1;

    if (setsockopt(local_fd, SOL_SOCKET, SO_LINGER, &so_linger, sizeof(so_linger)) == -1)
    {
        close(local_fd);
    }
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

int main(int argc, char **argv)
{
    if (argc < 2)
    {
        printf("argument pls\n");
        return 0;
    }
    /*printf("Enter your port number:");
    scanf("%d", &PORT);*/

    int server_fd, local_fd;
    struct sockaddr_in address;

    // Creating socket file descriptor
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == -1)
    {
        perror("socket failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    if ((local_fd = socket(AF_INET, SOCK_STREAM, 0)) == -1)
    {
        perror("local socket failed");
        close(local_fd);
        exit(EXIT_FAILURE);
    }

    local_connect(local_fd);
    // Forcefully attaching socket to the port

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    struct linger so_linger;
    so_linger.l_onoff = 1;
    so_linger.l_linger = 1;
    if (setsockopt(server_fd, SOL_SOCKET, SO_LINGER, &so_linger, sizeof(so_linger)) == -1)
    {
        close(server_fd);
        close(local_fd);
    }

    // Printed the server socket addr and port
    printf("IP address is: %s\n", inet_ntoa(address.sin_addr));
    printf("port is: %d\n", (int)ntohs(address.sin_port));

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0)
    {
        perror("bind failed");
        close(server_fd);
        close(local_fd);
        exit(EXIT_FAILURE);
    }
    if (listen(server_fd, 5) < 0)
    {
        perror("listen");
        close(server_fd);
        exit(EXIT_FAILURE);
    }
    pthread_t tid, tid2;
    pthread_create(&tid, NULL, &receive_thread, &server_fd); // Creating thread to keep receiving message in real time
    pthread_create(&tid2, NULL, &receive_thread, &local_fd);  // Creating thread to keep receiving message in real time
    while (1)
    {
        if (sending(argv[1], 1234) < 0)
        {
            break;
        }
    }
    close(server_fd);
    close(local_fd);
}

// Sending messages to port
int sending(char *ip_adress, int port)
{

    // Fetching port number

    int sock = 0;
    struct sockaddr_in serv_addr;
    char buffer_send[1024] = {0};
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        close(sock);
        printf("\n Socket creation error \n");
        return -1;
    }
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = inet_addr(ip_adress); // INADDR_ANY always gives an IP of 0.0.0.0
    serv_addr.sin_port = htons(port);
    //printf("Waiting for connection\n");
    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
        sleep(2);
        return 1;
    }
    scanf("%s", buffer_send);
    if (strlen(buffer_send) != 0)
    {
        if (strncmp(buffer_send, "/quit", strlen("/quit")) == 0)
        {
            return -1;
        }
        send(sock, buffer_send, sizeof(buffer_send), 0);
        bzero(buffer_send, 1024);
    }
    printf("Message sent\n");
    close(sock);
    return 1;
}

// Calling receiving every 2 seconds
void *receive_thread(void *fd)
{
    int s_fd = *((int *)fd);
    while (1)
    {
        sleep(2);
        receiving(s_fd);
    }
}

// Receiving messages on our port
void receiving(int fd)
{
    struct sockaddr_in address;
    int valread;
    char buffer[2000] = {0};
    int addrlen = sizeof(address);
    fd_set current_sockets, ready_sockets;

    // Initialize my current set
    FD_ZERO(&current_sockets);
    FD_SET(fd, &current_sockets);
    int k = 0;
    while (1)
    {
        k++;
        ready_sockets = current_sockets;

        if (select(FD_SETSIZE, &ready_sockets, NULL, NULL, NULL) < 0)
        {
            perror("Error");
            exit(EXIT_FAILURE);
        }

        for (int i = 0; i < FD_SETSIZE; i++)
        {
            if (FD_ISSET(i, &ready_sockets))
            {

                if (i == fd)
                {
                    int client_socket;
                    printf("%i\n", fd);
                    if ((client_socket = accept(fd, (struct sockaddr *)&address,
                                                (socklen_t *)&addrlen)) < 0)
                    {
                        perror("accept");
                        exit(EXIT_FAILURE);
                    }
                    FD_SET(client_socket, &current_sockets);
                }
                else
                {
                    valread = recv(i, buffer, sizeof(buffer), 0);
                    sending("127.0.0.1", 1235);
                    FD_CLR(i, &current_sockets);
                }
            }
        }
        if (k == (FD_SETSIZE * 2))
            break;
    }
}