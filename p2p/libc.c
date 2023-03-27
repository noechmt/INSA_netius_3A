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

int sending(char *ip);
void serveur(char *ip, int PORT);
void receiving(int server_fd);
void *receive_thread(void *server_fd);

void serveur(char *ip, int PORT)
{
    /*printf("Enter your port number:");
    scanf("%d", &PORT);*/

    int server_fd;
    struct sockaddr_in address;

    // Creating socket file descriptor
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == -1)
    {
        perror("socket failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }
    // Forcefully attaching socket to the port

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    // address.sin_addr.s_addr = inet_addr("192.168.206.185");
    address.sin_port = htons(1234);

    struct linger so_linger;
    so_linger.l_onoff = 1;
    so_linger.l_linger = 1;
    if (setsockopt(server_fd, SOL_SOCKET, SO_LINGER, &so_linger, sizeof(so_linger)) == -1)
    {
        close(server_fd);
    }
    // Printed the server socket addr and port
    /*printf("IP address is: %s\n", inet_ntoa(address.sin_addr));
    printf("port is: %d\n", (int)ntohs(address.sin_port));*/
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

    pthread_t tid;
    pthread_create(&tid, NULL, &receive_thread, &server_fd); // Creating thread to keep receiving message in real time

    while (1)
    {
        if (sending(ip) < 0)
        {
            break;
        }
    }
    close(server_fd);

    return;
}

// Sending messages to port
int sending(char *ip1)
{

    // Fetching port number
    int PORT_server = 1234;

    int sock = 0;
    struct sockaddr_in serv_addr;
    char buffer_send[1024] = {0};
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        printf("\n Socket creation error \n");
        close(sock);
        return -1;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = inet_addr(ip1); // INADDR_ANY always gives an IP of 0.0.0.0
    serv_addr.sin_port = htons(PORT_server);

    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
        close(sock);
        return 0;
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
    printf("\nMessage sent\n");
    close(sock);
    return 1;
}

// Calling receiving every 2 seconds
void *receive_thread(void *server_fd)
{
    int s_fd = *((int *)server_fd);
    while (1)
    {
        sleep(2);
        receiving(s_fd);
    }
}

// Receiving messages on our port
void receiving(int server_fd)
{
    struct sockaddr_in address;
    int valread;
    char buffer[2000] = {0};
    int addrlen = sizeof(address);
    fd_set current_sockets, ready_sockets;

    // Initialize my current set
    FD_ZERO(&current_sockets);
    FD_SET(server_fd, &current_sockets);
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

                if (i == server_fd)
                {
                    int client_socket;

                    if ((client_socket = accept(server_fd, (struct sockaddr *)&address,
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
                    printf("%s\n", buffer);
                    FD_CLR(i, &current_sockets);
                }
            }
        }
        if (k == (FD_SETSIZE * 2))
            break;
    }
}